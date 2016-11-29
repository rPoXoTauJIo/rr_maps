__version__ = 1.15
# Drill's automap v1.15
# All main settings are in 'mods/bf2/Settings/dam.ini' (value of settings_file_name)
# Semi-compatible with modmanager
#
# Warning : modifies maplist.con!
#
# dam.ini could be modified at run-time
#
# Format of dam.ini is:
#   [DAMSettings]
#    MapRotationChoiceSize level_of_randomness
#    ModifyMaplistCon (1,0)
#    DelayForNewMaplistCon seconds                  (if >= 0 - works, < 0 or False - turns off)
#   [MapList]
#    {number_of_players}
#     map_name map_size game_mode [priority](>=0, default value is 1.0)
#     ...
#    ...
#
# Priority determines how often the map appears. Default priority is 1.0 (when no number is written). Priority = 0.0 means that the map is disabled, i.e. it won't be changed to by the script. However, it still could be voted for or could be switched to by admin.
# If map A has priority 1.0, and map B has priority 0.5 - then map A will appear 2 times more often, than map B. If there's also map C with priority 0.25, then map A will appear 4 times more often, than C, and map B - 2 times more often, than C
#
# Example:
#    [DAMSettings]
#     MapRotationChoiceSize 2
#     ModifyMaplistCon 1
#     DelayForNewMaplistCon 1200
#    [MapList]
#     {0}
#      arena gpm_cq 16 0
#      strike_at_karkand gpm_cq 16
#      strike_at_karkand gpm_cq 32 0.5
#      daqing_oilfields gpm_cq 16 
#     {28}
#      strike_at_karkand gpm_cq 32 0.2
#      daqing_oilfields gpm_cq 32 2
#      dragon_valley gpm_cq 32
#
#

__supports_reload__ = True
__supported_games__ = {
	'bf2': True,
	'bf2142': True
}
__description__ = "DAM v%s" % __version__
__required_modules__ = {
	'modmanager': 0.0
}


import bf2
import host
import random
from bf2 import g_debug
import string
import os
import time

# for exception printing
import sys
import inspect
import re
#


# settings
debug = False # if true - mm.debug wouldn't be used
settings_file_name='dam.ini' #relative to mods/mod_name/settings/
maps_run_save_file_name='dam_mapsrun.dat'
g_newmlcon_delay = 900
g_timer_update_rate = 10

#enable_periodic_maplist_update = False
#update_rate = 300 # seconds between updating the maplist


# consts
MAPNAME = 0
GAMEMODE = 1
MAPSIZE = 2

NEEDINIT = 0
STOPPED = 1
RUN = 2

# gvars
state = NEEDINIT
current_map_size = None # None indicating that it's the first map and size couldn't be revealed (but could be read from maplist.con)
mm = None


def Debug(s):
	global mm
	
	if debug: 
		print '.'.join([str(x) for x in time.localtime()[:6]]), 'DAM:', s
	elif mm != None:
		mm.debug(4, s)	
		
def GetSetBasePath():
	return bf2.gameLogic.getModDir()+"/settings/"
	
def GetPathToMaplistCon():
	return GetSetBasePath() + '/maplist.con'

def InitMapsRun():
	global maps_run,maps_run_save_file_name, maps_run_priority
	
	maps_run = []
	maps_run_priority = {}
	try:
		
		Debug('Reading mapsrun...')
		
		mrf=open(GetSetBasePath()+maps_run_save_file_name,'r')
		for l in mrf.readlines():
			spl = [x.strip() for x in string.strip(l).split()]
			if len(spl)>3:
				if len(spl) < 5 or spl[4] != '0':
					maps_run += [' '.join(spl[0:3])]
				maps_run_priority[' '.join(spl[0:3])] = float(spl[3])
		mrf.close()
		
		Debug('Done! Resulting list: %s' % str(maps_run_priority))
		
	except:
		maps_run = []
		maps_run_priority = {}
		
		Debug('Failed to read mapsrun - considering empty')
		

