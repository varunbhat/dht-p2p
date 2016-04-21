import hashlib
import math


class Chord:
    NODE_NEIGHBOURS = {'predecessor': None, 'successor': None}
    NODE_ID = None
    NODE_FINGER_TABLE = {}
    INV_NODE_FINGER_TABLE = {}
    _NODE_COUNT = 0

    def __init__(self, address, m):
        self._NODE_COUNT_MANTISSA = int(math.ceil(math.log(m, 2)))
        self.NODE_ID = self.generate_id(address)

    def generate_id(self, address):
        return int(hashlib.sha1('%s:%d' % address).hexdigest()[0:int(math.ceil(self._NODE_COUNT_MANTISSA / 4.0))], 16)

    def get_nodeid(self):
        return self.NODE_ID

    def get_finger_table(self):
        return self.INV_NODE_FINGER_TABLE

    def get_peer_list(self):
        return list(set(self.INV_NODE_FINGER_TABLE.values()))

    def generate_finger_table(self, clientlist):
        id_list = {}
        finger = []

        for client in clientlist:
            str_client = '%s:%d' % (client)
            id_list[str_client] = self.generate_id(client)

        ids = id_list.values()
        ids.sort()

        ids_ov = ids + [(2 ** self._NODE_COUNT_MANTISSA) + i for i in ids]

        for k in range(self._NODE_COUNT_MANTISSA):
            finger_theoritical = (self.NODE_ID + 2 ** k) % (2 ** self._NODE_COUNT_MANTISSA)
            for i in ids_ov:
                if finger_theoritical < i:
                    break
            finger.append(i % (2 ** self._NODE_COUNT_MANTISSA))

        self.NODE_FINGER_TABLE = finger
        inv_id_list = {v: k for k, v in id_list.items()}
        self.INV_NODE_FINGER_TABLE = {i: inv_id_list[i].split(':') for i in finger}
        self.INV_NODE_FINGER_TABLE = {k: (v[0],int(v[1]))  for k,v in self.INV_NODE_FINGER_TABLE.items()}


