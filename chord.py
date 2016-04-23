import hashlib
import math


class Chord:
    NODE_ID = None
    id_space = ()
    finger_table = {}
    clientlist = []
    node_addressmap = {}
    successor = None
    predecessor = None
    node_filemap = {}
    peer_filemap = {}

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

    def get_peer_list(self):
        return list(set(self.finger_table.values()))

    def add_node(self, address):
        self.initialize_range(self.node_addressmap.values() + [address])

    def delete_node(self, address):
        del_id = self.generate_id('%s:%d' % address)
        del self.node_addressmap[del_id]
        self.initialize_range(self.node_addressmap.values())

    def initialize_range(self, clientlist):
        id_list = {}

        if type(clientlist) == tuple:
            self.clientlist = [clientlist]
        else:
            self.clientlist = clientlist

        for client in self.clientlist:
            id_list[client] = self.generate_id(client)

        self.node_addressmap = {v: k for k, v in id_list.items()}

        ids = id_list.values()
        ids.sort()

        self.id_space = (ids[ids.index(self.NODE_ID) - 1] + 1, self.NODE_ID + 1)

        self.successor = ids[(ids.index(self.NODE_ID) + 1) % len(ids)]
        self.predecessor = ids[ids.index(self.NODE_ID) - 1]

        self.generate_finger_table()

        return self.id_space

    def get_node_filemap(self):
        return self.node_filemap

    def get_peer_filemap(self):
        return self.peer_filemap

    def get_successor(self):
        return self.successor.values()[0]

    def initialize_files(self, file_list):
        for filex in file_list:
            self.node_filemap[self.generate_file_id(filex)] = filex

    def generate_finger_table(self):
        ids = self.node_addressmap.keys()
        ids.sort()

        ids_ov = ids + [(2 ** self._NODE_COUNT_MANTISSA) + i for i in ids]

        for k in range(self._NODE_COUNT_MANTISSA):
            finger_theoritical = ((self.NODE_ID + 2 ** k) + 1) % (2 ** self._NODE_COUNT_MANTISSA)
            for i in ids_ov:
                if finger_theoritical <= i:
                    break
            self.finger_table[i % (2 ** self._NODE_COUNT_MANTISSA)] = self.node_addressmap[
                i % (2 ** self._NODE_COUNT_MANTISSA)]
