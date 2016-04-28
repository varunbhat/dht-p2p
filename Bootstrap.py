#!/usr/bin/env python

import asyncio
import datetime
import json
import logging
import socket

import aiocoap
import aiocoap.resource as resource
from BoostrapBuffer import BootstrapBuffer
from aiocoap import Context
from aiocoap.message import Message
from chord import Chord
import re


class Register(resource.Resource):
    def __init__(self):
        super(Register, self).__init__()
        self.bb = BootstrapBuffer()
        self.arearouter = {}

    @asyncio.coroutine
    def check_arearouter_capability(self,ip_details,area):
        logging.debug('Checking area router Capability in the registered Node')
        ip = ip_details[0]
        context = yield from Context.create_client_context()
        request = Message(code=aiocoap.GET)
        request.opt.uri_host = ip
        request.opt.uri_path = ('.well-known', 'core')
        resp = yield from context.request(request).response

        routers = re.findall(r'<([a-zA-Z\.0-9_\-/]+)>',resp.payload.decode('utf8'))

        if '/sensor/areaindex' in routers:
            self.bb.addressmap[self.bb.generate_key(area)] = (area, ip)
        else:
            #Todo: register with the next available area (Use google maps / gridfs)
            logging.warning('No area routers found. Dropping registration Request')

        print('Result: %s\n%r' % (resp.code, resp.payload))

    @asyncio.coroutine
    def join_requester(self, location, source_address):
        key = self.bb.generate_key(location)
        area,dest = self.bb.addressmap[key]

        if dest is not None:
            logging.debug('Creating a new PUT request to remote Node')

            context = yield from Context.create_client_context()
            request = Message(code=aiocoap.PUT,
                              payload=json.dumps({'source': source_address[0]}).encode('utf8'))
            request.opt.uri_host = source_address[0]
            request.opt.uri_path = ('sensor', 'register', key)
            resp = yield from context.request(request).response
            print('Result: %s\n%r' % (resp.code, resp.payload))
        else:
            logging.warning('No Area Router Present, Dropping Message')

    @asyncio.coroutine
    def render_put(self, request):
        data = json.loads(request.payload.decode('utf8'))
        area = data.get('location')

        if area is not None:
            ar = self.arearouter.get(self.bb.generate_key(area))
            if ar is None:
                logging.debug('No area router found for the location')
                asyncio.get_event_loop().create_task(self.check_arearouter_capability(request.remote,area))
                return aiocoap.Message(code=aiocoap.VALID)
            else:
                asyncio.get_event_loop().create_task(self.join_requester(area, request.remote))
                # response = json.dumps({'status': 1, 'node_id': location_hash}).encode('utf8')
                return aiocoap.Message(code=aiocoap.CREATED)
        else:
            # response = json.dumps({'status': -1}).encode('utf8')
            return aiocoap.Message(code=aiocoap.BAD_REQUEST)



# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():
    # Resource tree creation

    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('register',), Register())
    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
