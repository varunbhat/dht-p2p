from ProtocolHandler import ProtocolHandler
from asyncsocket import AsyncNode
import ConfigParser
import time

config = ConfigParser.RawConfigParser()
config.read('../node.cfg')

username = config.get('node', 'username')

addresses = '''
129.82.46.190:30000
129.82.46.191:30000
129.82.46.194:30000
129.82.46.204:30000
129.82.46.205:30000
129.82.46.207:30000
129.82.46.225:30000
129.82.46.226:30000
129.82.46.230:30000
129.82.46.231:30000
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


def get_response(data,err, *args, **kwargs):
    if err:
        print data, args, kwargs


if __name__ == '__main__':
    node.start_thread_handler()
    for addr in addresses:
        node.sprawn_thread(node.send_data(addr, protocol.list_all(username), callback=get_response,address=addr))
        time.sleep(0.1)
    node.stop()

