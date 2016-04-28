import asyncio
import json

from aiocoap import *
import aiocoap


@asyncio.coroutine
def main():
    context = yield from Context.create_client_context()

    request = Message(code=aiocoap.PUT, payload=json.dumps({'location': 'Bangalore', 'type': 'string'}).encode('utf8'))
    request.set_request_uri('coap://localhost/register')
    response = yield from context.request(request).response
    print('Result: %s\n%r' % (response.code, response.payload))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