def SaveMapsRun():
	global maps_run,maps_run_save_file_name, maps_run_priority
	try:
		
#		Debug('Saving mapsrun...')
		
		mrf=open(GetSetBasePath()+maps_run_save_file_name,'w')				
		for e in maps_run:
			mrf.write(e+' '+str(maps_run_priority[e])+'\n')
		for e in maps_run_priority:
			if e not in maps_run:
				mrf.write(e+' '+str(maps_run_priority[e])+' 0\n')
		mrf.close()
		
#		Debug('Done!')
		
	except:
		
		Debug('Failed to write mapsrun')

def ReadSettings(fn):
	global g_newmlcon_delay
	
	class CStruct:
		pass
		
	Debug('Reading settings...')
	
	d=ReadDict(fn)
	
	r=CStruct()
	r.rndnum=int(d['DAMSettings']['MapRotationChoiceSize'])
	r.mod_maplistcon = int(d['DAMSettings']['ModifyMaplistCon'])!=0
	
	if 'DelayForNewMaplistCon' in d['DAMSettings']:
		val = d['DAMSettings']['DelayForNewMaplistCon']
		if val.lower() == 'false':
			g_newmlcon_delay = -1
		else:
			g_newmlcon_delay = float(val)
	
	if r.mod_maplistcon == False:
		g_newmlcon_delay = -1
	
	Debug('Done! Settings are: %s' % str(r.__dict__))
	Debug('DelayForNewMaplistCon = %s' % str(g_newmlcon_delay))
	
	return r

def LocateMapInServerMaplist(mn):
	sml = []
	for x in [x[ x.find(':') + 1 :].strip() for x in host.rcon_invoke('mapList.list').split('\n')[:-1]]:
		spl = x.split()
		sml += ['%s %s %s' % (spl[0][1:-1], spl[1], spl[2])]
	
	Debug('LocateMapInServerMaplist: level name "%s", server maplist %s' % (mn, sml))
	
	for i in xrange(len(sml)):
		if mn == sml[i]:
			
			Debug('Found level "%s" at index %s in server maplist' % (mn, i))
			
			return i
			
	Debug('Map "%s" wasn\'t found in server maplist' % mn)
			
	return None
	
def GetServerNextMap():
	mi = int( host.rcon_invoke('admin.nextLevel') )
	sml = []
	for x in [x[ x.find(':') + 1 :].strip() for x in host.rcon_invoke('mapList.list').split('\n')[:-1]]:
		spl = x.split()
		sml += ['%s %s %s' % (spl[0][1:-1], spl[1], spl[2])]
		
	Debug('Getting server next map. Next map index is %s. Server maplist is %s' % (mi, sml))
	
	return sml[mi][ len('') :]

def GetRandomNextMap(ml,rndnum):
	global maps_run
	
	Debug('Choosing next map...')
	
	pnms=[]
	for mn in ml.keys():
		if mn not in maps_run and ml[mn][0] > 0:
			pnms += [mn]
			
			Debug('Map not in mapsrun: %s' % str(mn))
			
	npnum=len(pnms)
	for mn in maps_run:
		if mn in ml and ml[mn][0] > 0:
			pnms+=[mn]
			
			Debug('Map from mapsrun: %s' % str(mn))
			
	for mn in ml.keys():
		if ml[mn][0] == 0:
			Debug('Disabled map: %s' % str(mn))
			
	if npnum>0:
		pnms=pnms[0:npnum]
	elif rndnum>=len(pnms):
		pnms=pnms[0:-1]
	else:
		pnms=pnms[0:rndnum]
	
	Debug('Resulting list of candidates: %s' % str(pnms))
	
	rc = random.choice(pnms)
	
	Debug('Choosing next map is done! Returning "%s"' % str(rc))
	
	return rc
	
def MoveToEndOfMapsRun(mn):
	global maps_run, maps_run_priority
	
	Debug('Adding "%s" at the end of mapsrun list' % str(mn))
	
	while mn in maps_run:
		maps_run.remove(mn)
	maps_run += [mn]
	SaveMapsRun()
	
	Debug('Done!')
	

