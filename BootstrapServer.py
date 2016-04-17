import Queue
import logging
import socket
import threading

import re
from BootstrapProtocol import BootstrapProtocol


class BootstrapServer:
    debug = False
    __registered_events = {}
    __threads = []
    __persistant_threads = []
    __persistant_thread_function = []
    __middlewares = []
    __thread_queue = Queue.Queue()
    __response_events = {}

    def __init__(self, username, ip, port):
        self.protocol = BootstrapProtocol(username)
        self.address = (ip, port)
        self.stop_flag = False

    def start(self):
        self._run_event_handler(self._get_event_handler('start'))

    def reconnect(self, ip, port):
        self.delete_ip(ip, port)
        self._run_event_handler(self._get_event_handler('start'))

    def _run_event_handler(self, event_handler, *args, **kwargs):
        logging.debug('Starting event Handler %s', (str(event_handler)))
        if event_handler is not None:
            return event_handler(*args, **kwargs)
        else:
            return None

    def response(self, event_name):
        def event_processor(func):
            self.__response_events[event_name] = func
            return func

        return event_processor

    def on(self, event_name):
        def event_processor(func):
            self.__registered_events[event_name] = func
            return func

        return event_processor

    def _get_event_handler(self, event_name):
        return self.__registered_events.get(event_name)

    def _get_socket(self, timeout=5):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)
        return sock

    def register(self, ip, port):
        logging.debug('Sending Register to Bootstrap Server, Node Address: %s:%d' % (ip, port))
        message = self.protocol.register_request(ip, port)
        self.send(message, self.address, self.__response_events.get('register'))

    def delete_ip(self, ip, port):
        logging.debug('Deregister IP from Bootstrap. Node Address:%s:%d' % (ip, port))
        message = self.protocol.deregister_ip_request(ip, port)
        self.send(message, self.address, self.__response_events.get('delete'))

    def sprawn_thread_wrapper(self, func, args):
        args, kwargs = args
        func(*args, **kwargs)

    def sprawn_thread(self, func, *args, **kwargs):
        # self.__thread_queue.put(threading.Thread(target=self.sprawn_thread_wrapper, args=(func, (args, kwargs))))
        threading.Thread(target=self.sprawn_thread_wrapper, args=(func, (args, kwargs))).start()

    def _socket_receive(self, sock, callback):
        try:
            data = sock.recv(1000)
        except socket.timeout:
            sock.close()
            callback(True, None)
            return
        sock.close()

        data_len, data = re.findall(r'(\d{4}) (.*)', data)[0]

        response = self.protocol.parse_response(data)
        callback(False, response)

    def send(self, message, address, receive_callback=None):
        sock = self._get_socket()
        sock.sendto(message, address)
        logging.debug('Message:%s Destination:%s' % (message, address))
        if receive_callback is not None:
            self.sprawn_thread(self._socket_receive, sock, receive_callback)
