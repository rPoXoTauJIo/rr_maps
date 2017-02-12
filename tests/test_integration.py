import os
import sys
import subprocess
import unittest
import socket
import threading
import time

import rr_mocks

import rr_config

class TestServer(unittest.TestCase):
    
    def setUp(self):
        self.path_game_root_relative = '..\\..\\..\\..\\..\\'
        self.name_exe = 'PRBF2_repo_w32ded.exe'
        self.launch_args = '+modPath mods/pr'
        self.game_server = None
    
    def tearDown(self):
        self.game_server.terminate()

    def test_can_start_server(self):
        os.chdir(self.path_game_root_relative)
        launch_string = '"' + self.name_exe + '"' + ' ' + self.launch_args
        rr_config.C['SOCKET'] = True
        test_message = 'INIT: Server initialized'
        timeout_message = 'TIMEOUT'

        # Start fake server in background thread
        client = rr_mocks.MockNetwork(rr_config).client
        server = rr_mocks.MockNetwork(rr_config).server
        server.exit_flags.append(test_message)
        server.exit_flags.append(timeout_message)
        server_thread = threading.Thread(target=server.runner_fake_server)
        server_thread.start()

        start_time = time.time()
        timeout = 5.640 # seconds should be enough for everyone

        # starting game server
        self.game_server = subprocess.Popen(launch_string, shell=False)

        # Start client sending messages
        while 1:
            if test_message in server.messages:
                # Ensure server thread ends
                server_thread.join()
                break
            if not server_thread.isAlive():
                # skipping test if we could not create listening server
                #self.skipTest('Failed to create UDP server thread')
                pass
            if time.time() - start_time > timeout:
                client.send_message(timeout_message, rr_config.C['CLIENTHOST'], rr_config.C['CLIENTPORT'])
                server_thread.join()
                break

        self.assertTrue(test_message in server.messages)

if __name__ == '__main__':
    unittest.main()