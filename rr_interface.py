

class Interface(object):
    # class to encapsulate interactions with the calling environment on a game
    # server

    def __init__(self, bf2, host, realitylogger):
        self.__bf2 = bf2
        self.__host = host
        self.__realitylogger = realitylogger
        self.C = {}
        self.init_config()

    def init_config(self, config = 'rr_config'):
        CFG = __import__(config, globals(), locals(), ['*'])
        self.C.update(CFG.C)

    def get_wall_time(self):
        return self.__host.timer_getWallTime()

    def get_mod_directory(self):
        return self.__host.sgl_getModDirectory()

    def create_logger(self, name, path, fileName, continous):
        if self.C['FILELOG']:
            self.__realitylogger.createLogger(name, path, fileName, continous)
        else:
            self.debug_echo('Filelogging disabled')

    def send_logger_logLine(self, name, msg):
        # self.__realitylogger.RealityLogger[name].setActive( True )
        if self.C['FILELOG']:
            return self.__realitylogger.RealityLogger[name].logLine(msg)
    
    def set_active_logger(self, name, not_really=True):
        if self.C['FILELOG']:
            self.__realitylogger.RealityLogger[name].setActive(not_really)
        else:
            self.debug_echo('Filelogging disabled, cant activate logger %s' % (name))

    def debug_echo(self, msg):
        try:
            self.__host.rcon_invoke("echo \"" + str(msg) + "\"")
        except:
            self.__host.rcon_invoke("echo \"" +
                                    'debug_echo(): failed to display message' +
                                    "\"")

    def debug_ingame(self, msg):
        try:
            self.__host.rcon_invoke("game.sayAll \"" + str(msg) + "\"")
        except:
            self.__host.rcon_invoke("game.sayAll \"" +
                                    'debug_ingame(): failed to display message' +
                                    "\"")
