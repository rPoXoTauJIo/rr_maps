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

        # copypasted solution by NanoDano
        # http://www.devdungeon.com/content/unit-testing-tcp-server-client-python
        def __run_fake_server():
            # Run a server to listen for a connection and then close it
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_sock.bind((self.interface.C['SERVERHOST'], self.interface.C['SERVERPORT']))
            while 1:
                d = server_sock.recvfrom(1024)
                data = d[0]  # data
                addr = d[1]  # ip and port
                if data == message:
                    self.__messages.append(data)
                    break
            server_sock.close()
     
        # Start fake server in background thread
        self.__messages = []
        server_thread = threading.Thread(target=__run_fake_server)
        server_thread.start()

        # Start client sending messages
        while 1:
            debugger._client.sendto(message, (self.interface.C['CLIENTHOST'], self.interface.C['CLIENTPORT']))
            if message in self.__messages:
                # Ensure server thread ends
                server_thread.join()
                break

        self.assert_(message in self.__messages)
        

if __name__ == '__main__':
    unittest.main()