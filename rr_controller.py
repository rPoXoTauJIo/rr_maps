import os
import random

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
        return bf2.gameLogic.getMapName()

    def get_current_map_gamemode(self):
        return bf2.serverSettings.getGameMode()

    def get_current_map_layer(self):
        return 64

    def get_path_maplist(self):
        return os.sep.join([self.get_path_base(), C['PATH_MAPLIST']])

    def get_path_base(self):
        return bf2.gameLogic.getModDir()

    # context managers not working with i\o in bf2
    def get_current_maplist_file(self):
        maplist_fo = open(self.get_path_maplist())
        maplist = maplist_fo.read()
        maplist_fo.close()
        return maplist
    
    def get_current_maplist_file_filtered(self):
        maplist_fo = open(self.get_path_maplist())
        maplist = maplist_fo.readlines()
        maplist_fo.close()
        maplist_filtered = [entry.strip() for entry in maplist if entry.lower().startswith('maplist.append')]
        return maplist_filtered

    def get_current_maplist_engine(self):
        return host.rcon_invoke("maplist.list").strip().split('\n')

    def get_random_start_map(self):
        return random.choice(self.get_current_maplist_engine())
    
    def add_map_start_to_maplist_fo(self, map):
        maplist_fo = open(self.get_path_maplist())
        maplist = maplist_fo.read()
        maplist_fo.close()
        # rewriting file
        maplist_fo = open(self.get_path_maplist(), 'w')
        maplist_fo.write('mapList.append "%s" %s %s\n' % (map))
        maplist_fo.write(maplist)
        maplist_fo.close()
        