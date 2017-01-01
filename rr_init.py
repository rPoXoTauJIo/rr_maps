import host
import rr_debugger
import rr_controller
#import rr_maps


def init():
    debugger = rr_debugger.Debugger()
    controller = rr_controller.MapsController()
    #maplist = controller.get_current_maplist_engine()
    # for entry in maplist:
    #    debugger._debug_echo(entry)
    maplist = controller.get_path_base()
    #debugger._debug_file('len maplist(%s)' % (len(maplist)))
    debugger._debug_file(maplist)
    #debugger._debug_file('finished maplist')
