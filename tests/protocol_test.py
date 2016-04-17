from BootstrapProtocol import ProtocolHandler
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)-15s %(levelname)s] %(message)s')

ph = ProtocolHandler()

test_file = open('test_cases.txt','r')

data = test_file.readline()

while True:
    print ph.parse_response(data)
    data = test_file.readline()
    if data == '':
        break
