import asyncio
import json

from aiocoap import *
import aiocoap


@asyncio.coroutine
def main():
    context = yield from Context.create_client_context()

    request = Message(code=aiocoap.GET, payload=json.dumps({'sensor': 'asdf'}).encode('utf8'))
    request.set_request_uri('coap://localhost:10001/node/register')
    #request.opt.uri_query = ('key=%s'%(1255252522454545454545454545),'port=%s'%(1255))
    response = yield from context.request(request).response
    print('Result: %s\n%r' % (response.code, response.payload))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
