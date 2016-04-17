import Queue
import logging
import socket
import threading
import time

import re
import requests
from PeerProtocol import PeerProtocol


class PeerClient:
    debug = False
    __registered_events = {}
    __threads = []
    __persistant_threads = []
    __persistant_thread_function = []
    __middlewares = []
    __thread_queue = Queue.Queue()
    __response_events = {}

    def __init__(self, username=None, address=('', 10000)):
        self.sock = None
        self.username = username
        self.stop_flag = False
        self.bootstrap_address = None
        self.protocol = PeerProtocol()
        self.format_address(address)
        self._run_event_handler(self._get_event_handler('init'))

    def format_address(self, address):
        ip, port = address
        # Check peer Address if set properly
        if ip == '' or ip == None:
            self.address = (self._get_public_ip(), port)
        else:
            self.address = (ip, port)
        logging.info('Node Address: %s:%d' % self.address)

    def start(self, ip='', port=10000):
        self.format_address((ip, port))
        self._run_event_handler(self._get_event_handler('init'))


        # Start the middlewares register
        for middleware in self.__middlewares:
            self.__thread_queue.put(threading.Thread(target=middleware.start, args=()))

        self.__persistant_thread_function.append(self._read_thread)

        # Start the Thread Manager
        self.thread_handler = threading.Thread(target=self._thread_handler, args=())
        self.thread_handler.start()

        while True:
            try:
                self._run_event_handler(self._get_event_handler('start'))
                time.sleep(.5)
            except KeyboardInterrupt:
                self._run_event_handler(self._get_event_handler('stop'))
                self.stop_flag = True
                logging.warn('Waiting for Thread Handler to exit.')
                self.thread_handler.join()

                for ware in self.__middlewares:
                    ware.stop_flag = True
                break

    def get_address(self):
        return self.address

    def _get_public_ip(self):
        r = requests.get('http://jsonip.com')
        return r.json()['ip']

    def use(self, middleware_class):
        self.__middlewares.append(middleware_class)

    def on(self, event_name):
        def event_processor(func):
            self.__registered_events[event_name] = func
            return func

        return event_processor

    def response(self, event_name):
        def event_processor(func):
            self.__response_events[event_name] = func
            return func

        return event_processor

    def _thread_handler(self):
        # Manage the thread if it has exited for some reason
        self.__persistant_threads = [None for i in range(len(self.__persistant_thread_function))]

        while not self.stop_flag:
            for i in range(len(self.__persistant_thread_function)):
                if self.__persistant_threads[i] is None or self.__persistant_threads[i].isAlive() is False:
                    self.__persistant_threads[i] = threading.Thread(target=self.__persistant_thread_function[i],
                                                                    args=())
                    logging.warning('Starting %s.' % str(self.__persistant_threads[i]))
                    self.__persistant_threads[i].start()

            while True:
                try:
                    thread = self.__thread_queue.get(timeout=1)
                    thread.start()
                    self.__threads.append(thread)
                except Queue.Empty:
                    pop_count = 0
                    for i in range(len(self.__threads)):
                        if not self.__threads[i - pop_count].isAlive():
                            self.__threads.pop(i - pop_count)
                            pop_count += 1
                    break

        for thread in self.__persistant_threads + self.__threads:
            logging.warn('Waiting for %s Thread to complete' % (str(thread)))
            thread.join()
        logging.debug('Node Thread Handler stopped threads successfully.')

    def _read_thread(self):
        # Server Socket
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(0.5)

        logging.debug('Server Bound at %s:%d' % ('0.0.0.0', self.address[1]))
        server.bind(('', self.address[1]))

        while not self.stop_flag:
            try:
                # Read Data
                data, addr = server.recvfrom(1024)
            except socket.timeout:
                continue

            logging.debug('Received Request: %s from %s' % (data, str(addr)))
            self.sprawn_thread(self._message_processor, server, data, addr)

    def _get_event_handler(self, event_name):
        return self.__registered_events.get(event_name)

    def _run_event_handler(self, event_handler, *args, **kwargs):
        if event_handler is not None:
            return event_handler(*args, **kwargs)
        else:
            return None

    def _message_processor(self, sock, data, src_address):
        self._run_event_handler(self._get_event_handler('message'), data, sock, src_address)

        # Process the data
        try:
            data_len, data = re.findall(r'(\d{3}) (.*)', data)[0] if len(data) > 0 else (0, '')
        except IndexError:
            return

        # Process and generate Response
        request = self.protocol.parse_request(data)
        logging.debug('Parsed Request:%s' % (str(request)))

        response = self._handle_request(request)

        if response is not None:
            logging.debug('Response sent: %s' % response)
            sock.sendto(response, src_address)

    def _handle_request(self, req):
        if req is None:
            return self._run_event_handler(self._get_event_handler('invalid_message')) or self.protocol.unknown_request(
                9999)
        elif req['type'] == 'JOIN':
            return self._run_event_handler(self._get_event_handler('join'), False, req) or self.protocol.join_response(
                0)
        elif req['type'] == 'LEAVE':
            return self._run_event_handler(self._get_event_handler('leave'), False,
                                           req) or self.protocol.leave_response(0)
        elif req['type'] == 'SER':
            ip, port = self.address
            return self._run_event_handler(self._get_event_handler('search'), False, req)
        elif req['type'] == 'SER' and req['response_flag']:
            return None
        else:
            return self._run_event_handler(self._get_event_handler(req['type']), False,
                                           req) or self.protocol.unknown_request(9999)

    def _socket_receive(self, sock, callback=None, addr=None):
        try:
            data = sock.recv(1000)
        except socket.timeout:
            logging.debug('Socket Timeout. No Callback Set.')
            sock.close()
            if callback is not None:
                callback(True, None)
            return
        sock.close()

        self._run_event_handler(self._get_event_handler('message'), data)

        data_len, data = re.findall(r'(\d{3}) (.*)', data)[0]
        response = self.protocol.parse_response(data)
        if addr is not None:
            response['host_address'] = addr

        if callback is not None:
            callback(False, response)

    def sprawn_thread_wrapper(self, func, args):
        args, kwargs = args
        if func is not None:
            func(*args, **kwargs)

    def sprawn_thread(self, func, *args, **kwargs):
        self.__thread_queue.put(threading.Thread(target=self.sprawn_thread_wrapper, args=(func, (args, kwargs))))

    def _get_socket(self, timeout=5):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)
        return sock

    def join(self, ip, port):
        logging.debug('Join Request.Peer Address:%s:%d' % (ip, port))
        message = self.protocol.join_request(*self.address)
        self.send_data(ip, port, message, self.__response_events.get('join'), (ip, port))

    def leave(self, ip, port):
        logging.debug('Leave Request.Peer Address:%s:%d' % (ip, port))
        message = self.protocol.leave_request(*self.address)
        self.send_data(ip, port, message, self.__response_events.get('leave'), (ip, port))

    def search(self, peer_ip, peer_port, filename, uid, hops):
        logging.debug('Search Request.Filename:%s, Destination:%s' % (filename, str(((peer_ip, peer_port)))))
        ip, port = self.address
        message = self.protocol.search_request(ip, port, filename, uid, hops)
        self.send_data(peer_ip, peer_port, message)

    def send_data(self, dest_ip, dest_port, message, callback=None, *args, **kwargs):
        sock = self._get_socket()
        logging.debug('Socket Sending Data:%s' % (message))
        sock.sendto(message, (dest_ip, dest_port))
        if callback is not None:
            self.sprawn_thread(self._socket_receive, sock, callback, *args, **kwargs)
