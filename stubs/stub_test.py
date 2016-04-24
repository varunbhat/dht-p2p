# from BootstrapServer import BootstrapServer, BSDeleteError
# import re
# import sys
# import time
# from PeerClient import PeerClient
# import logging
# import requests
# import socket
#
# bs_index = 1
#
# serv = BootstrapServer(ip_list_file='bs_list.txt')
# serv.set_username('ALPHA')
#
#
# for i in range(12):
#     serv.set_server(i)
#     try:
#         serv.deregister_all()
#     except BSDeleteError:
#         print 'Working.' ,serv.get_address()
#     except socket.timeout:
#         print 'Timedout:',serv.get_address()
#
# print serv.register('127.0.0.1', 10075)
# print serv.register('127.0.0.1', 10076)
# print serv.register('127.0.0.1', 10077)
# print serv.register('127.0.0.1', 10078)
# print serv.register('127.0.0.1', 10079)
# print serv.register('127.0.0.1', 10051)
# print serv.register('127.0.0.1', 10052)
# print serv.register('127.0.0.1', 10053)
#
# print serv.deregister_ip('127.0.0.1', 10053)

# print serv.deregister_all()
#
# logging.basicConfig(level=logging.INFO, format='[%(asctime)-15s %(levelname)s %(thread_name)s] %(message)s', )
# logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s] %(message)s', )
# logging.basicConfig(filename='server.log', level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s] %(message)s' )
#
# if __name__ == '__main__':
#     # peer = PeerClient('ALPHA', server_index=bs_index, port=int(sys.argv[1]), address='127.0.0.1')
#     peer = PeerClient('ALPHA', server_index=bs_index, port=int(sys.argv[1]))
#
#     try:
#         peer.unregister()
#     except BSDeleteError:
#         pass
#
#     peer.register()
#     peer.join_network()


# class asdfa:
#     def __init__(self):
#         pass
#
# a_2 = asdfa()
#
#
#
# class tssdf(object):
#     def __init__(self):
#         resp = {'test':1}
#         self.resobj = type('test', (object,), dict(resp))()
#
#     def asdf(self):
#         return self.resobj
#
# asdd = tssdf()
# print type(asdd.asdf())
# response = {}
# response['type'] = 'ts'
# response['error_code'] = 1
#
# response_obj = type('bootstrap_response',(dict,), dict())()
#
# response_obj.update(response)
#
# print response.type


# class Myclass:
#     events = {}
#     def on(self,tag_name):
#         def event_processor(func):
#             self.events[tag_name] = func
#             return func
#         return event_processor
#
#     def show(self):
#         print self.events['start']('varun')
#
#
# myclass = Myclass()
#
# @myclass.on("start")
# def get_text(name):
#     return "Hello "+name
#
# myclass.show()



# <length> SER IP port <file_name> <hops>

# re_search = re.search( r'(JOIN|LEAVE|SER)(' \
#                        r'(?<=JOIN)OK (?P<error_code_join>-?\d+)|' \
#                        r'(?<=LEAVE)OK (?P<error_code_leave>-?\d+)|' \
#                        r'(?<=SER)(?P<ser_resp>OK) (?P<node_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) (?P<error_code_search>\d+) (?P<hops_response>\d+) (?P<filename>( ".*?"){0,})|' \
#                        r')', 'SEROK 127.0.0.1 10020 1 "Helo" 3')
# # SEROK 127.0.0.1 10020 1 "Helo" 3
#
# print re_search.groups()
#
# import re
#
# data = open('../resources.txt','r').read()
# data = re.findall(r'^[^\#](.*)',data,re.MULTILINE)
# print data

# from KilenjeNataraj_VarunBhat_Lab03.DatabaseFunctions import *
# import peewee
#
# try:
#     db.create_tables([IncomingClients,OutgoingClients])
# except peewee.OperationalError:
#     pass
#     # print "Operational Error, Assuming Database already exists."
#
# IncomingClients.create(ip='123.1.1.1',port=11111)

