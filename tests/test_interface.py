# testing interface is pure for syntax as prbf2 throws no trace incase of error
import unittest
import rr_interface

class Mock_bf2(object):
    
    def __init__(self):
        self.Status = None
        
class Mock_host(object):
    
    def __init__(self):
        pass

class Mock_realitylogger(object):
    
    def __init__(self):
        pass
        
class TestInterface(unittest.TestCase):

    def setUp(self):
        bf2 = Mock_bf2()
        host = Mock_host()
        realitylogger = Mock_realitylogger()

        self.interface = rr_interface.Interface(bf2, host, realitylogger)

    def test_can_init_interface(self):
        self.assertIsInstance(self.interface, rr_interface.Interface)

if __name__ == '__main__':
    unittest.main()