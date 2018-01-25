# ------------------------------------------------------------------------
# Project Reality debug module by rPoXo
#
# Description:
#
#   Provides various debug for modules
#
# ------------------------------------------------------------------------

# game core modules
import host

def _debug_echo(msg):
    try:
        host.rcon_invoke('echo "%s"' % (str(msg)))
        return True
    except:
        host.rcon_invoke('echo "_debug_echo(): failed to display message"')
        return False

def _debug_ingame(msg):
    try:
        host.rcon_invoke('game.sayAll "%s"' % (str(msg)))
        return True
    except:
        host.rcon_invoke(
            'game.sayAll "_debug_ingame(): failed to send message"')
        return False
