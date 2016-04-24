from ProtocolHandler import ProtocolHandler
from asyncsocket import AsyncNode
import ConfigParser
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s] %(message)s')

config = ConfigParser.RawConfigParser()
config.read('../node.cfg')

username = config.get('node', 'username')

'''
129.82.46.230:30000
129.82.46.205:30000
'''

addresses = '''
129.82.46.190:30000
129.82.46.191:30000
129.82.46.194:30000
129.82.46.204:30000
129.82.46.207:30000
129.82.46.225:30000
129.82.46.226:30000
129.82.46.231:30000
129.82.46.190:40000
129.82.46.191:40000
129.82.46.194:40000
129.82.46.204:40000
129.82.46.205:40000
'''


def get_addr():
    global addresses
    addresses = addresses.split('\n')
    l_addr = []
    for addr in addresses:
        temp = addr.split(':')
        if len(temp) > 1:
            l_addr.append(temp)
    return protocol.format_addresses(l_addr)


protocol = ProtocolHandler()
node = AsyncNode()
addresses = get_addr()


def register_response(data, *args, **kwargs):
    if data is not None or data != '':
        print protocol.parse_response(data)


def get_response(data, address=None, *args, **kwargs):
    if data != '':
        print address, " Working. Clients:", protocol.parse_response(data)['clients']


if __name__ == '__main__':
    node.start_thread_handler()

    # for addr in addresses:
    #     node.sprawn_thread(node.send_data(addr, protocol.list_all(username), callback=get_response, address=addr))
    #     time.sleep(0.1)

    # for addr in addresses:
    #     node.sprawn_thread(
    #         node.send_data(addr, protocol.register_request(node.get_address(), username), callback=register_response,
    #                        address=addr))
    #     time.sleep(0.1)
    #
    # for addr in addresses:
    #     node.sprawn_thread(
    #         node.send_data(addr, protocol.deregister_ip_request(node.get_address(), username),
    #                        callback=register_response,
    #                        address=addr))
    #     time.sleep(0.1)



    # for addr in addresses:
    #     node.sprawn_thread(
    #         node.send_data(addr, protocol.deregister_ip_request(node.get_address(), username),
    #                        callback=register_response,
    #                        address=addr))
    #     time.sleep(0.1)

    # for addr in addresses:
    #     node.sprawn_thread(
    #         node.send_data(addr, protocol.update_finger_request(protocol.LEAVE, ('127.0.0.1', 8000), 'asdfasdfasdf'),
    #                        callback=register_response, address=addr))
    #     time.sleep(0.1)

    # for addr in addresses:
    #     node.sprawn_thread(
    #         node.send_data, addr, protocol.get_key_response([('127.0.0.1', 8000), ('127.0.0.1', 5000)],
    #                                                  [('abcd', 'helloworld'), ('abcde', 'helloworled')]),
    #                        callback=register_response, address=addr)
    #     time.sleep(0.1)

    # for addr in addresses:
    #     node.sprawn_thread(addr, protocol.update_finger_request(protocol.LEAVE, ('127.0.0.1', 8000), 'asdfasdfasdf'),
    #                        callback=register_response)
    #     time.sleep(0.1)

    ip, port = config.get('bootstrap', 'address').split(':')
    port = int(port)

    # print node.send_data((ip,port), protocol.register_request(node.get_address(),username), no_thread=True)
    print node.send_data((ip,port), protocol.deregister_all(username), no_thread=True)
    print node.send_data((ip,port), protocol.list_all(username), no_thread=True)

    # for i in range(80):
    #     node.send_data((ip, port),
    #                    protocol.deregister_ip_request(('127.0.0.1', 8000 + i), config.get('node', 'username')),
    #                    callback=register_response)
    #     time.sleep(0.25)
    #
    # for i in range(80):
    #     node.send_data((ip, port), protocol.register_request(('127.0.0.1', 8000 + i), config.get('node', 'username')),callback=register_response)
    #     time.sleep(0.25)

    node.stop()
