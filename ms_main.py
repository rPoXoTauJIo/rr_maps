import os

import host
import bf2 # dice OO wrapper for host engine binding

# custom logger
import ms_logger as logger

def init():
    # init_serverstart
    #  get current map
    #  increase rating(current)
    #   write stats file
    # force select next
    #  exclude current
    #  exclude by filter
    #  exclude by numbers
    #   
    host.registerGameStatusHandler(onGameStatusChanged)

def deinit():
    host.unregisterGameStatusHandler(onGameStatusChanged)

# ------------------------------------------------------------------------
# onGameStatusChanged
# ------------------------------------------------------------------------
def onGameStatusChanged(status):

    #if status == bf2.GameStatus.Playing:
        # registering chatMessage handler
        #host.registerHandler('ChatMessage', onChatMessage, 1)

        # test stuff
        #select_timer = rtimer.Timer(setTestVehicle, 3, 1, 'us_jet_a10a')

        # test stuff2
        #host.registerHandler('EnterVehicle', onEnterVehicle)
        #host.registerHandler('ExitVehicle', onExitVehicle)
    pass
    
def get_path_settings_dir():
	return os.path.join(bf2.gameLogic.getModDir(), 'settings')
	
def get_path_maplist():
	return os.path.join(get_path_settings_dir(), 'maplist.con')

def set_start_map(map):
    with open(get_path_maplist(), 'wb') as fo:
        fo.write('rem do not edit, all changes will be overwritten by server\n')
        fo.write('mapList.append %s\n' % (' '.join([str(_) for _ in map])))