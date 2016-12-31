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
            try:
                server_sock.bind((self.__listenhost, self.__listenport))
                while 1:
                    d = server_sock.recvfrom(1024)
                    data = d[0]  # data
                    addr = d[1]  # ip and port
                    self.messages.append(data)
                    if data in self.exit_flags:
                        break
                server_sock.close()
            except socket.error:
                server_sock.close()
            

    def __init__(self, config):
        self.C = config.C
        self.server = self.__FakeServer(
            self.C['SERVERHOST'], self.C['SERVERPORT'])


class host(object):

    class _MockGame(object):

        class _MockState(object):

            def __init__(self):
                self._console_log = []
                self._echo = []
                self._chat = {
                    'server': [],
                }
                self._map = (None, None, None)  # map name, gamemode, layer

        def __init__(self):
            self._state = self._MockState()
            self.__handlers = {
                'echo': self.__handler_echo,
                'game.sayAll': self.__handler_say_all,
            }

        def invoke(self, input):
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

    def rcon_invoke(self, command):
        self._game.invoke(command)

    def sgl_getModDirectory(self):
        return '.'
    
    def sgl_getMapName(self):
        return self.ss_getParam('mapName')

    def ss_getParam(self, key):
        params = {
            'mapName' : self._game._state._map[0],
            'gameMode' : self._game._state._map[1]
            }
        return params[key]


# class to mock 'game' module
class game(object):
    
    def __init__(self, host):
        self.realitylogger = realitylogger(host)

class realitylogger(object):

    def __init__(self, host):
        self.RealityLogger = MockLogger(host)

    def createLogger(self, name, path, fileName, continous):
        self.RealityLogger.createLogger(name, path, fileName, continous)


class MockLogger(object):

    # holds loggers
    _loggers = {}

    def __init__(self, host):
        self.host = host

    def __getitem__(self, key):
        return self._loggers[key]

    def __len__(self):
        return len(self._loggers)

    def createLogger(self, name, path, fileName, continous):
        if name not in self._loggers:
            self._loggers[name] = self.__Logger(path, fileName, continous)

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
        def setActive(self, active):
            self.active = active

class bf2(object):
    
    def __init__(self, host):
        self.gameLogic = self.GameLogic(host)
        self.serverSettings = self.ServerSettings(host)
        
    
    class GameLogic:
        
        def __init__( self, host ):
            self.host = host

        def getMapName( self ): return self.host.sgl_getMapName( )

    class ServerSettings:

        def __init__( self, host ):
            self.host = host

        def getGameMode( self ): return self.host.ss_getParam( 'gameMode' )
    








