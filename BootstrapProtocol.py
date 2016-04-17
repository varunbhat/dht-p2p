import re
import logging
import uuid


class ProtocolHandler:
    def parse_response(self, data):
        regex_string = r'(REG|DEL|BS|GET|JOIN|LEAVE|SER|[A-Z]+)(' \
                       r'(?<=REG)(?P<reg_address>( \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+)+) (?P<reg_username>[^0-9_][A-Za-z_0-9]+)|' \
                       r'(?<=REG)(?P<reg_resp>OK) ((?P<username_reg>[^0-9_][A-Za-z_0-9]+) )?(?P<error_code_reg>-?\d+)(?P<client_list_reg>( \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+){0,3})|' \
                       r'(?<=DEL) (IPADDRESS|UNAME)? *OK *(?P<username_del>[^0-9_][A-Za-z_0-9]+)? *(?P<client_list_del>( *\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+){0,3}) *(?P<error_code_del>-?\d+)|' \
                       r'(?<=BS) REQ (?P<error_code_bs>-?\d+)|' \
                       r'(?<=GET) IPLIST (?P<get_resp>OK )?(?P<username_get>[^0-9_][A-Za-z_0-9]+) ?(?P<client_count>\d+)? *(?P<client_list_get>( *\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+)+)?|' \
                       r'(?<=JOIN) (?P<address_join>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+)|' \
                       r'(?<=JOIN)(?P<join_resp>OK) (?P<error_code_join>-?\d+)|' \
                       r'(?<=LEAVE) (?P<address_leave>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+)|' \
                       r'(?<=LEAVE)(?P<leave_resp>OK) (?P<error_code_leave>-?\d+)|' \
                       r'(?<=SER) (?P<address_search>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) "(?P<search_string>.*?)" (?P<search_uid_req>[a-fA-F0-9\-]{36})? *(?P<hops>\d+)|' \
                       r'(?<=SER)(?P<ser_resp>OK) (?P<node_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) (?P<search_uid_resp>[a-fA-f0-9\-]{36}) (?P<error_code_search>\d+)( (?P<hops_response>\d+)(?P<filename>( ".*?"){0,}))?|' \
                       r' (?P<unspecified_data>.*)' \
                       r')'

        response_validate = re.search(regex_string, data)
        if response_validate is None:
            logging.error('Invalid Request.')
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
            if response_validate.group('ser_resp') == 'OK':
                response['response_flag'] = True
                response['type'] = response_type
                response['error_code'] = int(response_validate.group('error_code_leave'))
            else:
                response['type'] = response_type
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

    def register_request(self, ip_address, port):
        message = 'REG %s %d %s' % (ip_address, port, self.username)
        message = self._string_len_prepend(message)
        return message

    def deregister_ip_request(self, ip_address, port):
        message = 'DEL IPADDRESS %s %d %s' % (ip_address, port, self.username)
        message = self._string_len_prepend(message)
        return message

    def deregister_all(self, username):
        message = 'DEL UNAME %s' % (username)
        message = self._string_len_prepend(message)
        return message

    def list_all(self):
        message = 'GET IPLIST %s' % (self.username)
        message = self._string_len_prepend(message)
        return message

    def _string_len_prepend(self, string):
        return '%s %s' % (str(len(string)).zfill(3), string)

    def leave_request(self, ip, port):
        return self._string_len_prepend('LEAVE %s %s' % (ip, port))

    def leave_response(self, error_code):
        return self._string_len_prepend('LEAVEOK %d' % (error_code))

    def join_request(self, ip, port):
        return self._string_len_prepend('JOIN %s %s' % (ip, port))

    def join_response(self, error_code):
        return self._string_len_prepend('JOINOK %d' % (error_code))

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
