import hashlib
import logging
import math


class Chord:
    NODE_ID = None
    id_space = ()
    finger_table = {}
    clientlist = []
    node_addressmap = {}
    successor = {}
    predecessor = {}
    node_filemap = {}
    peer_filemap = []

    _NODE_COUNT = 0

    def __init__(self, address, m):
        self._NODE_COUNT_MANTISSA = int(math.ceil(math.log(m, 2)))
        self.NODE_ID = self.generate_id(address)
        self.NODE_ID = self.generate_id(address)

    def generate_id(self, address):
        return int(hashlib.sha1('%s:%d' % address).hexdigest()[0:int(math.ceil(self._NODE_COUNT_MANTISSA / 4.0))], 16)

    def generate_file_id(self, filename):
        return int(hashlib.sha1(filename).hexdigest()[0:int(math.ceil(self._NODE_COUNT_MANTISSA / 4.0))], 16)

    def get_nodeid(self):
        return self.NODE_ID

    def get_finger_table(self):
        return self.finger_table

    def get_span(self):
        return self.id_space

    def add_node(self, address):
        self.initialize_range(self.node_addressmap.values() + [address])

    def delete_node(self, address):
        del_id = self.generate_id(address)
        del self.node_addressmap[del_id]
        self.initialize_range(self.node_addressmap.values())

    def initialize_range(self, clientlist):
        if type(clientlist) == tuple:
            self.clientlist = [clientlist]
        else:
            self.clientlist = clientlist

        for client in self.clientlist:
            self.node_addressmap[self.generate_id(client)] = client

        ids = self.node_addressmap.keys()
        ids.sort()

        self.id_space = (ids[ids.index(self.NODE_ID) - 1] + 1, self.NODE_ID + 1)

        self.successor = {ids[(ids.index(self.NODE_ID) + 1) % len(ids)]: self.node_addressmap[
            ids[(ids.index(self.NODE_ID) + 1) % len(ids)]]}
        self.predecessor = {ids[ids.index(self.NODE_ID) - 1]: self.node_addressmap[ids[ids.index(self.NODE_ID) - 1]]}

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

    def get_successor(self):
        return self.successor.values()[0]

    def get_predecessor(self):
        return self.predecessor.values()[0]

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
        self.peer_filemap.append((address, (key,filename)))
        self.peer_filemap = list(set(self.peer_filemap))

    def generate_finger_table(self):
        ids = self.node_addressmap.keys()
        ids.sort()

        ids_ov = ids + [(2 ** self._NODE_COUNT_MANTISSA) + i for i in ids]

        for k in range(self._NODE_COUNT_MANTISSA + 1):
            finger_theoritical = ((self.NODE_ID + 2 ** k) - 1) % (2 ** self._NODE_COUNT_MANTISSA)
            for i in ids_ov:
                if finger_theoritical <= i:
                    break
            self.finger_table[k] = self.node_addressmap[i % ((2 ** self._NODE_COUNT_MANTISSA))]
