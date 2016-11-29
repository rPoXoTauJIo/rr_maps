# vim: ts=4 sw=4 noexpandtab
"""RR PROS module.

This is a RR PROS ModManager module

===== Config =====
 # RR PROS option
mm_rrpros.enable_squadless_kick 1 (0 - disable / 1 - enable squadless kick)
mm_rrpros.isPublicWarning 0 (0 - disable / 1 - enable warning public message to player)
mm_rrpros.kickInterval 120 (parameter in sec - 120 means 120 sec delay before player will be kicked)
mm_rrpros.kickDelay 5 (parameter in sec - 5 sec means a time between message about kick and kick action)
mm_rrpros.msgInterval 30 (parameter in sec - warning message interval for squadless rule)
mm_rrpros.warningMsg "Squadless players will be kicked!" (warning message)
mm_rrpros.prefixMsg "RR PROS:" (Prefix for messages)

===== History =====
 v0.1 - 10/05/2015:
 Started
 
Author: Sergey '6apcyk Kittenko' Medvedev
"""

import bf2
import host
import mm_utils
import bf2.Timer

__version__ = 0.1

__required_modules__ = {
	'modmanager': 1.6
}

__supports_reload__ = True

__supported_games__ = {
	'bf2': True
}

__description__ = "ModManager RR PROS v%s" % __version__

configDefaults = {
	'enable_squadless_kick': 1,
	'isPublicWarning': 0,
	'kickInterval': 120,
	'kickDelay': 5,
	'msgInterval': 30,
	'warningMsg': "Squadless players will be kicked!",
	'prefixMsg': "RR PROS:"
}

class RrPros( object ):
	
	def __init__( self, modManager ):
		self.mm = modManager
		self.__state = 0
		self.kickList = []
		self.msgTimer = None
				
	def init( self ):
		self.__config = self.mm.getModuleConfig( configDefaults )

		self.kickInterval = self.__config['kickInterval']
		self.msgInterval = self.__config['msgInterval']
		self.kickDelay = self.__config['kickDelay']
		self.prefixMsg = self.__config['prefixMsg']
		self.warningMsg = self.__config['warningMsg']
		self.enable_squadless_kick = self.__config['enable_squadless_kick']
		self.isPublicWarning = self.__config['isPublicWarning']
		
		if self.enable_squadless_kick == 1 and 0 == self.__state:
			host.registerHandler('PlayerSpawn', self.onPlayerSpawn)
			host.registerGameStatusHandler(self.onGameStatusChanged)

		self.__state = 1

	def cmdExec( self, ctx, cmd ):
		self.Debug("cmdExec")
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def onPlayerSpawn( self, player, soldier ):
		self.Debug("onPlayerSpawn")

		if 1 != self.__state:
			return 0

		if player.getSquadId() == 0 and not player.isCommander():
			self.Debug("not in squad or commander")
			if player.index not in self.kickList:
				self.Debug("add to kick list")
				self.kickList.append(player.index)

				self.Debug("kickInterval: %d" % self.kickInterval)
				bf2.Timer(self.onKickTimer, self.kickInterval, 1)
				
			self.doSendMessage("will be kicked for not being in a squad", player, 2)

	def shutdown( self ):
		self.Debug("shutdown")
		host.unregisterHandler(self.onPlayerSpawn)
		host.unregisterGameStatusHandler(self.onGameStatusChanged)

		self.__state = 2

	def update( self ):
		self.Debug("update")
		pass
	
	def doKick ( self, player ):
		self.Debug("doKick")
		host.rcon_invoke('admin.kickPlayer %d' % player.index)
		self.Info(player.getName() + " kicked")

	def doSendMessage ( self, msg, player = None, type = 1 ):
		self.Debug("doSendMessage")
		if self.isPublicWarning == 1:
			type = 1
			
		if player == None:
			host.rcon_invoke('game.sayall "%s %s"' % (self.prefixMsg, msg))
		else:		
			player_name = player.getName()
			self.Debug("Sending message: %s %s" % (player_name, msg))
			
			if type == 1:
				host.rcon_invoke('game.sayall "%s %s %s"' % (self.prefixMsg, player_name, msg))
			elif type == 2:
				mm_utils.PersonalMessage("%s %s %s" % (self.prefixMsg, player_name, msg), player)
	
	def onKickTimer(self, data):
		self.Debug("onKickTimer")
		
		player = bf2.playerManager.getPlayerByIndex(self.kickList.pop(0))
		
		if player.getSquadId() == 0 and not player.isCommander():
			self.Info(player.getName() + " kicking..")
			self.doSendMessage("was kicked for not being in a squad", player, 1)
			bf2.Timer(self.doKick, self.kickDelay, 1, player)
		
	def onGameStatusChanged(self, status):
		self.Debug("onGameStatusChanged")
		if status == bf2.GameStatus.Playing:
			self.Debug("Game Status: Playing")
			
			self.msgTimer = bf2.Timer(self.onMsgTimer, self.msgInterval, 1)
			self.msgTimer.setRecurring(self.msgInterval)

		elif status == bf2.GameStatus.PreGame:
			self.Debug("Game Status: PreGame")
			
			self.msgTimer.destroy()
			self.msgTimer = None
			
			self.kickList = []
		
		elif status == bf2.GameStatus.EndGame:
			self.Debug("Game Status: EndGame")

	def onMsgTimer(self, data):
		self.Debug("onMsgTimer")
		self.doSendMessage(self.warningMsg,)
		
	def Info(self, msg):
		self.mm.info(self.prefixMsg + " " + msg)

	def Debug(self, msg):
		self.mm.debug(1, self.prefixMsg + " " + msg)


def mm_load( modManager ):
	return RrPros( modManager )
