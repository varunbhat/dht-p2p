import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


def server_read():
    serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    serv.bind(('', 10001))

    while True:
        data, address = serv.recvfrom(1024)
        serv.sendto(data, address)


threading.Thread(target=server_read, args=())


def client_send():
    sock.sendto('hello', )
