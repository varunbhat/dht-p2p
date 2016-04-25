#!/usr/bin/env python
#Python program for Chord central controller
import socket
import os
import sys
import random
import threading
import time
import string
import signal
import getopt
import re
import json
from time import strftime, gmtime
from utilities import resources


b_ip = None
b_port = 0
controller = None
zipf_s = 0
nw_size = 0
uname = "ALPHA"
hops = {}
latency = {}

class CentralController:
    def __init__(self, bs_ip, bs_port, uname, s):
        self.bootstrap = bs_ip, bs_port, uname
        self.zipf_s = s
        self.nodes = []
        self.server_skt = None
        self.client_skt = None
        self.__init_sockets()
        self.__main_thread_notifier = threading.Event()
        self.__RUN_SERVER = False
        self.__logfile = open('chord_stats.log', 'w')

    def __del__(self):
        del self.nodes[:]
        self.server_skt.close()
        self.__RUN_SERVER = False
        self.s_thread.join(5)
        self.__logfile.close()

    def __init_sockets(self):
        self.server_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.server_skt.bind((host, 0)) # 0 => use any free port
        self.server_skt.listen(5)
        self.myip = socket.gethostbyname(host)
        self.myport = int(self.server_skt.getsockname()[1])
        self.s_thread = threading.Thread(target=self.__server_processor)
        self.s_thread.setDaemon(True)
        self.s_thread.start()

    def __server_processor(self):
        self.__RUN_SERVER = True
        while(self.__RUN_SERVER):
            try:
                cli, addr = self.server_skt.accept()
            except socket.error, e:
                print 'Server Thread: ', e.message
                continue
            # SEROK hops latency num_nodes ip port key entry
            data = cli.recv(3500)
            d = json.loads(data)
            entry = d['entry']
            if entry not in hops:
                hops[entry] = []
            if entry not in latency:
                latency[entry] = []
            hops[entry].append(d['hops'])
            latency[entry].append(d['endtime']-data['startime'])
            self.write_log(data)
            print 'RX: {0} from {1}'.format(data, addr)
            self.__main_thread_notifier.set()

    def __send_command_1(self, toip, toport, command, rx=False):
        try:
            message = str(command)
            len_msg = 5 + len(message) # 5 => 4 digits and a space
            message = "{0:04d} {1}".format(len_msg, message)
            return_message = "NONE"
            print 'TX: {0} to {1}'.format(message, (toip, toport))
            if self.client_skt is not None:
                self.client_skt.close()
            self.client_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_skt.connect((toip, int(toport)))
            except socket.error, e:
                print e.message
                self.client_skt.close()
                self.client_skt = None
                return

            self.client_skt.send(message)
            if rx == True:
                try:
                    return_message = self.client_skt.recv(3500)
                except socket.error, e:
                    return_message = "TIMEOUT"
            self.client_skt.close()
            self.client_skt = None
            return return_message
        except Exception as msg:
            print msg
            return msg

    def __send_command(self, ip, port, command, rx=False):
        try:
            if self.client_skt is not None:
                self.client_skt.close()
            self.client_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_skt.connect((toip, int(toport)))
            except socket.error, e:
                print e.message
                self.client_skt.close()
                self.client_skt = None
                return

            self.client_skt.send(message)
            return_message = "NONE"
            if rx == True:
                try:
                    return_message = self.client_skt.recv(3500)
                except socket.error, e:
                    return_message = "TIMEOUT"
            self.client_skt.close()
            self.client_skt = None
            return return_message
        except Exception as msg:
            print msg
            return msg

    def fake_register(self):
        del self.nodes[:]
        command = "REG " + str(self.myip) + " " + str(self.myport) + " " + str(self.bootstrap[2])
        return_message = self.__send_command(self.bootstrap[0], self.bootstrap[1], command, True)
        if "REGOK" in return_message:
            rxd_data = return_message.split()
            num_peers = int(rxd_data[3])
            rxd_data = rxd_data[4:]
            del self.nodes[:]
            for i in range(num_peers):
                p_ip = rxd_data[2*i]
                p_port = rxd_data[2*i + 1]
                self.nodes.append((p_ip, p_port))
            command = "DEL IPADDRESS " + str(self.myip) + " " + str(self.myport) + " " + str(self.bootstrap[2])
            self.__send_command(self.bootstrap[0], self.bootstrap[1], command, True)
            return (True, num_peers)
        return (False, 0)

    def search_for(self, query):
        node = self.random_node()
        if node is not None:
            command = {'command':'STARTSEARCH', 'QUERY':entry, 'SERVERINFO':(self.myip, self.myport)}
            self.__send_command(node[0], node[1], json.dumps(command))
            self.write_log("STARTSEARCH " + entry + "=> " + str(node[0]) + ":" + str(node[1]))
            self.__main_thread_notifier.wait(3)
            self.__main_thread_notifier.clear()
            return True
        return False

    def ring_test(self, num_nodes):
        if len(self.nodes) < num_nodes:
            print '%d nodes not registered to bootstrap' %(num_nodes)
            return False
        random.seed()
        l = len(self.nodes)
        idx = random.choice(range(l))
        n_ip, n_port = self.nodes[idx]
        # len RINGTEST num_nodes myip myport
        command = "RINGTEST " + str(num_nodes) + " " + str(self.myip) + " " + str(self.myport)
        self.__send_command(n_ip, n_port, command)
        b = self.__main_thread_notifier.wait(5)
        if b == False:
            print 'RINGTEST command failed!'
            return False
        else:
            self.__main_thread_notifier.clear()
            return True

    def exit_all_nodes(self):
        ip, port = self.random_node()
        if None not in (ip, port):
            self.exit_node(ip, port)
        command = "DEL UNAME " + str(uname)
        self.__send_command_1(b_ip, b_port, command, True)
        self.__main_thread_notifier.wait(5)

    def random_node(self):
        random.seed()
        l = len(self.nodes)
        if l > 0:
            idx = random.choice(range(l))
            ip, port = self.nodes[idx]
            return ip, port
        return None

    def exit_node(self, ip, port):
        #command = "EXITALL " + str(self.myip) + " " + str(self.myport)
        command = {'command':'EXITALL', 'SERVERINFO':(self.myip, self.myport)}
        self.__send_command(ip, port, command)
        for i in self.nodes:
            b = self.__main_thread_notifier.wait(2)
            self.__main_thread_notifier.clear()

    def get_iplist(self):
        command = "GET IPLIST " + str(uname)
        return_message = self.__send_command_1(b_ip, b_port, command, True)
        if "GET IPLIST OK" in return_message:
            data = return_message.split()
            num_ips = int(data[5])
            if num_ips == 9998 or num_ips == 9999:
                print 'No IPS registered with this bootstrap!'
                return
            del self.nodes[:]
            data = data[6:]
            for i in range(num_ips):
                self.nodes.append((data[2*i], data[2*i+1]))
            return True
        return False

    def pick_remanining(self, num_entries):
        self.get_iplist()
        for ip, port in self.nodes:
            self.__send_command(ip, port, json.dumps({'command':'PICKRESOURCES', 'num_entries':4}))
            time.sleep(0.5)

    def display(self, ip, port, arg):
        command = {'command':arg}
        self.__send_command(ip, port, command)

    def write_log(self, data):
        cur_time = strftime("[%m-%d %H:%M:%S]", gmtime())
        msg = "{0}: {1}".format(cur_time, data)
        f.write(msg + '\n')



