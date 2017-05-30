import host
import config
import debugger
import controller

def init():
    debug = debugger.Debugger(config.C)
    # for integration testing
    debug.message('INIT: Server initialized', ['echo', 'udp'])
    control = controller.MapsController()
    #maplist = controller.get_current_maplist_engine()
    # for entry in maplist:
    #    debugger._debug_echo(entry)
    #debugger._debug_file('len maplist(%s)' % (len(maplist)))
    #debugger._debug_file(controller.get_path_base())
    #debugger._debug_file(controller.get_path_maplist())
    #debugger._debug_file('finished maplist')
    
