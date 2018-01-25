import os
import sys
import subprocess
import unittest
import socket
import threading
import time

#import rr_mocks

#import rr_config

@unittest.skip('need to refactor tests first')
class TestServer(unittest.TestCase):
    
    def setUp(self):
        self.path_game_root_relative = '..\\..\\..\\..\\..\\'
        self.name_exe = 'PRBF2_repo_w32ded.exe'
        self.launch_args = '+modPath mods/pr'
        # as stdin\stdout not working with bf2 server, the only way to communicate with it is sockets
        if rr_config.C['SOCKET']:
            self.skipTest('Sockets disabled, cant receive debug info from game server')

    @unittest.skip('need to refactor tests first')
    def test_can_start_server(self):
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
        timeout = 10.640 # seconds should be enough for everyone

        current_dir = os.getcwd()
        # for some reason bf2 can't find it's modules otherwise
        os.chdir(self.path_game_root_relative)
        launch_string = '"' + self.name_exe + '"' + ' ' + self.launch_args
        # starting game server
        game_server = subprocess.Popen(launch_string, shell=False)

        # Start client sending messages
        while 1:
            if test_message in server.messages:
                # Ensure server thread ends
                server_thread.join()
                break
            if not server_thread.isAlive():
                # skipping test if we could not create listening server
                self.skipTest('Failed to create UDP server thread')
            if time.time() - start_time > timeout:
                client.send_message(timeout_message, rr_config.C['CLIENTHOST'], rr_config.C['CLIENTPORT'])
                server_thread.join()
                break
        
        # terminate game server
        game_server.terminate()
        # get back to start dir
        os.chdir(current_dir)

        self.assertTrue(test_message in server.messages)
    
    @unittest.skip('need to fix path_maplist being modified in config first')
    def test_server_can_report_start_map(self):
        # reading first map from maplist
        modpath = self.launch_args.split(' ')[1]
        path_maplist = os.path.join(self.path_game_root_relative, modpath, rr_config.C['PATH_MAPLIST'])
        with open(path_maplist) as maplist:
            for line in maplist:
                print(line)
        
        self.skipTest('Finished reading maplist')
        
        timeout_message = 'TIMEOUT'

        # Start fake server in background thread
        client = rr_mocks.MockNetwork(rr_config).client
        server = rr_mocks.MockNetwork(rr_config).server
        server.exit_flags.append(test_message)
        server.exit_flags.append(timeout_message)
        server_thread = threading.Thread(target=server.runner_fake_server)
        server_thread.start()

        start_time = time.time()
        timeout = 10.640 # seconds should be enough for everyone

        current_dir = os.getcwd()
        # for some reason bf2 can't find it's modules otherwise
        os.chdir(self.path_game_root_relative)
        launch_string = '"' + self.name_exe + '"' + ' ' + self.launch_args
        # starting game server
        game_server = subprocess.Popen(launch_string, shell=False)

        # Start client sending messages
        while 1:
            if test_message in server.messages:
                # Ensure server thread ends
                server_thread.join()
                break
            if not server_thread.isAlive():
                # skipping test if we could not create listening server
                self.skipTest('Failed to create UDP server thread')
            if time.time() - start_time > timeout:
                client.send_message(timeout_message, rr_config.C['CLIENTHOST'], rr_config.C['CLIENTPORT'])
                server_thread.join()
                break
        
        # terminate game server
        game_server.terminate()
        # get back to start dir
        os.chdir(current_dir)

        self.assertTrue(test_message in server.messages)
        

if __name__ == '__main__':
    unittest.main()