def GetCurrentMapList(fn, numpl = None):
	global maps_run
	
	Debug('Reading current maplist')
	
	d = ReadDict_MultiplyDatas(fn)
	if numpl == None: numpl = len(bf2.playerManager.getPlayers())

	d = d['MapList']
	mls=[]
	sk=[int(el) for el in d.keys()]
	sk.sort()
	maxprior = float(0)
	for sd in sk:
		ml={}
		for mn in d[str(sd)]:
			for data in d[str(sd)][mn]:
				spl=data.strip().split()
				if len(spl) < 3:
					spl += ['1']
				ml['%s %s %s' % (mn, spl[0], spl[1])]= [float(spl[2])] # mapname,gamemode,size = priority
				maxprior = max([float(spl[2]), maxprior])
		mls+=[[sd,ml]]
	np=numpl
	ml=mls[-1][1]
	for i in xrange(len(mls)):
		if mls[i][0]>np:
			
			Debug('Using maplist {%s} (currently %s players on the server): %s' % (mls[i-1][0], np,mls[i-1][1]) )
			
			ml=mls[i-1][1]
			break
	Debug('MaxPrior is %s. Normalizing maplist' % str(maxprior))
	for e in ml:
		ml[e][0] /= maxprior
	Debug('Done reading maplist!')
	return ml		

def SetMapList(ml):
	host.rcon_invoke('maplist.clear')
	sk=ml.keys()
	sk.sort()
	for mn in sk:
		spl = mn.split()
		host.rcon_invoke('maplist.append %s %s %s' % ( spl[MAPNAME], spl[GAMEMODE], spl[MAPSIZE] ))
	host.rcon_invoke('admin.setnextlevel 0')
	
def SetMap(mn):
	host.rcon_invoke('maplist.clear')
	spl = mn.split()
	host.rcon_invoke('maplist.append %s %s %s' % (spl[MAPNAME], spl[GAMEMODE], spl[MAPSIZE]))
	host.rcon_invoke('admin.setnextlevel 0')

def init():
	global g_playing, g_timer, state, g_need_choose_map, g_ml_game_start_time

#	if g_debug: 
	print 'initializing Drill\'s AutoMap'

	g_playing = False
	g_need_choose_map = True
	g_ml_game_start_time = None
	
	g_timer = bf2.Timer(onTimer, g_timer_update_rate, 1)
	g_timer.setRecurring(g_timer_update_rate)
	
	InitMapsRun()

	random.seed()
	host.registerGameStatusHandler(onGameStatusChanged)
	
	init_mapchanal()
	
	state = RUN
	
def onTimer(data):
	global g_playing, g_ml_game_start_time
	
	try:
		if state != RUN:
			return
		if not g_playing or g_ml_game_start_time == None or g_newmlcon_delay < 0:
			return
		
		tel = host.timer_getWallTime() - g_ml_game_start_time
		ttel = g_newmlcon_delay + float(host.rcon_invoke('sv.startDelay'))
		Debug('OnTimer. Time elapsed %s/%s' % (tel, ttel))

		if tel >= ttel:
			open(GetPathToMaplistCon(), 'wb').write('mapList.append %s' % GetServerNextMap())
			g_ml_game_start_time = None
			
	except:
		ExceptionOutput()		

