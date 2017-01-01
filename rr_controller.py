import bf2
import host

# custom modules
#from rr_debugger import Debugger as D
from rr_config import C

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
    
    def get_path_maplist(self):
        return C['PATH_MAPLIST']
    
    def get_path_base(self):
        return bf2.gameLogic.getModDir()
    
    def get_current_maplist_file(self): # context managers not working with i\o in bf2
        maplist_fo = open(self.get_path_maplist())
        maplist = maplist_fo.read()
        return maplist
    
    def get_current_maplist_engine(self):
        return host.rcon_invoke( "maplist.list" )