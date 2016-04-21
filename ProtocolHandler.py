import re
import logging
import uuid


class ProtocolHandler:
    LEAVE = 1
    JOIN = 0

    def parse_response(self, data):
        regex_string = r'(REG|DEL|BS|GET|JOIN|LEAVE|SER|UPFIN|GETKY|GIVEKY|ADD|[A-Z]+)(' \
                       r'(?<=REG)(?P<reg_address>( \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+)+) (?P<reg_username>[^0-9_][A-Za-z_0-9]+)|' \
                       r'(?<=REG)(?P<reg_resp>OK) ((?P<username_reg>[^0-9_][A-Za-z_0-9]+) )?(?P<error_code_reg>-?\d+)(?P<client_list_reg>( \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+){0,3})|' \
                       r'(?<=DEL) (IPADDRESS|UNAME)? *(?P<del_resp>OK)? *(?P<username_del>[^0-9_][A-Za-z_0-9]+)? *(?P<client_list_del>( *\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+){0,3}) *(?P<error_code_del>-?\d+)|' \
                       r'(?<=BS) REQ (?P<error_code_bs>-?\d+)|' \
                       r'(?<=GET) IPLIST (?P<get_resp>OK )?(?P<username_get>[^0-9_][A-Za-z_0-9]+) ?(?P<client_count>\d+)? *(?P<client_list_get>( *\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+)+)?|' \
                       r'(?<=JOIN) (?P<address_join>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+)|' \
                       r'(?<=JOIN)(?P<join_resp>OK) (?P<error_code_join>-?\d+)|' \
                       r'(?<=LEAVE) (?P<address_leave>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+)|' \
                       r'(?<=LEAVE)(?P<leave_resp>OK) (?P<error_code_leave>-?\d+)|' \
                       r'(?<=SER) (?P<address_search>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) "(?P<search_string>.*?)" (?P<search_uid_req>[a-fA-F0-9\-]{36})? *(?P<hops>\d+)|' \
                       r'(?<=SER)(?P<ser_resp>OK) (?P<node_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) (?P<search_uid_resp>[a-fA-f0-9\-]{36})? ?(?P<error_code_search>\d+)( (?P<hops_response>\d+)(?P<filename>( ".*?"){0,}))?|' \
                       r'(?<=UPFIN) (?P<upfin_type>[01]) (?P<upfin_node_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) (?P<ip_hash>[A-Za-z0-9\-]+)|' \
                       r'(?<=UPFIN)(?P<upfin_resp>OK) (?P<error_code_upfin>-?\d+)|' \
                       r'(?<=GETKY) (?P<getkey_key>[a-zA-Z0-9]+)|' \
                       r'(?<=GETKY)(?P<getky_resp>OK) (?P<get_key_resp_num>\d+) (?P<getkey_client_details>( *\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+ [0-9a-zA-Z]+ [a-zA-Z0-9]+)+)|' \
                       r'(?<=GIVEKY) (?P<givekey_resp_num>\d+) (?P<givekey_client_details>( *\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+ [0-9a-zA-Z]+ [a-zA-Z0-9]+)+)|' \
                       r'(?<=GIVEKY)(?P<giveky_resp>OK) (?P<givekey_key>[a-zA-Z0-9]+)|' \
                       r'(?<=ADD) (?P<add_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) (?P<add_key>[a-zA-Z0-9_]+) (?P<add_entry>[a-zA-Z0-9_]+)|' \
                       r'(?<=ADD)(?P<add_resp>OK) (?P<error_code_add>-?\d+)|' \
                       r' (?P<unspecified_data>.*)' \
                       r')'

        response_validate = re.search(regex_string, data)
        if response_validate is None:
            logging.error('Invalid Request.Data: %s' % (data))
            return None

        response_type = response_validate.group(1)
        response = {}

        if response_type == 'REG':
            response['type'] = response_type
            if response_validate.group('reg_resp') == 'OK':
                response['is_response'] = True
                response['username'] = response_validate.group('username_reg')
                response['error_code'] = int(response_validate.group('error_code_reg'))
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group('client_list_reg') if response_validate.group(
                                                     'client_list_reg') is not None else '')
            else:
                response['is_response'] = False
                response['username'] = response_validate.group('reg_username')
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group('reg_address') if response_validate.group(
                                                     'reg_address') is not None else '')
        elif response_type == 'DEL':
            if response_validate.group('del_resp') == 'OK':
                response['type'] = response_type
                response['username'] = response_validate.group('username_del')
                response['error_code'] = int(response_validate.group('error_code_del'))
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group('client_list_del') if response_validate.group(
                                                     'client_list_del') is not None else '')


        elif response_type == 'BS':
            response['type'] = response_type
            response['error_code'] = int(response_validate.group('error_code_bs'))
        elif response_type == 'GET':
            response['type'] = response_type
            if response_validate.group('get_resp') == 'OK ':
                response['is_response'] = True
                response['username'] = response_validate.group('username_get')
                response['error_code'] = int(response_validate.group('client_count'))
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group('client_list_get') if response_validate.group(
                                                     'client_list_get') is not None else '')
            else:
                response['response_flag'] = False
                response['username'] = response_validate.group('username_get')
        elif response_type == 'JOIN':
            response = {}
            if response_validate.group('join_resp') == 'OK':
                response['response_flag'] = True
                response['type'] = response_type
                response['error_code'] = int(response_validate.group('error_code_join'))
            else:
                response['response_flag'] = False
                response['type'] = response_type
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group('address_join') if response_validate.group(
                                                     'address_join') is not None else '')
        elif response_type == 'LEAVE':
            response = {}
            response['type'] = response_type
            if response_validate.group('leave_resp') == 'OK':
                response['response_flag'] = True
                response['error_code'] = int(response_validate.group('error_code_leave'))
            else:
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group('address_leave') if response_validate.group(
                                                     'address_leave') is not None else '')
        elif response_type == 'SER':
            response = {}
            response['type'] = response_type
            if response_validate.group('ser_resp') == 'OK':
                response['response_flag'] = True
                response['error_code'] = int(response_validate.group('error_code_search'))
                if response_validate.group('hops_response'):
                    response['hops'] = int(response_validate.group('hops_response'))
                response['source_address'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                        response_validate.group(
                                                            'node_address') if response_validate.group(
                                                            'node_address') is not None else '')
                response['search_id'] = response_validate.group('search_uid_resp') if response_validate.group(
                    'search_uid_resp') is not None else str(uuid.uuid4())

                if response_validate.group('filename') is not None:
                    response['filename'] = re.findall(r'"(.*?)"', response_validate.group('filename'))

            else:
                response['response_flag'] = False
                response['source_address'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                        response_validate.group(
                                                            'address_search') if response_validate.group(
                                                            'address_search') is not None else '')
                response['search_string'] = response_validate.group('search_string')
                response['hops'] = int(response_validate.group('hops'))
                response['search_id'] = response_validate.group('search_uid_req') if response_validate.group(
                    'search_uid_req') is not None else str(uuid.uuid4())
        elif response_type == 'UPFIN':
            response['type'] = response_type
            if response_validate.group('upfin_resp') == 'OK':
                response['is_response'] = True
                response['error_code'] = response_validate.group('error_code_upfin')
            else:
                response['is_response'] = False
                response['hash'] = response_validate.group('ip_hash')
                response['is_leaving'] = True if response_validate.group('upfin_type') == 1 else False
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group(
                                                     'upfin_node_address') if response_validate.group(
                                                     'upfin_node_address') is not None else '')
        elif response_type == 'GETKY':
            response['type'] = response_type
            if response_validate.group('getky_resp') == 'OK':
                response['is_response'] = True
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group(
                                                     'getkey_client_details') if response_validate.group(
                                                     'getkey_client_details') is not None else '')
                response['keymap'] = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+ ([a-zA-Z0-9]+) ([a-zA-Z0-9]+)',
                                                response_validate.group(
                                                    'getkey_client_details') if response_validate.group(
                                                    'getkey_client_details') is not None else '')
            else:
                response['is_response'] = False
                response['key'] = response_validate.group('getkey_key')
        elif response_type == 'GIVEKY':
            response['type'] = response_type
            if response_validate.group('giveky_resp') == 'OK':
                response['is_response'] = True
                response['key'] = response_validate.group('givekey_key')
            else:
                response['is_response'] = False
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group(
                                                     'givekey_client_details') if response_validate.group(
                                                     'givekey_client_details') is not None else '')
                response['keymap'] = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+ ([a-zA-Z0-9]+) ([a-zA-Z0-9]+)',
                                                response_validate.group(
                                                    'givekey_client_details') if response_validate.group(
                                                    'givekey_client_details') is not None else '')
        elif response_type == 'ADD':
            response['type'] = response_type
            if response_validate.group('add_resp') == 'OK':
                response['is_response'] = True
                response['error_code'] = response_validate.group('error_code_add')
            else:
                response['clients'] = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)',
                                                 response_validate.group(
                                                     'add_address') if response_validate.group(
                                                     'add_address') is not None else '')

                response['keymap'] = (response_validate.group('add_key'), response_validate.group('add_entry'))
        else:
            response = {}
            response['type'] = response_type
            response['data'] = response_validate.group('unspecified_data')

        # Format IP and Port
        if response.get('clients') is not None:
            response['clients'] = self.format_addresses(response.get('clients'))

        if response.get('source_address') is not None:
            response['clients'] = self.format_addresses(response.get('source_address'))

        return response

    def format_addresses(self, data):
        if data is not None:
            clients = []
            for ip, port in data:
                clients += [(ip, int(port))]
            if len(clients) == 0:
                data = None
            elif len(clients) == 1:
                data = clients[0]
            else:
                data = clients
        return data

    def register_request(self, addr, username):
        ip_address, port = addr
        message = 'REG %s %d %s' % (ip_address, port, username)
        message = self._string_len_prepend(message)
        return message

    def deregister_ip_request(self, addr, username):
        ip_address, port = addr
        message = 'DEL IPADDRESS %s %d %s' % (ip_address, port, username)
        message = self._string_len_prepend(message)
        return message

    def deregister_all(self, username):
        message = 'DEL UNAME %s' % (username)
        message = self._string_len_prepend(message)
        return message

    def list_all(self, username):
        message = 'GET IPLIST %s' % (username)
        message = self._string_len_prepend(message)
        return message

    def _string_len_prepend(self, string):
        return '%s %s' % (str(len(string)).zfill(3), string)

    def leave_request(self, address):
        ip, port = address
        return self._string_len_prepend('LEAVE %s %s' % (ip, port))

    def leave_response(self, error_code):
        return self._string_len_prepend('LEAVEOK %d' % (error_code))

    def join_request(self, address):
        ip, port = address
        return self._string_len_prepend('JOIN %s %s' % (ip, port))

    def join_response(self, error_code):
        return self._string_len_prepend('JOINOK %d' % (error_code))

    def update_finger_request(self, type, address, key):
        ip, port = address
        return self._string_len_prepend('UPFIN %d %s %d %s' % (type, ip, port, key))

    def update_finger_response(self, err_code):
        return self._string_len_prepend('UPFINOK %d' % (err_code))

    def get_key_request(self, key):
        return self._string_len_prepend('GETKY %s' % key)

    def get_key_response(self, addresses, keymap):
        data = ''
        for i in range(len(addresses)):
            temp = (addresses[i] + keymap[i])
            temp = ' '.join([str(i) for i in temp])
            data += ' ' + temp
        return self._string_len_prepend('GETKYOK %d%s' % (len(addresses), data))

    def give_key_request(self, addresses, keymap):
        data = ''
        for i in range(len(addresses)):
            temp = (addresses[i] + keymap[i])
            temp = ' '.join([str(i) for i in temp])
            data += ' ' + temp
        return self._string_len_prepend('GIVEKY %d%s' % (len(addresses), data))

    def give_key_response(self, err_code):
        return self._string_len_prepend('GIVEKYOK %d' % (err_code))

    def add_request(self, address, keymap):
        ip, port = address
        key, entry = keymap
        return self._string_len_prepend('ADD %s %d %s %s' % (ip, port, key, entry))

    def add_response(self, err_code):
        return self._string_len_prepend('ADDOK %s' % (err_code))

    def search_request(self, ip, port, filename, uid, hops):
        return self._string_len_prepend('SER %s %d "%s" %s %d' % (ip, port, filename, uid, hops))

    def search_response(self, ip, port, error_code, uid, filename=None, hops=0):
        if filename is not None and len(filename) > 0 and error_code >= 0:
            file_concat = ""
            error_code = len(filename)
            for filex in filename:
                file_concat += '"%s" ' % filex
            file_concat = file_concat[0:-1]
            return self._string_len_prepend('SEROK %s %d %s %d %d %s' % (ip, port, uid, error_code, hops, file_concat))
        else:
            return self._string_len_prepend('SEROK %s %d %s %d' % (ip, port, uid, error_code))

    def unknown_request(self, error_code):
        return self._string_len_prepend('UNKNOWN %d' % (error_code))
