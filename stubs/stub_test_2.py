# from BootstrapServer import BootstrapServer, BSDeleteError
# import re
# import sys
# import time
# from PeerClient import PeerClient

# serv = BootstrapServer(ip_list_file='bs_list.txt')
# serv.set_username('ALPHA')
# serv.set_server(3)
#
#
# try:
#     serv.deregister_all()
# except BSDeleteError:
#     pass
#
# print serv.register('127.0.0.1', 10075)
# print serv.register('127.0.0.1', 10076)
# print serv.register('127.0.0.1', 10077)
# print serv.register('127.0.0.1', 10078)
# print serv.register('127.0.0.1', 10079)
# print serv.register('127.0.0.1', 10051)
# print serv.register('127.0.0.1', 10052)
# # print serv.register('127.0.0.1', 10053)
# #
# # print serv.deregister_ip('127.0.0.1', 10053)
# #
# # print serv.deregister_all()


# peer = PeerClient('ALPHA', server_index=2, port=10001)
#
# try:
#     peer.unregister()
# except BSDeleteError:
#     pass
#
#
# peer.register()
#
# peer._read_thread()
#
# while True:
#     time.sleep(10)
#
#
# peer.unregister()

# peer.bootstrap_register()


# print peer._set_response('JOIN 127.0.0.1 10001')


# from PeerProtocol import PeerProtocol
# import uuid
#
# pp = PeerProtocol()
#
# print pp.search_request('127.0.0.1', 89884, 'Hello', uuid.uuid4(), 0)
# print pp.parse_request('066 SER 127.0.0.1 89884 "Hello" 0')

# import redis
# import time
#
# r = redis.Redis(
#     host='redis.varunbhat.in',
#     port=6379
# )

# if not r.hexists('global_clients','time'):
#     print r.hset('global_clients', 'hello','world')
# else:
#     print r.hset('global_clients', 'time_is_money', time.time() )
#
# data = r.hgetall('global_clients')
# print data
# data['time_is_money'] = time.time()
# print r.hmset('global_clients',data)
# print r.hgetall('global_clients')
#
# print r.hget('global_clients','time_sis_money')
#
# print r.hmget('globals_clients','wassup','chunky')
#
# p = r.pipeline()
# p.hsetnx('global_clients', 'client_index', 0L)
# p.hget('global_clients', 'client_index')
#
# print p.execute()

# r.sadd('hello',*[1,2,3,4])

# print r.smembers('hello')
# print r.hsetnx('global_clients', 'time', 'asdf')
# print r.hdel('global_clients', 'time')

import networkx as nx
import matplotlib.pyplot as plt
import scipy.special as sps
import numpy as np



s = np.arange(1., 60.)
a = .8
# y = x ** (-a) / sps.zetac(a)
#
# plt.clf()
# plt.plot(y, x)
# plt.savefig('zipfs.png')

plt.clf()
count, bins, ignored = plt.hist(s[s<50], 50, normed=True)
x = np.arange(1., 160.)
y = x**(-a)/sps.zetac(a)
plt.plot(x, y/max(y), linewidth=2, color='r')
plt.savefig('8zipfs.png')