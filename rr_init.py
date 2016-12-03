import bf2
import host
import game.realitylogger as rlogger

import rr_interface
import rr_debugger
#import rr_maps


def init():
    interface = rr_interface.Interface(bf2, host, rlogger)
    debugger = rr_debugger.Debugger(interface)