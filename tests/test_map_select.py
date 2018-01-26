import sys
import unittest
import tempfile
import os
import shutil

import bf2mocks

class TestMapSelect(unittest.TestCase):

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
    
    def test_can_filter_current_map(self):
        mock_current_map = ('test_airfield', 'gpm_cq', 64)
        mock_maplist = [
            ('test_airfield', 'gpm_cq', 64),
            ('test_bootcamp', 'gpm_cq', 64),
            ]
        ms_main.host._game._state._map = mock_current_map
        ms_main.host._game._state._maplist = mock_maplist

        self.assertNotIn(mock_current_map, ms_main.filtered_maplist_current(mock_maplist))


if __name__ == '__main__':
    unittest.main()
