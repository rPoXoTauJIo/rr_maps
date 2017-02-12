import host
import rr_debugger
import rr_controller

def init():
    debugger = rr_debugger.Debugger()
    # for integration testing
    debugger.debugMessage('INIT: Server initialized', ['echo', 'udp'])
    controller = rr_controller.MapsController()
    #maplist = controller.get_current_maplist_engine()
    # for entry in maplist:
    #    debugger._debug_echo(entry)
    #debugger._debug_file('len maplist(%s)' % (len(maplist)))
    #debugger._debug_file(controller.get_path_base())
    #debugger._debug_file(controller.get_path_maplist())
    #debugger._debug_file('finished maplist')
    
