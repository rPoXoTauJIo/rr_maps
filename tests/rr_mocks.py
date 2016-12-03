class MockConsole(object):
    
    def __init__(self):
        self.messages = []

    def echo(self, msg):
        self.messages.append(msg)


class MockInterface(object):
    
    class __MockLogger(object):
    
        def __init__(self, name, path, fileName, continous):
            self.__name = name
            self.__path = path
            self.__fileName = fileName
            self.__continous = continous
            
            self.__buffer = []

    def __init__(self):
        self.__logger = None
        self.__console = MockConsole()
    
    def get_wall_time(self):
        return 0
    
    def create_logger(self, name, path, fileName, continous):
        return self.__MockLogger(name, path, fileName, continous)
    
    def debug_echo(self, msg):
        self.__console.echo(msg)
        
    def get_mod_directory(self):
        return '.'