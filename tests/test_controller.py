import unittest

import rr_mocks
import rr_controller

class TestController(unittest.TestCase):

    def setUp(self):
        interface = rr_mocks.MockInterface()
        self.controller = rr_controller.MapsController(interface)

    def test_can_init_controller(self):
        self.assertIsInstance(self.controller, rr_controller.MapsController)
    

if __name__ == '__main__':
    unittest.main()