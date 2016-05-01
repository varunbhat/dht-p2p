import argparse
import asyncio
import configparser
import json
import logging

import aiocoap
import re
from aiocoap import resource
from aiocoap.message import Message
from aiocoap.protocol import Context


def arguement_parser():
    parser = argparse.ArgumentParser(description='Create a socket server')
    # parser.add_argument('-p', "--port", type=int, help='Port Number to use for the server', required=True)
    args = parser.parse_args()
    return args


config = configparser.RawConfigParser()
config.read('node.cfg')


def read_config():
    cfg = type('obj', (object,), {})
    ip, port = config.get('bootstrap', 'address').split(':')
    cfg.bs_address = (ip, int(port))
    return cfg


args = arguement_parser()
CONFIG = read_config()


class BootstrapServer(resource.Resource):
    def __init__(self):
        super(BootstrapServer, self).__init__()
        self.area_router_map = {}

    @asyncio.coroutine
    def render_put(self, request):
        query = dict([tuple(q.split('=')) for q in request.opt.uri_query])
        key = query.get('key')
        addr = (request.remote[0], int(query.get('port')))
        if key:
            if self.area_router_map.get(query['key']):
                asyncio.get_event_loop().create_task(
                    self.service_discovery_initiate(key, addr, self.area_router_map[query['key']]))
                return Message(code=aiocoap.CONTENT,
                               payload=json.dumps({'area_router': self.area_router_map[query['key']]}).encode('utf8'))
            else:
                asyncio.get_event_loop().create_task(self.find_area_router_capability(key, addr))
                return Message(code=aiocoap.NOT_FOUND)
        else:
            return Message(code=aiocoap.BAD_REQUEST)

    @asyncio.coroutine
    def find_area_router_capability(self, key, addr):
        context = yield from Context.create_client_context()
        request = Message(code=aiocoap.GET)
        request.opt.uri_host = addr[0]
        request.opt.uri_port = addr[1]
        request.opt.uri_path = ('.well-known', 'core')
        resp = yield from context.request(request).response

        routers = re.findall(r'<([a-zA-Z\.0-9_\-/]+)>', resp.payload.decode('utf8'))
        print(routers)

        if '/boostrap/areaindex' in routers:
            self.area_router_map[key] = addr
        else:
            # Todo: register with the next available area (Use google maps / gridfs)
            logging.warning('No area routers found. Dropping registration Request')

        print('Result: %s\n%r' % (resp.code, resp.payload))

    @asyncio.coroutine
    def service_discovery_initiate(self, key, addr, area_addr):
        logging.debug('Creating a new PUT request to remote Node')

        context = yield from Context.create_client_context()
        request = Message(code=aiocoap.PUT, payload=json.dumps({'source': addr, 'area': key}).encode('utf8'))
        request.opt.uri_host = area_addr[0]
        request.opt.uri_port = area_addr[1]
        request.opt.uri_path = ('node', 'register')
        resp = yield from context.request(request).response
        print('Result: %s\n%r' % (resp.code, resp.payload))


class BootstrapDomainUpdate:

    def __init__(self):
        pass

    @asyncio.coroutine
    def updateIpAddress(self):
        "http://username:password@dynupdate.no-ip.com/nic/update?hostname=mytest.testdomain.com&myip=1.2.3.4

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():
    logging.debug('Starting the Bootstrap Server')
    root = resource.Site()
    root.add_resource(('bootstrap','register'), BootstrapServer())
    logging.debug('starting at Port:%s' % CONFIG.bs_address[1])
    asyncio.async(aiocoap.Context.create_server_context(root, bind=('', CONFIG.bs_address[1])))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    print(1)
    main()