def onGameStatusChanged(status):
	global ml,settings_file_name, current_map_size, g_playing, maps_run_priority, g_need_choose_map, g_ml_game_start_time
	
	try:
		onGameStatusChanged_mapchanal(status)
	except:
		ExceptionOutput()
	
	if state != RUN:
		return
	
	try:

		Debug('onGameStatusChanged begins. Status is %s' % str(status))
		
		set=ReadSettings(GetSetBasePath()+settings_file_name)

		if status == bf2.GameStatus.Playing:
			Debug('bf2.GameStatus.Playing')
			g_playing = True
			
			if CurrentRound() == 0 and len(bf2.playerManager.getPlayers()) >= int(host.rcon_invoke('sv.numPlayersNeededToStart')):
				g_ml_game_start_time = host.timer_getWallTime()
				
				Debug('Start playing map for real. Remembering time for maplist.con update: %s' % str(g_ml_game_start_time) )
			
			if not g_need_choose_map and CurrentRound() > 0:
				Debug('Marked as done. Don\'t choosing next map and returning')
				Debug('onGameStatusChanged ends')
				
				return
			g_need_choose_map = False
			
			if current_map_size == None:
				
				Debug('Reading current level size in maplist.con')
				
				try:
					for raw_line in open(GetPathToMaplistCon(), 'rb'):
						l = raw_line.strip()
						if l.lower().startswith('maplist.append'):
							
							Debug('Found first map entry: %s' % l)
							
							current_map_size = str(int(l.split()[3]))
				except:
					pass
			
			ml=GetCurrentMapList(GetSetBasePath()+settings_file_name)
			
			if current_map_size != None:
				mn = '%s %s %s' % (bf2.serverSettings.getMapName(), bf2.serverSettings.getGameMode(), current_map_size)
				
				if mn not in maps_run_priority:
					if mn in ml:
						maps_run_priority[mn] = ml[mn][0]
					else:
						maps_run_priority[mn] = 0
				MoveToEndOfMapsRun(mn)
				
				Debug('Current map is "%s"' % str(mn))

			SetMapList(ml)
			for i in xrange(1000): # not using while true: to prevent possible infinite loop
				nmn=GetRandomNextMap(ml,set.rndnum)
				
				Debug('Map chosen: %s' % nmn)
				
				if nmn not in maps_run_priority:
					maps_run_priority[nmn] = ml[nmn][0]
					SaveMapsRun()
					
				if maps_run_priority[nmn] < 1:
					maps_run_priority[nmn] += ml[nmn][0]
					
					Debug('Map\'s priority value < 1. Increasing it (new value is %s) and moving map to the end of mapsrun. Choosing another map' % str(maps_run_priority[nmn]))
					
					MoveToEndOfMapsRun(nmn)
				elif LocateMapInServerMaplist(nmn) == None:
					
					Debug('Map wasn\'t found in server maplist! Maybe it\'s wrong level name "%s"?' % nmn)
					
					MoveToEndOfMapsRun(nmn)
				else:
					Debug('Setting map as next')
					
					break
				
#			sk=ml.keys()
#			sk.sort()
#			nmi=sk.index(nmn)
			host.rcon_invoke('admin.setnextlevel %d' % LocateMapInServerMaplist(nmn))
			
		if status == bf2.GameStatus.EndGame:
			Debug('bf2.GameStatus.EndGame')
			
			g_playing = False
			
			if isGonnaChangeMap():
				g_need_choose_map = True
				g_ml_game_start_time = None
				
				smn = GetServerNextMap()
			
				ml=GetCurrentMapList(GetSetBasePath()+settings_file_name)
				
				nmn = None
				smnspl = smn.split()
				
				if smn in ml:
					nmn = smn
					
					Debug('Level was found in current maplist')
				
				if nmn == None:
					pmns = [x for x in ml if x.split()[MAPNAME] == smnspl[MAPNAME] and x.split()[GAMEMODE] == smnspl[GAMEMODE]]
					if len(pmns) == 0:
						pmns = [x for x in ml if x.split()[MAPNAME] == smnspl[MAPNAME]]
					if len(pmns) > 0:
						nmn = random.choice(pmns)
						
						Debug('Level(s) with same mapname and gamemode or only mapname was found in current maplist. pnms %s' % str(pmns))
						
				if nmn == None:
					Debug('No resembling level was found in current maplist. Full rechoose')
					
					nmn=GetRandomNextMap(ml,set.rndnum)
					
				Debug('Resulting mapname is %s' % nmn)
					
				SetMap(nmn)
			
				current_map_size = nmn.split()[MAPSIZE]
				if set.mod_maplistcon:
					open(GetPathToMaplistCon(), 'wb').write('mapList.append %s' % nmn)
				if nmn in maps_run_priority:
					maps_run_priority[nmn] %= 1
				else:
					maps_run_priority[nmn] = 0
				maps_run_priority[nmn] += ml[nmn][0]
				SaveMapsRun()
				
				Debug('Reseting priority value of map "%s". New value is %s' % (nmn, maps_run_priority[nmn]))


		
		Debug('onGameStatusChanged ends')
	except:
		ExceptionOutput()		

