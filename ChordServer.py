import asyncio
import json
import socket

from aiocoap import resource
from aiocoap.message import Message
from aiocoap.protocol import Context
from chord import Chord


class RangeFinder:
    def __init__(self, bootstrap_addr, address=(socket.gethostbyname(socket.gethostname()), 5683)):
        self.chord = Chord()
        self.chord.set_nodeid('%s:%d' % (address[0], address[1]))
        self.stable_flag = False
        self.bootstrap_addr = bootstrap_addr
        self.address = address

    @asyncio.coroutine
    def render_get(self, request):
        # Get request for search key
        info = json.loads(request.payload.decode('utf8'))
        key = info.get('key')
        if self.chord.in_range(key):
            # Check if the key belongs to this range
            return Message(code=asyncio.CONTENT, payload=json.dumps({'addr': self.address}))
        else:
            # If it does not belong to this range, find the next node it belongs to
            addr = self.chord.get_max_dist_address(key)

            # Send the request
            context = yield from Context.create_client_context()
            request = Message(code=asyncio.GET)
            request.opt.uri_host = addr
            request.opt.uri_path = ('peer', 'search')
            request.opt.uri_query = {'key': key}

            # Get the response
            resp = yield from context.request(request).response
            if resp.code == asyncio.CONTENT:
                info = json.loads(resp.payload.decode('utf8'))

            else:
                resp.

    def run(self):
        root = resource.Site()
        root.add_resource(('peer', 'search'), RangeFinder())
        loop = asyncio.get_event_loop()
        loop.create_task(self.bootstrap_communication())
