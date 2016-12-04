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

# import rr_config_debugger as C
# from datetime import datetime


class Debugger():

    _client = None

    def __init__(self, interface):
        self.interface = interface
        if self.interface.C['SOCKET']:
            self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__default_addr = self.interface.C['CLIENTHOST']
            self.__default_port = self.interface.C['CLIENTPORT']
        '''
        self.g_time_init_epoch = time.time()
        self.g_time_init_wall = self.interface.get_wall_time()
        
        self.g_default_log_path = C.PATH_LOG_DIRECTORY
        self.g_default_log_filename = C.PATH_LOG_FILENAME
        
        self.g_logger_name = "RRDebug"
        self.interface.create_logger(name=self.g_logger_name,
                                    path=self.g_default_log_path,
                                    fileName=self.g_default_log_filename,
                                    continous=True)
        '''
    
    def _debug_socket(self, msg, addr=None, port=None):
        if self.interface.C['SOCKET']:  # safety check
            try:
                if self.interface.C['PICKLE_DATA']:
                    msg = cPickle.dumps(msg)
                if addr is None:
                    addr = self.__default_addr
                if port is None:
                    port = self.__default_port
                self._client.sendto(msg, (addr, port))
            except:
                self.interface.debug_echo('debug_socket(): failed to send message')

    '''
    def debug_message(msg, senders=None):

        def _debug_file(msg):
            self.interface.send_logger_logLine(self.g_logger_name, msg)

        def debug_socket(msg, addr=self.g_default_server_addr, port=self.g_default_server_port):
            if self.interface.C['SOCKET']:  # safety check
                try:
                    if C.PICKLE_DATA:
                        msg = cPickle.dumps(data)
                    SOCK.sendto(msg, (addr, port))
                except:
                    debug_echo('debug_socket(): failed to send message')

        debugs = {
            'echo': self.interface.debug_echo,
            'ingame': self.interface.debug_ingame,
            'file': _debug_file,
            'udp': _debug_socket,
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
    '''

pass
