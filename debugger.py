# ------------------------------------------------------------------------
# Project Reality debug module by rPoXo
#
# Description:
#
#   Provides various debug for modules
#
# ------------------------------------------------------------------------

# sys modules
import sys
import time
import cPickle
import socket

# game core modules
import host

# PR modules
from game import realitylogger

class Debugger:

    #_client = None

    def __init__(self, C):
        self._client = None

        #self._time_init_epoch = time.time()
        #self._time_init_wall = host.timer_getWallTime()

        self._default_addr = C['CLIENTHOST']
        self._default_port = C['CLIENTPORT']
        self._default_log_path = C['PATH_LOG_DIRECTORY']
        self._default_log_filename = C['PATH_LOG_FILENAME']
        self._logger_name = "RRDebug"
        self._logger_enabled = False
        
        if C['SOCKET']:
            self._init_client()
        if C['FILELOG']:
            self._init_filelogger()
            self._logger_enabled = True

    def _init_client(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _init_filelogger(self):
        realitylogger.createLogger(name=self._logger_name,
                                   path=self._default_log_path,
                                   fileName=self._default_log_filename,
                                   continous=True)

    def _debug_socket(self, msg, addr=None, port=None):
        if self._client != None:  # safety check
            if addr == None:
                addr = self._default_addr
            if port == None:
                port = self._default_port
            try:
                self._client.sendto(msg, (addr, port))
                return True
            except:
                self._debug_echo('_debug_socket(): failed to send message')
                return False
        return False

    def _debug_file(self, msg):
        if self._logger_enabled:
            try:
                return realitylogger.RealityLogger[self._logger_name].logLine(msg)
            except KeyError:
                self._logger_enabled = False
                return False
        return False

    def _debug_echo(self, msg):
        try:
            host.rcon_invoke('echo "%s"' % (str(msg)))
            return True
        except:
            host.rcon_invoke('echo "_debug_echo(): failed to display message"')
            return False

    def _debug_ingame(self, msg):
        try:
            host.rcon_invoke('game.sayAll "%s"' % (str(msg)))
            return True
        except:
            host.rcon_invoke(
                'game.sayAll "_debug_ingame(): failed to send message"')
            return False

    def message(self, msg, targets=['echo']):
        senders = {
            'ingame' : self._debug_ingame,
            'echo' : self._debug_echo,
            'file' : self._debug_file,
            'udp' : self._debug_socket
            }
        
        for target in targets:
            if target not in senders:
                continue
            senders[target](msg)
    

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
