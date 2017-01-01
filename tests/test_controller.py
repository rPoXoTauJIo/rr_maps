import sys
import unittest
import tempfile
import os
import shutil

import rr_mocks
g_host = rr_mocks.host()
g_bf2 = rr_mocks.bf2(g_host)
g_game = rr_mocks.game(g_host)
g_realiylogger = rr_mocks.realitylogger(g_host)
sys.modules['host'] = g_host
sys.modules['bf2'] = g_bf2
sys.modules['game'] = g_game
sys.modules['game'].realitylogger = g_realiylogger

import rr_config
g_config = rr_config
sys.modules['rr_config'] = g_config

import rr_controller


class TestController(unittest.TestCase):

    def setUp(self):
        global g_host

        reload(rr_mocks)

        g_host = rr_mocks.host()
        g_bf2 = rr_mocks.bf2(g_host)
        g_game = rr_mocks.game(g_host)
        g_realiylogger = rr_mocks.realitylogger(g_game)
        sys.modules['host'] = g_host
        sys.modules['bf2'] = g_bf2
        sys.modules['game'] = g_game
        sys.modules['game'].realitylogger = g_realiylogger

        reload(rr_controller)

    def test_init_controller(self):
        controller = rr_controller.MapsController()
        self.assertIsInstance(controller, rr_controller.MapsController)

    def test_controller_can_get_current_map_name(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertTrue(controller.get_current_map_name() is map_mock[0], str(
            controller.get_current_map()) + ' is not ' + str(map_mock[0]))

    def test_controller_can_get_current_map_gamemode(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertTrue(controller.get_current_map_gamemode() is map_mock[1], str(
            controller.get_current_map()) + ' is not ' + str(map_mock[1]))

    @unittest.skip("backport layer algorithm from realitycore")
    def test_controller_can_get_current_map_layer(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertTrue(controller.get_current_map_layer() is map_mock[2], str(
            controller.get_current_map()) + ' is not ' + str(map_mock[2]))
        self.fail("backport layer algorithm from realitycore")

    def test_controller_cannot_get_current_non64_layer(self):
        map_mock = ('test_airfield', 'gpm_cq', 32)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertNotEqual(controller.get_current_map_layer(), map_mock[2])

    def test_controller_can_get_current_map(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertEqual(controller.get_current_map(), map_mock)

    def test_controller_can_get_maplist_engine(self):
        maplist_mock = [
            ('0:', '"map_1"', 'gamemode_1', 'size_1'),
            ('1:', '"map_2"', 'gamemode_2', 'size_2'),
            ('2:', '"map_3"', 'gamemode_3', 'size_3'),
            ('3:', '"map_4"', 'gamemode_4', 'size_4'),
            ('')  # bf2 maplist always ending with whitestring
        ]

        g_host._game._state._maplist = '\n'.join(
            (' '.join(entry) for entry in maplist_mock))

        controller = rr_controller.MapsController()
        self.assertEqual(controller.get_current_maplist_engine(), '\n'.join(
            ' '.join(entry) for entry in maplist_mock).strip().split('\n'))

    @unittest.skip("future stuff")
    def test_controller_filter_maplist_by_group(self):
        maplist_mock = [
            ('0:', '"map_1"', 'gamemode_1', 'size_1'),
            ('1:', '"map_1"', 'gamemode_1', 'size_2'),
            ('2:', '"map_1"', 'gamemode_1', 'size_3'),
            ('3:', '"map_2"', 'gamemode_2', 'size_2'),
            ('4:', '"map_2"', 'gamemode_2', 'size_3'),
            ('5:', '"map_3"', 'gamemode_1', 'size_1'),
            ('6:', '"map_3"', 'gamemode_1', 'size_3'),
            ('7:', '"map_4"', 'gamemode_1', 'size_3'),
            ('8:', '"map_4"', 'gamemode_2', 'size_1'),
            ('9:', '"map_4"', 'gamemode_2', 'size_3'),
            ('')  # bf2 maplist always ending with whitestring
        ]
        groups_mock = {
            'group_1': [  # represebtin aas big
                'map_1|gamemode_1|size_2',
                'map_1|gamemode_1|size_3',
                'map_3|gamemode_1|size_3',
                'map_4|gamemode_1|size_3',
            ],
            'group_2': [  # ins big
                'map_2|gamemode_2|size_2',
                'map_2|gamemode_2|size_3',
                'map_4|gamemode_2|size_3',
            ],
            'group_3': [  # small
                'map_1|gamemode_1|size_1',
                'map_2|gamemode_2|size_2',
                'map_3|gamemode_1|size_1',
            ],
            'group_4': [  # seed
                'map_1|gamemode_1|size_1',
                'map_3|gamemode_1|size_1',
            ],
        }
        num_players_mock = {  # probability of group depending on player num
            # should be in external .ini file
            20: {
                'group_4': 1.0,
                'group_3': 0.3
            },
            54: {
                'group_1': 0.8,
                'group_3': 1.0
            },
            80: {
                'group_1': 1.0,
                'group_2': 0.4
            }
        }

        controller = rr_controller.MapsController()

    def test_controller_can_locate_maplist_file(self):
        mock_path_base = tempfile.mkdtemp()
        g_host._game._dir = mock_path_base
        mock_path_maplist = tempfile.NamedTemporaryFile(
            dir=mock_path_base,
            delete=False
        )
        mock_path_maplist.close()
        g_config.C['PATH_MAPLIST'] = os.path.split(mock_path_maplist.name)[1]

        controller = rr_controller.MapsController()
        path_maplist = controller.get_path_maplist()
        self.assertTrue(os.path.exists(path_maplist))
        shutil.rmtree(mock_path_base)

    def test_controller_can_locate_base_path(self):
        mock_path_base = tempfile.mkdtemp()
        g_host._game._dir = mock_path_base

        controller = rr_controller.MapsController()
        self.assertEqual(controller.get_path_base(), mock_path_base)
        shutil.rmtree(mock_path_base)

    def test_controller_can_read_maplist_file(self):
        maplist_mock = [
            ('0:', '"map_1"', 'gamemode_1', 'size_1'),
            ('1:', '"map_1"', 'gamemode_1', 'size_2'),
            ('2:', '"map_1"', 'gamemode_1', 'size_3'),
            ('3:', '"map_2"', 'gamemode_2', 'size_2'),
            ('4:', '"map_2"', 'gamemode_2', 'size_3'),
            ('5:', '"map_3"', 'gamemode_1', 'size_1'),
            ('6:', '"map_3"', 'gamemode_1', 'size_3'),
            ('7:', '"map_4"', 'gamemode_1', 'size_3'),
            ('8:', '"map_4"', 'gamemode_2', 'size_1'),
            ('9:', '"map_4"', 'gamemode_2', 'size_3'),
            ('')  # bf2 maplist always ending with whitestring
        ]
        mock_path_base = tempfile.mkdtemp()
        g_host._game._dir = mock_path_base
        with tempfile.NamedTemporaryFile(dir=mock_path_base, delete=False) as temp:
            maps = '\n'.join(
                ('mapList.append ' + ' '.join(entry[1:]) for entry in maplist_mock[:-1])) + '\n'
            temp.write(maps)
            mock_path_maplist = temp.name
            mock_path_maplist_name = os.path.split(temp.name)[1]
            g_config.C['PATH_MAPLIST'] = mock_path_maplist_name

        controller = rr_controller.MapsController()
        maplist = controller.get_current_maplist_file()
        self.assertEqual(maplist, maps, 'temp maplist in %s' %
                         (mock_path_maplist))
        # this won't execute if assertEqual will raise
        shutil.rmtree(mock_path_base)
    
    def test_controller_can_read_and_filter_maplist_file(self):
        maplist_mock = [
            ('0:', '"map_1"', 'gamemode_1', 'size_1'),
            ('1:', '"map_1"', 'gamemode_1', 'size_2'),
            ('2:', '"map_1"', 'gamemode_1', 'size_3'),
            ('3:', '"map_2"', 'gamemode_2', 'size_2'),
            ('4:', '"map_2"', 'gamemode_2', 'size_3'),
            ('5:', '"map_3"', 'gamemode_1', 'size_1'),
            ('6:', '"map_3"', 'gamemode_1', 'size_3'),
            ('7:', '"map_4"', 'gamemode_1', 'size_3'),
            ('8:', '"map_4"', 'gamemode_2', 'size_1'),
            ('9:', '"map_4"', 'gamemode_2', 'size_3'),
            ('')  # bf2 maplist always ending with whitestring
        ]
        mock_path_base = tempfile.mkdtemp()
        g_host._game._dir = mock_path_base
        with tempfile.NamedTemporaryFile(dir=mock_path_base, delete=False) as temp:
            remmed_strings = [
                'rem this is example of 1st single remmed string',
                'rem this is example of 2nd single remmed string',
                'beginrem',
                '========================================',
                'this is example of multiline remmed text',
                'this is example of multiline remmed text',
                '========================================',
                'endrem'
                ]
            for line in remmed_strings:
                temp.write(line+'\n')
            maps = '\n'.join(
                ('mapList.append ' + ' '.join(entry[1:]) for entry in maplist_mock[:-1])) + '\n'
            temp.write(maps)
            mock_path_maplist = temp.name
            mock_path_maplist_name = os.path.split(temp.name)[1]
            g_config.C['PATH_MAPLIST'] = mock_path_maplist_name

        controller = rr_controller.MapsController()
        filtered_maplist = controller.get_current_maplist_file_filtered()
        filtered_mock_maplist = maps.split('\n')[:-1]
        self.assertEqual(filtered_maplist, filtered_mock_maplist, 'maplist:\n%s\nmaps:\n%s\ntemp maplist in %s' %
                         (filtered_maplist, filtered_mock_maplist, mock_path_maplist))
        # this won't execute if assertEqual will raise
        shutil.rmtree(mock_path_base)
    
    def test_controller_can_get_random_start_map(self):
        maplist_mock = [
            ('0:', '"map_1"', 'gamemode_1', 'size_1'),
            ('1:', '"map_1"', 'gamemode_1', 'size_2'),
            ('2:', '"map_1"', 'gamemode_1', 'size_3'),
            ('3:', '"map_2"', 'gamemode_2', 'size_2'),
            ('4:', '"map_2"', 'gamemode_2', 'size_3'),
            ('5:', '"map_3"', 'gamemode_1', 'size_1'),
            ('6:', '"map_3"', 'gamemode_1', 'size_3'),
            ('7:', '"map_4"', 'gamemode_1', 'size_3'),
            ('8:', '"map_4"', 'gamemode_2', 'size_1'),
            ('9:', '"map_4"', 'gamemode_2', 'size_3'),
            ('')  # bf2 maplist always ending with whitestring
        ]
        g_host._game._state._maplist = '\n'.join(
            (' '.join(entry) for entry in maplist_mock))
        
        controller = rr_controller.MapsController()
        self.assertIn(controller.get_random_start_map(), g_host._game._state._maplist, 'temp maplist in %s' %
                         (g_host._game._state._maplist))
        choose1 = controller.get_random_start_map()
        choose2 = controller.get_random_start_map()
        while choose2 == choose1:
            choose2 = controller.get_random_start_map()
        self.assertNotEqual(choose1, choose2)
    
    def test_controller_can_add_map_to_start_of_maplist_fo(self):
        maplist_mock = [
            ('0:', '"map_1"', 'gamemode_1', 'size_1'),
            ('1:', '"map_1"', 'gamemode_1', 'size_2'),
            ('2:', '"map_1"', 'gamemode_1', 'size_3'),
            ('3:', '"map_2"', 'gamemode_2', 'size_2'),
            ('4:', '"map_2"', 'gamemode_2', 'size_3'),
            ('5:', '"map_3"', 'gamemode_1', 'size_1'),
            ('6:', '"map_3"', 'gamemode_1', 'size_3'),
            ('7:', '"map_4"', 'gamemode_1', 'size_3'),
            ('8:', '"map_4"', 'gamemode_2', 'size_1'),
            ('9:', '"map_4"', 'gamemode_2', 'size_3'),
            ('')  # bf2 maplist always ending with whitestring
            ]
        mock_path_base = tempfile.mkdtemp()
        g_host._game._dir = mock_path_base
        with tempfile.NamedTemporaryFile(dir=mock_path_base, delete=False) as temp:
            maps = '\n'.join(
                ('mapList.append ' + ' '.join(entry[1:]) for entry in maplist_mock[:-1])) + '\n'
            temp.write(maps)
            mock_path_maplist = temp.name
            mock_path_maplist_name = os.path.split(temp.name)[1]
            g_config.C['PATH_MAPLIST'] = mock_path_maplist_name

        controller = rr_controller.MapsController()
        mock_original_maplist = controller.get_current_maplist_file()
        mock_random_start_map = ('map_1', 'gamemode_1', 'size_1')
        controller.add_map_start_to_maplist_fo(mock_random_start_map)
        
        new_maplist = controller.get_current_maplist_file()
        
        with open(mock_path_maplist) as temp_maplist_fo:
            mock_map_string = 'mapList.append "%s" %s %s' % (mock_random_start_map)
            temp_first_map = temp_maplist_fo.readlines()[0].strip() # fix for \n
            self.assertEqual(mock_map_string, temp_first_map, 'maplist in %s' % mock_path_maplist)

        # this won't execute if assertEqual will raise
        shutil.rmtree(mock_path_base)

if __name__ == '__main__':
    unittest.main()
