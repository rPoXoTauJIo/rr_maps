# vbf2 modules
import bf2
import host

# custom modules
#import rr_debugger as D
#import rr_maps_config as C

g_controller = None

class MapsController:
    
    def __init__(self):
        # global singletone, i'm evil hahaha
        global g_controller
        g_controller = self

        self.g_path_mod = host.sgl_getModDirectory()
        self.g_path_settings = os.path.join([self.path_mod, 'settings'])
        self.g_path_maplist = os.path.join([self.path_mod, 'settings', 'maplist.con'])
        self.g_map_at_server_start = self.get_first_map_in_maplist(self.g_path_maplist)
    
    def deinit(self):
        global g_controller
        g_controller = None

        del self
    
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


# ------------------------------------------------------------------------
# Init
# ------------------------------------------------------------------------
def init():
    g_controller = MapsController()
    host.registerGameStatusHandler(onGameStatusChanged)

# ------------------------------------------------------------------------
# DeInit
# ------------------------------------------------------------------------
def deinit():
    g_controller.set_server_start_map()
    g_controller.deinit()
    host.unregisterGameStatusHandler(onGameStatusChanged)


# ------------------------------------------------------------------------
# onGameStatusChanged
# ------------------------------------------------------------------------
def onGameStatusChanged(status):

    if status == bf2.GameStatus.Playing:
        pass
        # registering handlers
        #host.registerHandler( 'ChatMessage', onChatMessage )
        #host.registerHandler( 'EnterVehicle', onEnterVehicle )
        #host.registerHandler( 'ExitVehicle', onExitVehicle )
        #host.registerHandler( 'VehicleDestroyed', onVehicleDestroyed )







