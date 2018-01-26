import sys
import unittest
import tempfile
import os
import shutil

import bf2mocks

class TestInitialization(unittest.TestCase):

    def setUp(self):
        self.host = bf2mocks.host()
        self.bf2 = bf2mocks.bf2(self.host)
        sys.modules['host'] = self.host
        sys.modules['bf2'] = self.bf2

        if 'ms_main' not in globals():
            import ms_main

            # weird trick needed so module will be discovered
            #  in global namescape despite being in sys.modules
            global ms_main
        else:
            reload(ms_main)
    
    def test_can_import_host(self):
        self.assertIsInstance(ms_main.host, bf2mocks.host)
    
    def test_can_import_bf2(self):
        self.assertIsInstance(ms_main.bf2, bf2mocks.bf2)

    def test_can_register_game_status_handler(self):
        ms_main.init()
        self.assertIn(ms_main.onGameStatusChanged, ms_main.host._GameStatusHandlers)


if __name__ == '__main__':
    unittest.main()
