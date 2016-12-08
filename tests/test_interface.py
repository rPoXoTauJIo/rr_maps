# testing interface is pure for syntax as prbf2 throws no trace incase of error
import unittest

import rr_mocks
import rr_config

import rr_interface
        
class TestInterface(unittest.TestCase):

    def setUp(self):
        self.__bf2 = rr_mocks.Mock_bf2()
        self.__host = rr_mocks.Mock_host()
        self.__realitylogger = rr_mocks.Mock_realitylogger()

        self.interface = rr_interface.Interface(self.__bf2, self.__host, self.__realitylogger)
        self.interface.init_config('rr_config')
        self.interface.C['FILELOG'] = True
    
    def tearDown(self):
        del self.__bf2, self.__host, self.__realitylogger, self.interface

    def test_init_interface(self):
        self.assertIsInstance(self.interface, rr_interface.Interface)
    
    def test_interface_config_init(self):
        self.interface.init_config('rr_config')
        for key, value in rr_config.C.items():
            self.assertIn(key, self.interface.C)
            self.assertEqual(self.interface.C[key], value)
    
    def test_assert_get_wall_time(self):
        self.assert_(self.interface.get_wall_time() is 0)
    
    def test_assert_get_mod_directory(self):
        self.assert_(self.interface.get_mod_directory() is '.')
    
    def test_assert_create_logger(self):
        name = 'testLog1_1'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.create_logger(name, path, fileName, continous)
        self.assertIn(name, self.__realitylogger.RealityLogger._loggers)
        #logger, 
    
    def test_should_not_create_logger_if_filelog_disabled(self):
        name = 'testLog1_2'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.C['FILELOG'] = False
        self.interface.create_logger(name, path, fileName, continous)
        self.assertNotIn(name, self.__realitylogger.RealityLogger._loggers)
    
    def test_should_echo_create_logger_if_filelogger_disabled(self):
        name = 'testLog1_3'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.C['FILELOG'] = False
        self.interface.create_logger(name, path, fileName, continous)
        self.assertIn('Filelogging disabled', self.__host._game._state._echo)
    
    def test_assert_set_active_logger(self):
        name = 'testLog2_1'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.create_logger(name, path, fileName, continous)
        self.interface.set_active_logger(name)
        self.assert_(self.__realitylogger.RealityLogger[name].active is True)
    
    def test_should_echo_set_active_logger_if_filelogger_disabled(self):
        name = 'testLog2_2'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.C['FILELOG'] = False
        self.interface.create_logger(name, path, fileName, continous)
        self.interface.set_active_logger(name)
        self.assertIn('Filelogging disabled, cant activate logger %s' % (name), self.__host._game._state._echo)
    
    def test_assert_send_logger_logLine(self):
        name = 'testLog3'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.create_logger(name, path, fileName, continous)
        self.interface.send_logger_logLine(name, 'test logger')
        self.assertIn('test logger', self.__realitylogger.RealityLogger[name].messages)
    
    def test_should_not_assert_send_logger_logLine_if_filelog_disabled(self):
        name = 'testLog1_2'
        path = '.'
        fileName = 'rr_mapscript.txt'
        continous = False
        self.interface.C['FILELOG'] = False
        self.interface.create_logger(name, path, fileName, continous)
        self.assert_(self.interface.send_logger_logLine(name, 'test no logging') is None) # not exception
        
    def test_assert_debug_echo(self):
        self.interface.debug_echo('test echo')
        self.assertIn('test echo', self.__host._game._state._echo)
    
    def test_assert_debug_ingame(self):
        self.interface.debug_ingame('test ingame')
        self.assertIn('test ingame', self.__host._game._state._chat['server'])
    


if __name__ == '__main__':
    unittest.main()