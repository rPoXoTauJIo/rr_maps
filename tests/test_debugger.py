import time
import socket
import unittest
import threading

import rr_mocks

import rr_debugger

class TestDebugger(unittest.TestCase):

    def setUp(self):
        self.interface = rr_mocks.MockInterface()
        self.interface.init_config('rr_config')

    def tearDown(self):
        del self.interface

    def test_init_debugger(self):
        debugger = rr_debugger.Debugger(self.interface)
        self.assertIsInstance(debugger, rr_debugger.Debugger)
    

class TestDebuggerFilelog(unittest.TestCase):

    def setUp(self):
        self.interface = rr_mocks.MockInterface()
        self.interface.init_config('rr_config')

    def tearDown(self):
        del self.interface

    def test_filelogger_default_disabled(self):
        debugger = rr_debugger.Debugger(self.interface)
        self.assert_(debugger.interface.C['FILELOG'] is False)
        self.assert_(debugger._filelogger is None)

    # test for creating logger in interface creation
    def test_filelogger_default_enabled(self):
        self.interface.init_config('rr_config')
        self.interface.C['FILELOG'] = True
        debugger = rr_debugger.Debugger(self.interface)
        self.assert_(debugger.interface.C['FILELOG'] is True)

    def test_filelogger_can_send_message(self): 
        self.interface.init_config('rr_config')
        self.interface.C['FILELOG'] = True
        debugger = rr_debugger.Debugger(self.interface)
        self.assert_(debugger._debug_file('test message') is True)
    
    def test_filelogger_should_not_send_message_if_disabled(self): 
        self.interface.init_config('rr_config')
        self.interface.C['FILELOG'] = False
        debugger = rr_debugger.Debugger(self.interface)
        self.assert_(debugger._debug_file('test message') is False)


class TestDebuggerSockets(unittest.TestCase):

    def setUp(self):
        self.interface = rr_mocks.MockInterface()
        self.interface.init_config('rr_config')

    def tearDown(self):
        del self.interface

    def test_socket_client_default_disabled(self):
        debugger = rr_debugger.Debugger(self.interface)
        self.assert_(debugger.interface.C['SOCKET'] is False)
        self.assert_(debugger._client is None)

    def test_socket_client_default_enabled(self):
        self.interface.init_config('rr_config')
        self.interface.C['SOCKET'] = True
        debugger = rr_debugger.Debugger(self.interface)
        self.assert_(debugger.interface.C['SOCKET'] is True)
        self.assertIsInstance(debugger._client, socket.socket)

    def test_socket_client_can_send_message(self):
        self.interface.init_config('rr_config')
        self.interface.C['SOCKET'] = True
        debugger = rr_debugger.Debugger(self.interface)
        message = 'test udp'

        # Start fake server in background thread
        server = rr_mocks.MockNetwork(self.interface).server
        server.exit_flags.append(message)
        server_thread = threading.Thread(target=server.runner_fake_server)
        server_thread.start()

        # Start client sending messages
        while 1:
            debugger._debug_socket(
                message, self.interface.C['CLIENTHOST'], self.interface.C['CLIENTPORT'])
            if message in server.messages:
                # Ensure server thread ends
                server_thread.join()
                break

        self.assert_(message in server.messages)

if __name__ == '__main__':
    unittest.main()
