import sys
import unittest

import rr_mocks
g_host = rr_mocks.host()
g_bf2 = rr_mocks.bf2(g_host)
sys.modules['host'] = g_host
sys.modules['bf2'] = g_bf2

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
        sys.modules['host'] = g_host
        sys.modules['bf2'] = g_bf2

        reload(rr_controller)

    def test_init_controller(self):
        controller = rr_controller.MapsController()
        self.assertIsInstance(controller, rr_controller.MapsController)
    
    def test_controller_can_get_current_map_name(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertTrue(controller.get_current_map_name() is map_mock[0], str(controller.get_current_map()) + ' is not ' + str(map_mock[0]))
    
    def test_controller_can_get_current_map_gamemode(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertTrue(controller.get_current_map_gamemode() is map_mock[1], str(controller.get_current_map()) + ' is not ' + str(map_mock[1]))
    
    def test_controller_can_get_current_map_layer(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertTrue(controller.get_current_map_layer() is map_mock[2], str(controller.get_current_map()) + ' is not ' + str(map_mock[2]))
        self.fail("backport layer algorithm from realitycore")

    def test_controller_can_get_current_map(self):
        map_mock = ('test_airfield', 'gpm_cq', 64)
        g_host._game._state._map = map_mock

        controller = rr_controller.MapsController()
        self.assertEqual(controller.get_current_map(), map_mock)


if __name__ == '__main__':
    unittest.main()
