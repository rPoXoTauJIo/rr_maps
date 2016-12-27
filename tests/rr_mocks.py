import socket


class MockNetwork(object):
    # solution by NanoDano
    # http://www.devdungeon.com/content/unit-testing-tcp-server-client-python

    class __FakeServer(object):

        def __init__(self, listenhost, listenport):
            self.__listenhost = listenhost
            self.__listenport = listenport
            self.messages = []
            self.exit_flags = []

        def runner_fake_server(self):
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


    def __init__(self, interface):
        self.interface = interface
        self.server = self.__FakeServer(self.interface.C['SERVERHOST'], self.interface.C['SERVERPORT'])


class Mock_bf2(object):
    # actually it's just a wrapper around host in bf2
    
    def __init__(self):
        self.Status = None
        
class Mock_host(object):
    
    class _MockGame(object):
    
        class _MockState(object):
            
            def __init__(self):
                self._console_log = []
                self._echo = []
                self._chat = {
                    'server' : [],
                    }
        
        def __init__(self):
            self._state = self._MockState()
            self.__handlers = {
                'echo' : self.__handler_echo,
                'game.sayAll' : self.__handler_say_all,
                }
            
        def send_to_handlers(self, input):
            self._state._console_log.append(input)
            self.command = input.split(' ')[0]
            self.__handlers[self.command](input)
        
        def __handler_echo(self, input):
            self._state._console_log.append(input)
            message = input.replace('echo ', '')
            message = message.replace('"', '').replace("'", '')
            self._state._echo.append(message)
        
        def __handler_say_all(self, input):
            message = input.replace('game.sayAll ', '')
            message = message.replace('"', '').replace("'", '')
            self._state._chat['server'].append(message)

    def __init__(self):
        self._game = self._MockGame()
    
    def timer_getWallTime(self):
        return 0
        
    def sgl_getModDirectory(self):
        return '.'
    
    def rcon_invoke(self, command):
        self._game.send_to_handlers(command)

class Mock_realitylogger(object):

    def __init__(self):
        self.RealityLogger = MockLogger()
    
    def createLogger(self, name, path, fileName, continous):
        self.RealityLogger.createLogger(name, path, fileName, continous)

class MockLogger(object):
    
    # holds loggers
    _loggers = { }
    
    def __init__(self):
        pass
        
    def __getitem__( self, key ):
        return self._loggers[key]

    def __len__( self ):
        return len( self._loggers )
    
    def createLogger(self, name, path, fileName, continous):
        if name not in self._loggers:
            self._loggers[name] = self.__Logger( path, fileName, continous )
    
    class __Logger(object):

        def __init__(self, path, fileName, continous):
            self._path = path
            self._fileName = fileName
            self._continous = continous
            self.active = False
            
            self.messages = []
        
        def logLine(self, msg):
            try:
                self.messages.append(msg)
                return True
            except:
                return False
        
        # To Enable/Disable logging at certain times
        # Disabled logger still logs to memory buffer!
        def setActive( self, active ):
            self.active = active

class MockInterface(object):

    def __init__(self):
        self.__logger = MockLogger()
        self.__host = Mock_host()
        self.C = {}
    
    def init_config(self, config):
        CFG = __import__(config)
        self.C.update(CFG.C)
    
    def get_wall_time(self):
        return self.__host.timer_getWallTime()
    
    def create_logger(self, name, path, fileName, continous):
        self.__logger.createLogger(name, path, fileName, continous)
    
    def send_logger_logLine(self, name, msg):
        return self.__logger._loggers[name].logLine(msg)
    
    def debug_echo(self, msg):
        self.__host.rcon_invoke("echo \"" + str(msg) + "\"")
        
    def get_mod_directory(self):
        return self.__host.sgl_getModDirectory()

    # methods for testing
    def _get_echo_messages(self):
        return self.__host._game._state._echo






