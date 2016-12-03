# testing interface is pure for syntax as prbf2 throws no trace incase of error
import unittest

import rr_mocks

import rr_interface
        
class TestInterface(unittest.TestCase):

    def setUp(self):
        self.__bf2 = rr_mocks.Mock_bf2()
        self.__host = rr_mocks.Mock_host()
        self.__realitylogger = rr_mocks.Mock_realitylogger()

        self.interface = rr_interface.Interface(self.__bf2, self.__host, self.__realitylogger)

    def test_init_interface(self):
        self.assertIsInstance(self.interface, rr_interface.Interface)
    
    def test_assert_get_wall_time(self):
        self.assert_(self.interface.get_wall_time() is 0)
    
    def test_assert_get_mod_directory(self):
        self.assert_(self.interface.get_mod_directory() is '.')
    
    def test_assert_create_logger(self):
        name = 'testLog'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.create_logger(name, path, fileName, continous)
        self.assertIn(name, self.__realitylogger.RealityLogger._loggers)
        #logger, 
    
    def test_assert_send_logger_logLine(self):
        name = 'testLog2'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.create_logger(name, path, fileName, continous)
        self.interface.send_logger_logLine(name, 'testmsg')
        self.assertIn('testmsg', self.__realitylogger.RealityLogger[name].messages)
        
    def test_assert_debug_echo(self):
        self.interface.debug_echo('testmsg2')
        self.assertIn('testmsg2', self.__host._game._state._echo)


if __name__ == '__main__':
    unittest.main()