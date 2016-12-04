import os

#import bf2
#import host

#import rr_debugger as D
#import rr_config_maps as C


class MapsController:

    def __init__(self, interface):
        #self.g_path_mod = host.sgl_getModDirectory()
        self.g_path_mod = interface.get_mod_directory()
        #self.g_path_mod = 'D:\\Games\\Project Reality\\mods\\pr\\python\\game\\rr_maps'
        self.g_path_settings = os.path.join(self.g_path_mod, 'settings')
        self.g_path_maplist = os.path.join(
            self.g_path_mod, 'settings', 'maplist.con')
        self.g_map_at_server_start = self.get_first_map_in_maplist(
            self.g_path_maplist)

    def get_first_map_in_maplist(self, path_maplist):
        # mapList.append sbeneh_outskirts gpm_vehicles 64
        try:
            with open(path_maplist) as maplist:
                map_string = maplist.readline()
            map_string_parts = map_string.split(' ')
            map_name = map_string_parts[1]
            map_gamemode = map_string_parts[2]
            map_layer = map_string_parts[3]
        except:
            # failed to get start map
            map_name = 'asad_khal'
            map_gamemode = 'gpm_skirmish'
            map_layer = '16'

        return (map_name, map_gamemode, map_layer)