#########################################################

def ReadDict(fn):
	file=open(fn,'r')
	ls=file.readlines()
	file.close()
	r={}
	cur_sec=None
	cur_subsec=None
	
	for l in ls:
		l=string.strip(l)
		if len(l)>0:
			if l[0]=='[':
				loc=string.find(l,']')
				cur_sec=l[1:loc]
				cur_subsec = None
				r[cur_sec]={}
			elif l[0]=='{':
				if cur_sec==None:
					raise Exception('ReadDict():Creating subsection while there\'s no any section! Filename:%s' % fn)
				loc=string.find(l,'}')
				cur_subsec=l[1:loc]
				r[cur_sec][cur_subsec]={}
			elif l[0] in string.letters or l[0] in string.digits:
				if cur_sec==None:
					raise Exception('ReadDict():Creating entry while there\'s no any section! Filename:%s' % fn)
				loc=string.find(l,' ')
				if loc>=0:
					entryname=l[0:loc]
					data=l[loc+1:]
				else:
					entryname=l[:]
					data=''
				if cur_subsec!=None:
					r[cur_sec][cur_subsec][entryname]=data
				else:
					r[cur_sec][entryname]=data
	return r


def ReadDict_MultiplyDatas(fn):
	file=open(fn,'r')
	ls=file.readlines()
	file.close()
	r={}
	cur_sec=None
	cur_subsec=None
	
	for l in ls:
		l=string.strip(l)
		if len(l)>0:
			if l[0]=='[':
				loc=string.find(l,']')
				cur_sec=l[1:loc]
				cur_subsec = None
				r[cur_sec]={}
			elif l[0]=='{':
				if cur_sec==None:
					raise Exception('ReadDict():Creating subsection while there\'s no any section! Filename:%s' % fn)
				loc=string.find(l,'}')
				cur_subsec=l[1:loc]
				r[cur_sec][cur_subsec]={}
			elif l[0] in string.letters or l[0] in string.digits:
				if cur_sec==None:
					raise Exception('ReadDict():Creating entry while there\'s no any section! Filename:%s' % fn)
				loc=string.find(l,' ')
				if loc>=0:
					entryname=l[0:loc]
					data=l[loc+1:]
				else:
					entryname=l[:]
					data=''
				if cur_subsec!=None:
					if entryname in r[cur_sec][cur_subsec]:
						r[cur_sec][cur_subsec][entryname] += [data]
					else:
						r[cur_sec][cur_subsec][entryname] = [data]
				else:
					if entryname in r[cur_sec]:
						r[cur_sec][entryname] += [data]
					else:
						r[cur_sec][entryname] = [data]
	return r


################################################

def ExceptionOutput():
	print "\n" + "Exception Occured: " + str(sys.exc_info()[0])
	print "Value: " + str(sys.exc_info()[1])
	print "Line:" + str(readline(inspect.getfile(sys.exc_info()[2]),sys.exc_info()[2].tb_lineno))
	print "Line #: " + str(sys.exc_info()[2].tb_lineno)
	print "File: " + str(inspect.getfile(sys.exc_info()[2])) + "\n"
	
def readline(filename,lineno):
	filen = re.sub('\\\\', '/', filename)
	file = open(filen, 'rU')
	lines = file.readlines()
	file.close()
	linen = lineno - 1
	line = re.sub('\s+', ' ', lines[linen])
	return line

