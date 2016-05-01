import math

import hashlib


class Chord:
    NODE_ID = None
    id_space = (0, 0)
    finger_table = {}
    node_addressmap = {}
    successor = {}
    predecessor = {}
    node_filemap = {}
    peer_filemap = []

    _NODE_COUNT = 0

    def __init__(self, m=(2 ** (4 * 20))):
        self._NODE_COUNT_MANTISSA = int(math.ceil(math.log(m, 2)))
        self.mod_val = 2**self._NODE_COUNT_MANTISSA

    def generate_key(self, address):
        hash_inp = address.encode('utf8')
        return int(hashlib.sha1(hash_inp).hexdigest()[0:int(math.ceil(self._NODE_COUNT_MANTISSA / 4.0))], 16)

    def get_nodekey(self):
        return self.NODE_ID

    def get_finger_table(self):
        return self.finger_table

    def get_span(self):
        return self.id_space

    def add_node(self, key,addr):
        if self.in_range(key):
            peer_space = (key + 1, self.id_space[1])
            peer_keys = self.get_predecessor_keys(key)
            self.id_space = (key + 1, self.id_space[1])
            return (peer_space, peer_keys)
        elif self.in_range((self.id_space[1],self.successor[0])):
            self.successor = (key,addr)
        elif self.in_range(key,(self.predecessor,self.id_space[1])):
            self.predecessor = (key, addr)

    def delete_node(self, key):
        # find predecessor()
        # self.initialize_range(list(self.node_addressmap.values()))
        pass

    def initialize_range(self, clientlist):
        self.successor = ()
        self.generate_finger_table()

        return self.id_space

    def get_node_filemap(self):
        return self.node_filemap

    def get_peer_filemap(self):
        self.peer_filemap = list(set(self.peer_filemap))
        return self.peer_filemap

    def get_predecessor_keys(self, pred_id):
        retval = []
        space = (self.id_space[0], pred_id)
        for addr, (id, filename) in self.peer_filemap:
            if self.in_range(id, space):
                retval.append((addr, (id, filename)))
        return retval

    def set_nodeid(self, ip_address):
        self.NODE_ID = self.generate_key(ip_address)
        self.id_space = (self.NODE_ID, self.NODE_ID)

    def get_successor(self):
        return list(self.successor.values())[0]

    def get_predecessor(self):
        return list(self.predecessor.values())[0]

    def get_max_dist_address(self, fileid):
        val = (fileid - self.NODE_ID + 1) % (2 ** self._NODE_COUNT_MANTISSA)

        n = int(math.floor(math.log(val, 2)))
        if len(self.finger_table) > 0:
            return self.finger_table[n]

    def initialize_files(self, file_list):
        for filex in file_list:
            fileid = self.generate_file_id(filex)
            self.node_filemap[fileid] = filex

    def in_range(self, key, key_range=None):
        if key_range == None:
            minval, maxval = self.id_space
        else:
            minval, maxval = key_range

        key = (key - minval) % (2 ** self._NODE_COUNT_MANTISSA)
        maxval = (maxval - 1 - minval) % (2 ** self._NODE_COUNT_MANTISSA)
        minval -= minval

        if key >= 0 and key <= maxval:
            return True
        else:
            return False

    def peer_file_del(self, key):
        # logging.debug('Peer Filemap: %s' % str(self.peer_filemap))
        temp = self.peer_filemap
        try:
            for i in range(len(self.peer_filemap)):
                addr, (id, filename) = self.peer_filemap[i]
                if id == key:
                    del temp[i]
        except IndexError:
            pass

        self.peer_filemap = list(set(temp))

    def peer_file_add(self, key, filename, address):
        self.peer_filemap.append((address, (key, filename)))
        self.peer_filemap = list(set(self.peer_filemap))

    def generate_finger_table(self):
        ids = list(self.node_addressmap.keys())
        ids.sort()

        ids_ov = ids + [(2 ** self._NODE_COUNT_MANTISSA) + i for i in ids]

        for k in range(self._NODE_COUNT_MANTISSA + 1):
            finger_theoritical = ((self.NODE_ID + 2 ** k) - 1) % (2 ** self._NODE_COUNT_MANTISSA)
            for i in ids_ov:
                if finger_theoritical <= i:
                    break
            self.finger_table[k] = self.node_addressmap[i % ((2 ** self._NODE_COUNT_MANTISSA))]
