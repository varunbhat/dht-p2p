from StandaloneBootstrapHdlr import BootstrapServer, BSDeleteError
import sys, socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s] %(message)s')


def check(i):
    serv = BootstrapServer(ip_list_file='bs_list.txt')
    serv.set_username('ALPHA')
    try:
        serv.set_server(i)
        try:
            serv.deregister_all()
            logging.info("    Working " + str(serv.get_address()) + " (Cleared)")
        except BSDeleteError:
            logging.info("    Working " + str(serv.get_address()))
    except socket.timeout:
        logging.info("Not Working " + str(serv.get_address()))


for i in range(7):
    threading.Thread(target=check, args=(i,)).start()