# Drill's map change analizator (tool script)
# use isGonnaChangeMap from other scripts to determine if map is going to change (use only at EndGame status)
# should work with time limit

def isGonnaChangeMap():
	global g_ChangingMap
	
	UpdateRoundCounter()
	
	Debug('g_ChangingMap value is %s' % str(g_ChangingMap))
	return g_ChangingMap

def CurrentRound():
	global g_curRound
	
	return g_curRound
	
def ReachedTimeLimit():
	global g_roundStartTime

	tlimit = float(host.rcon_invoke('sv.timeLimit'))
	
	if tlimit == 0:
		Debug("No time limit. Returning False")
		
		return False

	tel = host.timer_getWallTime() - g_roundStartTime - float(host.rcon_invoke('sv.startDelay'))
	res = tel >= tlimit
	
	Debug('ReachedTimeLimit> Time elapsed %s, time limit %s. Result %s' % (tel, tlimit, res))
	
	return res

def isForcedToChangeMap():
	t1 = bf2.gameLogic.getTickets(1)
	t2 = bf2.gameLogic.getTickets(2)
	Debug('isForcedToChangeMap> Tickets are %s, %s' % (t1, t2))
	return (t1 == 0 and t2 == 0) or (t1 > 0 and t2 > 0 and not ReachedTimeLimit())

def RoundsLimit():
	return int(host.rcon_invoke('sv.roundsPerMap'))	

def UpdateRoundCounter():
	global g_curRound,g_chThisRound,g_ChangingMap
	
	if not g_chThisRound:
		Debug('It was %s/%s round' % (g_curRound + 1, RoundsLimit()))
		
		g_chThisRound=True
		g_curRound+=1
	
		if isForcedToChangeMap() or g_curRound>=RoundsLimit():
			Debug('That\'s gonna be mapchange')
			
			g_curRound=0
			g_ChangingMap=True

def init_mapchanal():
	global g_curRound
	global g_lastMapId,g_lastCPNum,g_lastGameMode
	
	g_lastMapId=None
	g_lastCPNum=None
	g_lastGameMode=None
#	if g_debug: print 'initializing Drill\'s mapchange analizator'	
	g_curRound=0	
#	host.registerGameStatusHandler(onGameStatusChanged)

def onGameStatusChanged_mapchanal(status):
	global g_curRound,g_chThisRound,g_ChangingMap
	global g_lastMapId,g_lastCPNum,g_lastGameMode
	global g_roundStartTime
	
	Debug('onGameStatusChanged_mapchanal begins')
	
	if status == bf2.GameStatus.Playing:
		g_roundStartTime = host.timer_getWallTime()
		
		Debug("Remembering start of round time: %s" % str(g_roundStartTime))
		
		g_chThisRound=False
		g_ChangingMap=False
		cmip=bf2.gameLogic.getMapName()
		ccpn=len(bf2.objectManager.getObjectsOfType('dice.hfe.world.ObjectTemplate.ControlPoint'))
		cgm=bf2.serverSettings.getGameMode()
		if cmip!=g_lastMapId or cgm!=g_lastGameMode: #ccpn!=g_lastCPNum or 
			
			Debug('Reseting round counter due to maps description mismatch')
			
			g_curRound=0
			g_lastMapId=cmip
			g_lastCPNum=ccpn
			g_lastGameMode=cgm			
	if status == bf2.GameStatus.EndGame:
		UpdateRoundCounter()
		
	Debug('onGameStatusChanged_mapchanal ends')


#########################################################
## loader for MM

class DAMW:
	def __init__(self):
		return
		
	def init(self):
		global mm, state
		
		if state == NEEDINIT:
			init()
		else:
			state = RUN
			onGameStatusChanged(bf2.GameStatus.Playing)
		
		mm.info("Started DAM")
	
	def shutdown(self):
		global state
		
		if state == RUN:
			state = STOPPED

def mm_load( modManager ):
	global mm
		
	mm = modManager
	return DAMW()
