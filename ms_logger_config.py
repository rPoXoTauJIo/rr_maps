# =============================================================================
# Debugger config file
#
#
C = {}
#
#
# Use UDP remote logger
# Default is False
C['DEBUG_UDP'] = False
#
#
# Remote host listening for udp mesages
# Default is localhost
C['REMOTEADDR'] = 'localhost'
#
#
# Remote port
# Default is 8888
C['REMOTEPORT'] = 8888
#
#
# Use file logger
# Default is False
C['DEBUG_FILE'] = True
#
#
# Filename of the admin log file
# Default is "ms_mapscript.log"
C['PATH_LOG_FILENAME'] = "ms_mapscript.log"
#
#
# Path relative to PR root (not mod root) of mapscript log file
# Default is "admin/logs"
C['PATH_LOG_DIRECTORY'] = "admin/logs"
#
#