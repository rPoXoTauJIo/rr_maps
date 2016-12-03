# ------------------------------------------------------------------------
# Project Reality debug module by rPoXo
#
# Description:
#
#   Provides various debug for modules
#
# ------------------------------------------------------------------------

import os
import sys
import time
import cPickle
import socket

# import bf2 #suprisingly not needed
# import host # <-- replaced by interface

# import realitylogger as rlogger # <-- replaced by interface

import rr_config_debugger as C
# from datetime import datetime


class Debugger():

    def __init__(self, interface):
        self.interface = interface
        self.g_time_init_epoch = time.time()
        self.g_time_init_wall = self.interface.get_wall_time()
        
        self.g_default_server_addr = C.SERVERHOST
        self.g_default_server_port = C.SERVERPORT
        
        self.g_logger_name = "RRDebug"
        self.interface.create_logger(name=self.g_logger_name,
                                    path=C.PATH_LOG_DIRECTORY,
                                    fileName=C.PATH_LOG_FILENAME,
                                    continous=True)
        self.g_SOCK = None
        self.client_udp_create()

    def client_udp_create(self):
        try:
            self.g_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.interface.debug_echo('Created UDP socket')
        except socket.error:
            # self.errorMessage()
            self.interface.debug_echo('Failed to create UDP socket')

    def client_udp_destroy(self):
        try:
            self.g_SOCK.close()
            self.interface.debug_echo('Closed UDP socket')
        except socket.error:
            # self.errorMessage()
            self.interface.debug_echo('Failed to close UDP socket')

    def debug_message(msg, senders=None):

        def debug_file(msg):
            self.interface.send_logger_logLine(self.g_logger_name, msg)

        def debug_socket(msg):
            try:
                if C.PICKLE_DATA:
                    message = cPickle.dumps(data)
                else:
                    message = msg
                SOCK.sendto(message, (C.CLIENTHOST, C.CLIENTPORT))
            except:
                debug_echo('debug_socket(): failed to send message')

        debugs = {
            'echo': self.interface.debug_echo,
            'ingame': self.interface.debug_ingame,
            'file': debug_file,
            'udp': debug_socket,
        }
        if senders is None:
            for default_debug in C.DEBUGS_DEFAULT:
                debugs[default_debug](msg)
        else:
            for debug in senders:
                debugs[debug](msg)

    def error_message():
        type_, value_, traceback_ = sys.exc_info()
        print 'Traceback:\n'
        print 'Type:   %s' % (type_)
        print 'Value:  %s' % (value_)
        print 'EXCEPTION: %s' % (str(sys.exc_info()[0]))
        print '\n...\n...\n...'
        errType = str(sys.exc_info()[0])
        errPart1 = 'EXCEPTION: ' + errType[errType.find('.') + 1:]
        errPart2 = str(sys.exc_info()[1])

        # \t is TAB
        trace = '\n\tTrace:'
        lastTrace = ''
        while sys.exc_info()[2] is not None:
            if sys.exc_traceback.tb_lineno == 0:
                sys.exc_info()[2] = sys.exc_traceback.tb_next
                continue

            lastTrace = str(sys.exc_traceback.tb_frame.f_code.co_filename) + \
                ' on line ' + str(sys.exc_traceback.tb_lineno)
            trace += '\n\t\t' + lastTrace
            sys.exc_info()[2] = sys.exc_traceback.tb_next

        print errPart1 + '\n\t' + errPart2 + trace + '\n'


pass