# for client in IncomingClients.select():
#     print client.ip,client.port
#     client = IncomingClients.get(ip=client.ip,port=client.port)
#     print client.ip,client.port
#     print client.delete_instance()
#     try:
#         client = IncomingClients.get(ip=client.ip,port=client.port)
#     except:
#         print "does not exist"
import time

import re

# import random
# from KilenjeNataraj_VarunBhat_Lab03.DatabaseFunctions import *
# # from peewee import fn
#
# db.create_tables([FileTable, IncomingClients, OutgoingClients])
#
# def read_resource_txt():
#     data = open('../resources.txt', 'r').read().replace('\r', '').split('\n')
#     search_list = []
#     count = 1
#     for index in range(len(data)):
#         if len(data[index]) > 0 and data[index][0] != '#':
#             search_list.append(data[index])
#
#     return search_list
#
# def select_random_files(file_list,length):
#     selected_files = []
#     for i in range(length):
#         selected_files.append(file_list.pop(int(random.random() * 1000)%len(file_list)))
#
#     for i in range(len(selected_files)):
#         FileTable.create(filename=selected_files[i], index=i,file_exists_on_node_flag=True)
#
#     return selected_files
#
# select_random_files(read_resource_txt(),160)
#
# # for filex in FileTable.select().where(FileTable.file_exists_on_node_flag==True):
# #     filex.filename
#
#
#
# for q in FileTable.select().where(FileTable.filename.contains('spr')):
#     print q.filename

#
# data = re.search(r'(JOIN|LEAVE|SER|[A-Z]+)(' \
#                        r'(?<=JOIN) (?P<address_join>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+)|' \
#                        r'(?<=LEAVE) (?P<address_leave>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+)|' \
#                        r'(?<=SER) (?P<address_search>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) "(?P<search_string>.*)" (?P<hops>\d+)|' \
#                        r'(?<=SER)(?P<ser_resp>OK) (?P<node_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+) (?P<error_code_search>\d+)( (?P<hops_response>\d+)(?P<filename>( ".*?"){0,}))?|' \
#                        r' (?P<unspecified_data>.*)' \
#                        r')','SEROK 127.0.0.1 12552 0')
#
# print data.groups()



# import socket
#
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# from DatabaseFunctions import *
# import peewee
# import logging
#
# try:
#     db.create_tables([FileTable, IncomingClients, OutgoingClients, SearchResults, SearchRequests])
# except peewee.OperationalError:
#     logging.warn('Assuming Clients Database already exists.')
#
# OutgoingClients.create(ip='127.0.0.1', port=8558)
#
# for client in OutgoingClients.select():
#     print client.ip,client.port


