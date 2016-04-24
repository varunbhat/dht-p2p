from ProtocolHandler import ProtocolHandler
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)-15s %(levelname)s] %(message)s')

ph = ProtocolHandler()
USERNAME = 'AlphaFoxtrot112'

test_file = open('test_cases.txt', 'r')


def read_test():
    data = test_file.readline()
    while True:
        print ph.parse_response(data)
        data = test_file.readline()
        if data == '':
            break
    print '=' * 100


def write_test():
    print ph.parse_response(ph.register_request(('127.0.0.1', 5455), USERNAME))
    print ph.deregister_ip_request(('127.0.0.1', 5455), USERNAME)
    print ph.parse_response('DEL IPADDRESS 127.0.0.1 5455 AlphaFoxtrot112')
    print ph.parse_response(ph.deregister_ip_request(('127.0.0.1', 5455), USERNAME))

    print '=' * 100

    print ph.leave_request(('127.0.0.1', 8000))
    print ph.leave_response(1255)
    print ph.join_request(('127.0.0.1', 8000))
    print ph.join_response(1255)
    print ph.update_finger_request(ph.LEAVE, ('127.0.0.1', 8000), 'asdfasdfasdf')
    print ph.update_finger_response(1255)
    print ph.get_key_request('asdfasdfasdf')
    print ph.get_key_response([('127.0.0.1', 8000), ('127.0.0.1', 5000)],
                              [('abcd', 'helloworld'), ('abcde', 'helloworled')])
    print ph.give_key_request([('127.0.0.1', 8000), ('127.0.0.1', 5000)],
                              [('abcd', 'helloworld'), ('abcde', 'helloworled')])
    print ph.give_key_response(2522)
    print ph.add_request(('127.0.0.1', 8000), ('abcd', 'helloworld'))
    print ph.add_response(2522)

    print '=' * 100

    print ph.parse_response(ph.leave_request(('127.0.0.1', 8000)))
    print ph.parse_response(ph.leave_response(1255))
    print ph.parse_response(ph.join_request(('127.0.0.1', 8000)))
    print ph.parse_response(ph.join_response(1255))
    print ph.parse_response(ph.update_finger_request(ph.LEAVE, ('127.0.0.1', 8000), 'asdfasdfasdf'))
    print ph.parse_response(ph.update_finger_response(1255))
    print ph.parse_response(ph.get_key_request('asdfasdfasdf'))
    print ph.parse_response(ph.get_key_response([('127.0.0.1', 8000), ('127.0.0.1', 5000)],
                              [('abcd', 'helloworld'), ('abcde', 'helloworled')]))
    print ph.parse_response(ph.give_key_request([('127.0.0.1', 8000), ('127.0.0.1', 5000)],
                              [('abcd', 'helloworld'), ('abcde', 'helloworled')]))
    print ph.parse_response(ph.give_key_response(2522))
    print ph.parse_response(ph.add_request(('127.0.0.1', 8000), ('abcd', 'helloworld')))
    print ph.parse_response(ph.add_response(2522))
    # print ph.search_request()


if __name__ == '__main__':
    read_test()
    # write_test()
