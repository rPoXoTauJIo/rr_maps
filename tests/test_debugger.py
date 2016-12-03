import socket
import unittest

import rr_mocks

import rr_debugger


class TestDebugger(unittest.TestCase):

    def setUp(self):
        interface = rr_mocks.MockInterface()
        self.debugger = rr_debugger.Debugger(interface)

    def test_can_init_debugger(self):
        self.assertIsInstance(self.debugger, rr_debugger.Debugger)
    
    def test_create_socket(self):
        self.assertIsInstance(self.debugger.g_SOCK, socket.socket)
        

if __name__ == '__main__':
    unittest.main()