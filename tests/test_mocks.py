import os
import unittest

import bf2mocks

class TestHost(unittest.TestCase):
    
    def setUp(self):
        self.host = bf2mocks.host()

    def test_can_register_game_status_handler(self):
        def mock_onGameStatusChanged(status):
            pass
        
        self.host.registerGameStatusHandler(mock_onGameStatusChanged)
        self.assertTrue(mock_onGameStatusChanged in self.host._GameStatusHandlers)
    
    def test_can_return_modDir(self):
        self.host._game._dir = 'mods/pr'
        self.assertEqual(self.host.sgl_getModDirectory(), 'mods/pr')

    def test_can_return_ss_getParam(self):
        for param in self.host._params.keys():
            self.assertEqual(self.host.ss_getParam(param), self.host._params[key])
    
    def test_can_return_mapname(self):
        self.assertEqual(self.host.sgl_getMapName(), None)
    
    def test_can_invoke_rcon_command_echo(self):
        self.host.rcon_invoke('echo echo')
        self.assertIn('echo', self.host._game._state._echo)
    
    def test_can_sanitize_quotes_rcon_command_echo(self):
        self.host.rcon_invoke('echo "echo"')
        self.assertTrue(self.host._game._state._echo[-1] == 'echo')
        self.assertTrue(self.host._game._state._echo[-1] != '"echo"')
        
        self.host.rcon_invoke("echo 'echo'")
        self.assertTrue(self.host._game._state._echo[-1] == "'echo'")
        self.assertTrue(self.host._game._state._echo[-1] != "echo")
    
    def test_can_invoke_rcon_command_sayall(self):
        self.host.rcon_invoke('game.sayAll "sayall"')
        self.assertIn('sayall', self.host._game._state._chat['server'])
    
    def test_can_sanitize_quotes_rcon_command_sayall(self):
        self.host.rcon_invoke('game.sayAll "sayall"')
        self.assertTrue(self.host._game._state._chat['server'][-1] == 'sayall')
        self.assertTrue(self.host._game._state._chat['server'][-1] != '"sayall"')
        
        self.host.rcon_invoke("game.sayAll 'sayall'")
        self.assertTrue(self.host._game._state._chat['server'][-1] == "'sayall'")
        self.assertTrue(self.host._game._state._chat['server'][-1] != "sayall")
    
    def test_can_invoke_rcon_command_maplist(self):
        maplist = self.host.rcon_invoke('maplist.list')
        self.assertEqual(maplist, self.host._game._state._maplist)


# bf2 is purely OO wrapper around engine host binding
class TestBf2(unittest.TestCase):
    
    def setUp(self):
        self.host = bf2mocks.host()
        self.bf2 = bf2mocks.bf2(self.host)
    
    def test_can_get_mapname(self):
        self.host._game._state._map = ('test_airfield', 'gpm_cq', 64)
        
        self.assertTrue(self.bf2.gameLogic.getMapName() == 'test_airfield')
    
    def test_can_get_gamemode(self):
        self.host._game._state._map = ('test_airfield', 'gpm_cq', 64)

        self.assertTrue(self.bf2.serverSettings.getGameMode() == 'gpm_cq')
    
    def test_can_get_moddir(self):
        self.host._game._dir = 'mods/pr'

        self.assertEqual(self.bf2.gameLogic.getModDir(), 'mods/pr')
        self.assertEqual(self.bf2.gameLogic.getModDir(), self.host.sgl_getModDirectory())

if __name__ == '__main__':
    unittest.main()