import unittest

import rr_mocks
import rr_controller


@unittest.skip('rework')
class TestController(unittest.TestCase):

    def setUp(self):
        self.interface = rr_mocks.MockInterface()

    def tearDown(self):
        del self.interface

    def test_init_controller(self):
        controller = rr_controller.MapsController(self.interface)
        self.assertIsInstance(controller, rr_controller.MapsController)

    def test_controller_can_get_current_map(self):
        mock_map = ('test_airfield', 'gpm_cq', '64')
        self.interface._set_current_map(mock_map)
        controller = rr_controller.MapsController(self.interface)
        current_map = controller.get_current_map()
        self.assert_(current_map is mock_map)


if __name__ == '__main__':
    unittest.main()
