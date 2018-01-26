import sys
import unittest
import tempfile
import os
import shutil

import bf2mocks

class TestFileOps(unittest.TestCase):

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

    def test_can_get_path_settings(self):
        self.assertEqual(ms_main.get_path_settings_dir(), os.path.join(ms_main.host._game._dir, 'settings'))
    
    def test_can_get_path_maplist(self):
        self.assertEqual(ms_main.get_path_maplist(), os.path.join(ms_main.host._game._dir, 'settings', 'maplist.con'))

    def test_can_set_start_map(self):
        mock_map = ('test_airfield', 'gpm_cq', 64)
        ms_main.host._game._dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(ms_main.host._game._dir, 'settings'))
        ms_main.set_start_map(mock_map)

        with open(ms_main.bf2.gameLogic.getModDir() + '/settings/maplist.con') as fo:
            maplist = [mapstring for mapstring in fo.read().splitlines() if mapstring.startswith('mapList.append')]
            
            first_map = maplist[0].replace('mapList.append ', '').split(' ')
            first_map[2] = int(first_map[2])
            first_map = tuple(first_map)
            self.assertEqual(first_map, mock_map)


if __name__ == '__main__':
    unittest.main()