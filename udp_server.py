# --------------------------------------------------------------------------
# udp_server
#
# Description:
#
#   Simple udp socket server for testing
#   Will listen for udp messages and print them in console
#
# -------------------------------------------------------------------------
import os
import sys
import time
import socket

'''
class Server(object):

    def __init__(self, listenhost, listenport):
        self.__listenhost = listenhost
        self.__listenport = listenport
        self.messages = []
        self.exit_flags = []

    def run(self):
        # Run a server to listen for a connection and then close it
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_sock.bind((self.__listenhost, self.__listenport))
        while 1:
            d = server_sock.recvfrom(1024)
            data = d[0]  # data
            addr = d[1]  # ip and port
            self.messages.append(data)
            if data in self.exit_flags:
                break
        server_sock.close()




if __name__ == '__main__':
    C = {
        'SERVERHOST' : 'localhost',
        'SERVERPORT' : 8888,
        }
    server = Server(C['SERVERHOST'], C['SERVERPORT'])
    server.run()
'''

SOCK = None
C = {
    'SERVERHOST': 'localhost',
    'SERVERPORT': 8888,
}

# Datagram (udp) socket
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK.bind((C['SERVERHOST'], C['SERVERPORT']))

# now keep talking with the client
while 1:
    data, addr = SOCK.recvfrom(1024)
    print('Message from[%s:%s]: %s' % (addr[0], addr[1], data))

S.close()
