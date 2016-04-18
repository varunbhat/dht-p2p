from ProtocolHandler import ProtocolHandler
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)-15s %(levelname)s] %(message)s')

ph = ProtocolHandler()
USERNAME = 'AlphaFoxtrot112'

test_file = open('test_cases.txt','r')

def read_test():
    data = test_file.readline()
    while True:
        print ph.parse_response(data)
        data = test_file.readline()
        if data == '':
            break


def write_test():
    print ph.parse_response(ph.register_request('127.0.0.1',5455,USERNAME))
    print ph.deregister_ip_request('127.0.0.1', 5455, USERNAME)
    print ph.parse_response('DEL IPADDRESS 127.0.0.1 5455 AlphaFoxtrot112')
    print ph.parse_response(ph.deregister_ip_request('127.0.0.1', 5455, USERNAME))


if __name__ == '__main__':
    read_test()
    print
    write_test()

