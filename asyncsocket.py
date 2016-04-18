import Queue
import logging
import socket
import threading
import time
import requests
import re


class AsyncNode:
    __registered_events = {}
    __threads = []
    __persistant_threads = []
    __persistant_thread_function = []
    __middlewares = []
    __thread_queue = Queue.Queue()
    __response_events = {}

    def __init__(self, address=('', 10000)):
        self.stop_flag = False
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

        self._run_event_handler(self._get_event_handler('start'))

        while True:
            try:
                self._run_event_handler(self._get_event_handler('loop'))
                time.sleep(.5)
            except KeyboardInterrupt:
                self.stop()
                break

    def stop(self):
        self._run_event_handler(self._get_event_handler('stop'))
        self.stop_flag = True
        logging.warn('Waiting for Thread Handler to exit.')
        self.thread_handler.join()

        for ware in self.__middlewares:
            ware.stop()

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
        server.settimeout(1)

        logging.debug('Server Bound at %s:%d' % ('0.0.0.0', self.address[1]))
        server.bind(('', self.address[1]))

        while not self.stop_flag:
            try:
                # Read Data
                data, addr = server.recvfrom(1024 * 24)
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
        response = self._run_event_handler(self._get_event_handler('message'), data, sock, src_address)

        if response is not None:
            logging.debug('Response sent: %s' % response)
            sock.sendto(response, src_address)

    def _socket_receive(self, sock, callback=None,event=None, addr=None, *args, **kwargs):
        try:
            data = sock.recv(1024 * 8)
        except socket.timeout:
            logging.debug('Socket Timeout. No Callback Set.')
            sock.close()
            if callback is not None:
                callback(True, None)
            return
        sock.close()

        if callback is None:
            self._run_event_handler(self._get_event_handler('message'), data, sock, addr)
        elif event is not None:
            self._run_event_handler(self._get_event_handler(event), data, sock, addr)
        else:
            callback(data, *args, **kwargs)

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

    def send_data(self, dest_ip, dest_port, message, callback=None,event=None, *args, **kwargs):
        sock = self._get_socket()
        addr = (dest_ip, dest_port)
        logging.debug('Socket Sending Data:%s' % (message))
        sock.sendto(message, addr)
        if callback is not None or event is not None:
            self.sprawn_thread(self._socket_receive, sock, callback, event,addr, *args, **kwargs)