# import networkx as nx
# import matplotlib.pyplot as plt
# from BootstrapProtocol import BootstrapProtocol
# import socket
# import json
# import numpy as np
# import random
#
# from PeerProtocol import PeerProtocol
#
# bp = BootstrapProtocol('ALPHA')
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
#
# def send(data, address, response=True):
#     sock.sendto(data, address)
#     if response:
#         data = sock.recv(100000000)
#         return data
#     else:
#         return None
#
#
# def read_resource_txt():
#     data = open('resources.txt', 'r').read().replace('\r', '').split('\n')
#     search_list = []
#     count = 1
#     for index in range(len(data)):
#         if len(data[index]) > 0 and data[index][0] != '#':
#             search_list.append(data[index])
#
#     return search_list
#
#
# def get_clients():
#     return bp.parse_response(send(bp.list_all(), ("129.82.46.191", 10000)))['clients']
#
#
# def get_network_config(clients):
#     G = nx.DiGraph()
#     for node in clients:
#         G.add_node(node, addr=str(node))
#
#     for client in clients:
#         resp = send('LISTO', client)
#         resp = json.loads(resp)
#         peers = resp['clients']
#         edge = [(client, tuple(peer)) for peer in peers]
#         G.add_edges_from(edge)
#     return G
#
#
# def node_degree(graph):
#     degree = []
#     for client in graph.nodes():
#         degree.append(len(graph.predecessors(client)))
#     return sum(degree) / float(len(degree))
#
#
# def get_graph(graph, filename='test.png'):
#     nx.draw_circular(graph)
#     plt.savefig(filename)
#     plt.show()
#
#
# def set_file_count(clients, value):
#     for client in clients:
#         send('SET_FILE_COUNT ' + str(value), client)
#
#
# def get_files(clients):
#     result = []
#     for client in clients:
#         resp = send('GET_FILES', client)
#         resp = json.loads(resp)
#         result.append(resp['files'])
#     return result
#
#
# def plot_file_distribution(resources, file_distribution, filename):
#     count = [0 for i in range(len(resources))]
#
#     for node_fil_arr in file_distribution:
#         for lfile in node_fil_arr:
#             count[resources.index(lfile)] += 1
#
#     plt.clf()
#     y_pos = np.arange(len(resources))
#     plt.bar(y_pos, count, align='center', alpha=0.5)
#     # plt.xticks(y_pos, resources)
#     plt.ylabel('Number of Nodes')
#     plt.title('File Distribution')
#     plt.savefig(filename)
#
#     plt.show()
#     pass
#
#
# def execute_search(resources, clients, ns):
#     pp = PeerProtocol()
#     for i in range(ns):
#         for filex in resources:
#             index = int(random.random() * 1000) % len(clients)
#             ip, port = clients[index]
#             send(pp.search_request(ip, port, filex, 0), clients[index], response=False)
#             time.sleep(.5)
#
#
# def calculate_1(clients):
#     hops = []
#     latency = []
#     msg_count = []
#     for client in clients:
#         resp = json.loads(send('SEARCH_RESULTS', client))
#         filename, start_time = [], []
#         for name, timex, hop in resp['requests']:
#             filename.append(name), start_time.append(timex)
#         for res in resp['results']:
#             name = res[0][2:-2]
#             tx = start_time[filename.index(name)]
#             hops.append(res[1])
#             latency.append(abs(res[2] - tx))
#
#         msg_count.append(len(resp['results']) + len(resp['requests']))
#     print "Hops     :", "Min:", min(hops), "Max:", max(hops), "average:", sum(hops) / float(len(hops)), "SD:", np.std(
#         hops)
#     print "Latency  :", "Min:", min(latency), "Max:", max(latency), "average:", sum(latency) / float(
#         len(latency)), "SD:", np.std(latency)
#     print "Msg Count:", "Min:", min(msg_count), "Max:", max(msg_count), "average:", sum(msg_count) / float(
#         len(msg_count)), "SD:", np.std(
#         msg_count)
#
#
# def calculate_2(clients, resources):
#     a = 2.
#     dist = np.random.zipf(a, len(resources))
#     dist = np.sort(dist)
#     plt.clf()
#     plt.plot(dist, range(len(resources)))
#     plt.savefig('zipfs.png')
#     plt.show()
#
#
# if __name__ == '__main__':
#     clients = get_clients()
#     print "Number of Nodes:", len(clients)
#     graph = get_network_config(clients)
#
#     degree = []
#     for client in graph.nodes():
#         degree.append(len(graph.predecessors(client)))
#     nd1 = sum(degree) / float(len(degree))
#
#     print "Node Degree:", nd1
#     get_graph(graph, str(len(clients)) + '_config.png')
#     if len(clients) >= 80:
#         set_file_count(clients, 2)
#     elif len(clients) >= 40:
#         set_file_count(clients, 4)
#     else:
#         set_file_count(clients, 8)
#
#     resources = read_resource_txt()
#     file_arr = get_files(clients)
#     plot_file_distribution(resources, file_arr, str(len(clients)) + '_file_distribution.png')
#     execute_search(resources, clients, 1)
#     calculate_1(clients)
#     calculate_2(clients, resources)



import hashlib, uuid

print uuid.NAMESPACE_DNS

print uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
