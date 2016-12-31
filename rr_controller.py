import bf2
import host

#import rr_debugger as D
#import rr_config_maps as C


class MapsController:

    def __init__(self):
        pass

    def get_current_map(self):
        map_name = self.get_current_map_name()
        map_gamemode = self.get_current_map_gamemode()
        map_layer = self.get_current_map_layer()
        return map_name, map_gamemode, map_layer
    
    def get_current_map_name(self):
        return bf2.gameLogic.getMapName( )
    
    def get_current_map_gamemode(self):
        return bf2.serverSettings.getGameMode( )
    
    def get_current_map_layer(self):
        return 64