def keyboard_interrupt_handler(sig, frame):
    print "In SIGINT Handler"
    controller.exit_all_nodes()
    os._exit(0)

def arg_parser(args):
    global b_ip, b_port, zipf_s, nw_size
    if '-b' not in args:
        print 'Bootstrap IP missing'
        help()
    if '-n' not in args:
        print 'Bootstrap Port missing'
        help()
    if '-z' not in args:
        print "Zipf's parameter missing"
        help()
    if '-s' not in args:
        print 'Network Size missing'
        help()
    option, value = getopt.getopt(args, 'b:n:z:s:')
    for o, v in option:
        if o == '-b':
            b_ip = v
        elif o == '-n':
            b_port = int(v)
        elif o == '-z':
            zipf_s = float(v)
        elif o == '-s':
            nw_size = int(v)

def help():
    print "Usage: %s -b <Bootstrap IP> -n <Bootstrap Port> -z <Zipf's parameter> -s <Network Size>" %(sys.argv[0])
    sys.exit(0)

def get_zipf_s(file_contents, s):
    l = len(file_contents)
    zeta = 0.0
    for i in range(l):
        zeta += 1.0 / (i + 1) ** s
    freq = []
    for i in range(l):
        p = 1000 * 1.0 / (i + 1) ** s / zeta
        freq.append(int(round(p)))
    return freq

def read_resources(filename):
    file_contents = []
    f = open(filename, 'r')
    for line in f:
        if line[0] == "#" or line[0] == '\n':
            continue
        file_contents.append(line.rstrip())
    return file_contents

def main():
    global controller
    controller = CentralController(b_ip, b_port, uname, zipf_s)
    controller.get_iplist()
    num_nodes = len(controller.nodes)
    if num_nodes < nw_size:
        print 'Network size is %d. Desired Size is %d' %(num_nodes, nw_size)
        sys.exit(0)

    controller.pick_remanining(4)
    resources = read_resources('resources_sp2p.txt')
    freq = get_zipf_s(resources, 0.6)
    idx = 0
    for f in freq:
        r = range(f)
        query = resources[idx]
        for i in range(r):
            controller.search_for(query)
        idx += 1

    controller.exit_all_nodes()


#Initial processing
if __name__ == "__main__":
    try:
        if(len(sys.argv) == 1 or '-h' in sys.argv):
            help()
        else:
            signal.signal(signal.SIGINT, keyboard_interrupt_handler)
            arg_parser(sys.argv[1:])
            main()
    except KeyboardInterrupt:
        print "Program aborted"
