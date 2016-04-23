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

    def get_peer_filemap(self,key=None):
        if key == None:
            return self.peer_filemap
        else:
            retval = []
            for addr,(id,file) in self.peer_filemap:
                if  id > key:
                    continue
                retval.append((addr,(id,file)))
            return retval

    def get_successor(self):
        return self.successor.values()[0]

    def get_predecessor(self):
        return self.predecessor.values()[0]

    def get_max_dist_address(self, fileid):
        val = fileid - self.NODE_ID + 1 + (
            2 ** self._NODE_COUNT_MANTISSA) if fileid - self.NODE_ID + 1 < 0 else fileid - self.NODE_ID + 1

        n = int(math.floor(math.log(val, 2)))
        if len(self.finger_table) > 0:
            return self.finger_table[n]

    def initialize_files(self, file_list):
        for filex in file_list:
            fileid = self.generate_file_id(filex)
            self.node_filemap[fileid] = filex

    def in_range(self, key):
        minval, maxval = self.id_space

        key = (key - minval) % (2 ** self._NODE_COUNT_MANTISSA)
        maxval = (maxval - 1 - minval) % (2 ** self._NODE_COUNT_MANTISSA)
        minval -= minval

        if key >= 0 and key <= maxval:
            return True
        else:
            return False

    def peer_file_add(self, key, filename, address):
        self.peer_filemap.append((address,(key,filename)))

        # if self.peer_filemap.get(key) is not None:
        #     self.peer_filemap[key].append((filename, address))
        # else:
        #     self.peer_filemap[key] = [(filename, address)]

    def generate_finger_table(self):
        ids = self.node_addressmap.keys()
        ids.sort()

        ids_ov = ids + [(2 ** self._NODE_COUNT_MANTISSA) + i for i in ids]

        for k in range(self._NODE_COUNT_MANTISSA + 1):
            finger_theoritical = ((self.NODE_ID + 2 ** k) - 1) % (2 ** self._NODE_COUNT_MANTISSA)
            for i in ids_ov:
                if finger_theoritical <= i:
                    break

            self.finger_table[k] = self.node_addressmap[i % (2 ** self._NODE_COUNT_MANTISSA)]
