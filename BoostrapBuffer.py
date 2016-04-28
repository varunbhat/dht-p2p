import hashlib
import math

class BootstrapBuffer:

    def __init__(self):
        self.addressmap = {}
        self.node_exponent = (2**(4*20))

    def search_addressmap(self,key):
        keys = self.addressmap.keys()
        keys.sort()
        ranges = [(keys[i-1],(keys[i]+1)*self.node_exponent) for i in range(1,len(keys))]
        for range in ranges:
            if self.in_range(key,range):
                return self.addressmap[i]

    def in_range(self, key, key_range=None):
        if key_range == None:
            minval, maxval = self.id_space
        else:
            minval, maxval = key_range

        key = (key - minval) % (2 ** self.node_exponent)
        maxval = (maxval - 1 - minval) % (2 ** self.node_exponent)
        minval -= minval

        if key >= 0 and key <= maxval:
            return True
        else:
            return False

    def add_addressmap(self,key,value):
        self.addressmap[key] = value

    def generate_key(self, address):
        hash_inp = address.encode('utf8')
        return int(hashlib.sha1(hash_inp).hexdigest()[0:int(math.ceil(self.node_exponent / 4.0))], 16)