# -*- coding: iso-8859-15 -*-

import os
import sys
import default
import new
import string
import re
import time
import datetime
import host
import bf2
import bf2.Timer
import mm_utils
import math
import mm_banmanager as banmanager



__version__ = 1.0

# Set the required module versions here
__required_modules__ = {
	'modmanager': 1.7#,
	#"mm_utils": 3.5
}

# Does this module support reload ( are all its reference closed on shutdown?)
__supports_reload__ = True

# Sets which games this module supports
__supported_games__ = {
	'bf2': True,
	'bfheroes': True,
	'bfp4f': True
}

# Set the description of your module here
__description__ = "Admin Module v%s" % __version__


class Admin:
	def __init__(self, modManager):
		self.mm = modManager
		self.Info("Admin constructor")
		self.__state = 0
		### self.mapList (the active self.mapList on the server)
		self.mapList = []

		# If true, the script uses cd key hashes to verify administrators.  If false,
		# it skips those checks, so one is able to test the script on a local server
		self.isDedicated = True
		#vote
		self.voteRunning = False
		self.voteTimer = None
		self.voteMsgTimer = None
		self.voteList = {}
		self.voteMap = []
		self.voteResultMsg = ""
		self.voteTimeLeft = 120
		#Are any admins online or not?
		self.admins = False
		#self.lastBan
		self.lastBan = ""
		self.isSquadCreationAllowed = True
		self.squadMsgTimer = None
		self.squadTimer = None

		self.lastAutoVoteTime = 0
		self.lastAutoRunNextTime = 0
		self.roundStartTime = 0
		self.autoVoteResultMsg = ""

		self.aVoteMode = ""
		self.aVoteSize = "" 
		self.aVoteMap = ""

		self.timers = []

		self.logFile = None
		

	
	def init(self):
		"""Provides default initialisation."""
		self.Info("Admin init")
		self.InitConfig()
		if 0 == self.__state:
			host.registerHandler('ChatMessage', self.onChatMessage, 1)			
			host.registerHandler('ChatMessage', self.onChatMessageVote, 1)
			host.registerHandler('PlayerChangedSquad', self.onPlayerChangedSquad)
			host.registerHandler('ChangedCommander', self.onChangedCommander)
			
			host.registerHandler('ChatMessage', self.onChatLog, 1)
			host.registerHandler('PlayerConnect', self.onPlayerConnectLog, 1)
			host.registerHandler('PlayerKilled', self.onPlayerKilledLog)
			host.registerGameStatusHandler(self.onGameStatusChanged)
			if self.squadMsgTimer != None:
				self.squadMsgTimer.destroy()
				self.squadMsgTimer = None
			if self.squadTimer != None:
				self.squadTimer.destroy()
				self.squadTimer = None		
			if self.voteTimer != None:
				self.voteTimer.destroy()
				self.voteTimer = None
			if self.voteMsgTimer != None:
				self.voteMsgTimer.destroy()
				self.voteMsgTimer = None	
			for t in self.timers:
					if t != None:
						t.destroy()
			self.timers = []
		self.__state = 1
		# Check to see if the server is dedicated or not
		#if int(host.rcon_invoke("sv.internet").strip()) == 1:
		#	self.isDedicated = True
		#else:
		#	self.isDedicated = False
		self.Info("Admin in dedicated mode: %s" % (self.isDedicated))
		# Fill the dictionary with all the available commands
		self.adminCommands = {
			"init":			self.InitConfig,
			"admins":		self.TextAdmins,
			"b":			self.PlayerBan,
			"ban":			self.PlayerBan,
			"ab":			self.PlayerABan,
			"aban":			self.PlayerABan,
			"change":		self.MapChange,
			"fly":			self.PlayerFly,
			"hash":			self.PlayerHash,
			"help":			self.TextHelp,
			"k":			self.PlayerKick,
			"kick":			self.PlayerKick,
			"kill":			self.PlayerKill,
			"r":			self.PlayerReport,
			"reload":		self.MapReload,
			"remove":		self.MapRemove,
			"report":		self.PlayerReport,
			"resign":		self.PlayerResign,
			"restart":		self.MapRestart,
			"rules":		self.TextRules,
			"runnext":		self.MapRunNext,
			"save":			self.MapListSave,
			"say":			self.TextSay,
			"sayteam":		self.TextSayTeam,
			"setnext":		self.MapSetNext,
			"shownext":		self.MapShowNext,
			"maplist":		self.TextMapList,
			"ss":			self.PlayerScreenshot,
			"st":			self.TextSayTeam,
			"stopserver":	self.ServerStop,
			"swapteams":	self.PlayerSwapTeams,
			"s":			self.PlayerSwitch,
			"switch":		self.PlayerSwitch,
			"tb":			self.PlayerBanTemp,
			"ub":			self.PlayerUnban,
			"unban":		self.PlayerUnban,
			"banlist":		self.TextBanList,
			"pb":			self.ServerPBRestart,
			"pbrestart":    self.ServerPBRestart,
			"vote":			self.ServerVote,
			"w":			self.PlayerWarn,
			"warn":			self.PlayerWarn,
			"website":		self.TextWebsite,
			"mvote":		self.MapVote,
			"mapvote":		self.MapVote,
			"autovote":		self.AutoVote,
			"avote":		self.AutoVote,
			"anext":		self.AutoRunNext,
			"arunnext":		self.AutoRunNext,
		}
	
	
	# Reinitialize the settings file
	def InitConfig(self):
		try:
			import mm_admin_settings as settings
			reload(settings)
			self.config = settings			
		except:
			self.mm.error("Failed to load admin settings")

	#
	# ======================= ADMIN COMMANDS =======================
	#

	def onGameStatusChanged(self, status):
		try:
			if bf2.GameStatus.PreGame == status:
				self.Info("Status changed to PreGame")
				self.voteRunning = False
				if self.squadMsgTimer != None:
					self.squadMsgTimer.destroy()
					self.squadMsgTimer = None
				if self.squadTimer != None:
					self.squadTimer.destroy()
					self.squadTimer = None		
				if self.voteTimer != None:
					self.voteTimer.destroy()
					self.voteTimer = None
				if self.voteMsgTimer != None:
					self.voteMsgTimer.destroy()
					self.voteMsgTimer = None	
				self.isSquadCreationAllowed = False					
				self.Info("Players are denied to create squads and apply for commander position")	
				self.autoVoteResultMsg = ""
				for t in self.timers:
					if t != None:
						t.destroy()
				self.timers = []				
			if bf2.GameStatus.Playing == status:
				self.lastAutoVoteTime = 0
				self.lastAutoRunNextTime = 0
				self.roundStartTime = host.timer_getWallTime()
				self.Info("Status changed to Playing")
				timeBeforeStart = int(host.rcon_invoke('sv.startdelay').strip())
				self.Info("Time before start: %d" % timeBeforeStart)
				tDiff = 0
				if timeBeforeStart > self.config.adm_squadTimeAllowed:
					tDiff = timeBeforeStart - self.config.adm_squadTimeAllowed
					message = "§C1001No Squad or Commander before §C1001%s§C1001 or be kicked \ banned" % time.strftime('%M:%S', time.gmtime(self.config.adm_squadTimeAllowed))
					self.squadMsgTimer = bf2.Timer(self.onMsgTimer, 0, 1, message)
					self.squadMsgTimer.setRecurring(self.config.adm_squadRecurrence)
					self.squadTimer = bf2.Timer(self.onSquadTimer, tDiff, 1, None)	
				else:
					self.isSquadCreationAllowed = True	
				dtm = time.strftime("%d/%m/%Y_%H:%M:%S  UTC", time.gmtime(time.time()))
				self.logFile.write("Round Start  : " + dtm + "\n")
				self.logFile.write("Map          : " + bf2.gameLogic.getMapName() + "\n")
				self.logFile.write("Gamemode     : " + bf2.serverSettings.getGameMode() + "\n")
				self.logFile.write("Team 1       : " + bf2.gameLogic.getTeamName(1) + "\n")
				self.logFile.write("Team 2       : " + bf2.gameLogic.getTeamName(2) + "\n")							
			self.CreateFile()							
		except:		
			self.Info("Exception in onGameStatusChanged")
		
	def onMsgTimer(self, data):
		if host.timer_getWallTime() - self.roundStartTime > int(host.rcon_invoke('sv.startdelay').strip()) - self.config.adm_squadTimeAllowed:
			self.squadMsgTimer.destroy()
			self.squadMsgTimer = None
		self.SayAll(data, 3)

	def onSquadTimer(self, data):
		try:
			try:
				if self.squadMsgTimer != None:
					self.squadMsgTimer.destroy()
					self.squadMsgTimer = None
			except:
				if self.squadMsgTimer != None:
					self.squadMsgTimer.destroy()
					self.squadMsgTimer = None
			if self.squadTimer != None:
				self.squadTimer.destroy()
				self.squadTimer = None
			self.isSquadCreationAllowed = True
			message = "§C1001Now you can create squads and apply for commander position!"
			self.SayAll(message, 2)	
			self.Info("Now players able to create squads and apply for commander position")	
		except:
			self.Info("Exception in onSquadTimer")

	def onPlayerChangedSquad(self, player, oldSquad, newSquad):
		try:
			if self.isSquadCreationAllowed:
				return
			self.Info("Squad changed by player: %s" % player.getName())
			if player and player.isValid():
				self.KickPlayer("", player, " for squad/commander violation!", None)
		except:
			self.Info("Exception in onPlayerChangedSquad")

	def onChangedCommander(self, team, oldCmd, newCmd):
		try:
			if self.isSquadCreationAllowed:
				return
			if newCmd and newCmd.isValid():
				self.Info("New commander: %s" % newCmd.getName())
			else:
				self.Info("Commander resigned")
				return			
			self.KickPlayer("", newCmd, " for squad/commander violation!", None)
		except:
			self.Info("Exception in onChangedCommander")	

	# Show the next map
	def MapShowNext(self, cmd, args, p):
		try:
			fMapName = ""
			fMapType = ""
			fMapSize = ""

			self.ConstructMaplist()
			nextMapID = host.rcon_invoke("admin.nextLevel").strip()
			for nextMap in self.mapList:
				map = nextMap.split("|")
				if map[0] == nextMapID:
					fMapName = self.FormatMapProperties(map[1])
					fMapType = self.FormatMapProperties(map[2])
					fMapSize = self.FormatMapProperties(map[3])
					
					mm_utils.PersonalMessage("§C1001Next map in rotation is: §C1001" + fMapName + " (" + fMapType + ", " + fMapSize + ")", p)
					break
		except:
			self.Info("Exception in MapShowNext()")

	def TextMapList(self, cmd, args, p):
		try:
			fMapName = ""
			fMapType = ""
			fMapSize = ""
			self.ConstructMaplist()
			nextMapID = host.rcon_invoke("admin.nextLevel").strip()
			mapList = ""
			for nextMap in self.mapList:
				map = nextMap.split("|")
				
				fMapName = self.FormatMapProperties(map[1])
				fMapType = self.FormatMapProperties(map[2])
				fMapSize = self.FormatMapProperties(map[3])
				lm = " §1§C1001[%s]:§C1001%s(%s,%s)" % (map[0],fMapName,fMapType,fMapSize)
				if map[0] == nextMapID:
					lm = " §1§C1001[%s]:%s(%s,%s)§C1001" % (map[0],fMapName,fMapType,fMapSize)
				if not len(args) > 0 or (len(args) == 1 and map[2].lower().find(args[0].lower()) > -1) or (len(args) == 2 and map[2].lower().find(args[0].lower()) > -1 and map[3].lower().find(args[1].lower()) > -1):
					mapList += lm
			if len(mapList) > 0:
				msg = self.MsgSplitter(mapList, 150)
				data = {"msg": msg, "timer": None, "player":p}
				t = bf2.Timer(self.PersonalTimedMessage, 0, 1, data)
				data["timer"] = t
				t.setRecurring(10)
				self.timers.append(t)				
		except:
			self.Info("Exception in TextMapList()")
	
	def PersonalTimedMessage(self, data):
		try:
			d = []
			for i in range(4):				
				if(len(data["msg"]) > i):
					d.append(data["msg"][i])
			for m in d:
				mm_utils.PersonalMessage(m, data["player"])
				data["msg"].remove(m)						
			if len(data["msg"]) == 0:
				self.timers.remove(data["timer"])
				data["timer"].destroy()
				data["timer"] = None				
		except:
			self.Info("Exception in PersonalTimedMessage")
		

	# Change the next map and run it
	def MapChange(self, cmd, args, p):
		try:
			if not self.MapSetNext(cmd, args, p) == False:
				self.AdminPM("§C1001Changing map", p)
				self.SayAll("§C1001Running next map...")
				host.rcon_invoke('admin.runNextLevel')
				self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in MapChange()")


	# Save the current self.mapList
	def MapListSave(self, cmd, args, p):
		try:
			host.rcon_invoke("maplist.save")
			self.AdminPM("§C1001The current self.mapList has been saved", p)
			self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in MapListSave()")


	# Remove a map from the self.mapList
	def MapRemove(self, cmd, args, p):
		try:
			fMapName = ""
			fMapType = ""
			fMapSize = ""

			if len(args) < 1 or args[0].isdigit() == False:
				mm_utils.PersonalMessage("§C1001Please specify a mapid", p)
				return False

			# Setting a next map using a mapid
			self.ConstructMaplist()
			matches = 0
			for nextMap in self.mapList:
				map = nextMap.split("|")
				mapID = map[0]
				mapName = map[1]
				mapType = map[2]
				mapSize = map[3]

				# If the ID's match, we have a winner..
				if map[0] == args[0]:
					matches = 1

					# Remove the map
					host.rcon_invoke("maplist.remove %s" % str(mapID))

					# Format map properties
					fMapName = self.FormatMapProperties(mapName)
					fMapType = self.FormatMapProperties(mapType)
					fMapSize = self.FormatMapProperties(mapSize)

					# Display removal text
					self.AdminPM("§C1001The following map has been removed from the rotation: " + fMapName + " (" + fMapType + ", " + fMapSize + ")", p)
					self.Log(cmd, p.getName(), "", fMapName + " (" + fMapType + ", " + fMapSize + ")")
					break

			# If there aren't any matches, return (stop execution)
			if matches == 0:
				mm_utils.PersonalMessage("§C1001Sorry, no matching map found for mapID: " + args[0], p)
				return False
		except:
			self.Info("Exception in MapRemove()")


	# Set the next map
	def MapSetNext(self, cmd, args, p):
		try:
			fMapName = ""
			fMapType = ""
			fMapSize = ""

			if len(args) < 1:
				mm_utils.PersonalMessage("§C1001Please specify a mapname or mapid", p)
				return False

			# Setting a next map using a mapid
			elif args[0].isdigit() == True:
				self.ConstructMaplist()
				matches = 0
				for nextMap in self.mapList:
					map = nextMap.split("|")
					mapID = map[0]
					mapName = map[1]
					mapType = map[2]
					mapSize = map[3]

					# If the ID's match, we have a winner..
					if map[0] == args[0]:
						matches = 1
						host.rcon_invoke("admin.nextLevel %s" % str(mapID))

						# Format map properties
						fMapName = self.FormatMapProperties(map[1])
						fMapType = self.FormatMapProperties(map[2])
						fMapSize = self.FormatMapProperties(map[3])

						# Display text
						self.AdminPM("§C1001Next map in rotation set to: §C1001" + fMapName + " (" + fMapType + ", " + fMapSize + ")§C1001", p)
						self.Log(cmd, p.getName(), "", fMapName + " (" + fMapType + ", " + fMapSize + ")")
						break

				# If there aren't any matches, return (stop execution)
				if matches == 0:
					mm_utils.PersonalMessage("§C1001Sorry, no matching map found for mapID: §C1001" + args[0], p)
					return False

			# Setting a next map using the mapname, gamemode and mapsize (search through
			# server's self.mapList, if fail, then search through adm_mapListAll)
			else:
				if len(args) < 3:
					mm_utils.PersonalMessage("§C1001Please specify a mapname, gamemode and layer", p)
					return False

				if args[2] == "16" or args[2] == "32" or args[2] == "64":
					mm_utils.PersonalMessage("§C1001You can no longer use 16/32/64, use inf, alt or std instead", p)
					return False

				self.ConstructMaplist()
				matches = 0
				for nextMap in self.mapList:
					map = nextMap.split("|")
					# [0] = mapID
					# [1] = mapname
					# [2] = maptype
					# [3] = mapsize

					# Does the entered mapname, gamemode and layer exist in the server's
					# self.mapList§
					if map[1].lower().find(args[0].lower()) != -1 and map[2].lower().find(args[1].lower()) != -1 and map[3].lower().find(args[2].lower()) != -1:
						self.Info("Mapname, gamemode and layer found in maplist!")
						matches += 1
						mapID = map[0]
						mapName = map[1]
						mapType = map[2]
						mapSize = map[3]
						break

				# If no matches are found in the server's self.mapList, try to find it in
				# adm_mapListAll
				if matches == 0:
					for nextMap in self.config.adm_mapListAll:
						map = nextMap.split("|")
						# [0] = mapname
						# [1] = maptype
						# [2] = mapsize

						# Search for the map in adm_mapListAll (mapname, gamemode, mapsize)
						if map[0].lower().find(args[0].lower()) != -1 and map[1].lower().find(args[1].lower()) != -1 and map[2].lower().find(args[2].lower()) != -1:
							self.Info("Mapname, gamemode and layer found in adm_mapListAll!")
							matches += 1
							break

					self.Info("matches after second search: " + str(matches))

					# Map found, append it to the current list
					if matches == 1:
						# Save map info, so we can add the map to the server's self.mapList later
						mapID = len(self.mapList)
						mapName = map[0]
						mapType = map[1]
						mapSize = map[2]

						# Format map properties
						fMapName = self.FormatMapProperties(mapName)
						fMapType = self.FormatMapProperties(mapType)
						fMapSize = self.FormatMapProperties(mapSize)

						# Translate mapsizes, so we add the correct ones
						if mapSize == "inf":
							mapSize = "16"
						elif mapSize == "alt":
							mapSize = "32"
						elif mapSize == "std":
							mapSize = "64"

						self.Info("Trying RCON commands " + str(mapName) + ", " + str(mapType) + ", " + str(mapSize))

						# Add the map
						host.rcon_invoke("maplist.append %s %s %s" % (mapName, mapType, mapSize))

						self.Info("Trying RCON commands... say: " + str(fMapName) + ", " + str(fMapType) + ", " + str(fMapSize))

						# Display text
						self.AdminPM("§C1001The following map has been added to rotation: §C1001" + fMapName + " (" + fMapType + ", " + fMapSize + ")", p)

				self.Info("Done searching")

				# If there still aren't any matches, return (stop execution)
				if matches == 0:
					mm_utils.PersonalMessage("§C1001Sorry, no matching map found for: §C1001" + args[0] + " " + args[1] + " " + args[2], p)
					return False
				else:
					fMapName = self.FormatMapProperties(mapName)
					fMapType = self.FormatMapProperties(mapType)
					fMapSize = self.FormatMapProperties(mapSize)

					self.Info("Going to set the next map")
					host.rcon_invoke("admin.nextLevel %s" % str(mapID))

					self.AdminPM("§C1001Next map in rotation set to: §C1001" + fMapName + " (" + fMapType + ", " + fMapSize + ")§C1001", p)
					self.Log(cmd, p.getName(), "", fMapName + " (" + fMapType + ", " + fMapSize + ")")
		except:
			self.Info("Exception in MapSetNext()")
			return False


	# Run the next map
	def MapRunNext(self, cmd, args, p):
		try:
			self.AdminPM("§C1001Running next map", p)
			self.SayAll("§C1001Running next map...")
			host.rcon_invoke('admin.runNextLevel')
			self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in MapRunNext()")


	# Restart the current map
	def MapRestart(self, cmd, args, p):
		try:
			self.AdminPM("§C1001Restarting map", p)
			self.SayAll("§C1001Restarting map...")
			host.rcon_invoke('admin.restartMap')
			self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in MapRestart()")


	# Reload the current map (this reloads the entire map)
	def MapReload(self, cmd, args, p):
		try:
			currentMapID = host.rcon_invoke("admin.currentLevel").strip()
			host.rcon_invoke("admin.nextLevel %s" % str(currentMapID))
			self.AdminPM("§C1001Reloading map", p)
			self.SayAll("§C1001Reloading map...")
			host.rcon_invoke('admin.runNextLevel')
			self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in MapReload()")


	def TextAdmins(self, cmd, args, p):
		try:
			mm_utils.PersonalMessage("§C1001The following admins are online:", p)

			adm = ""
			i = 0
			j = 0
			for	pl in bf2.playerManager.getPlayers():
				# check if Real admins are there or not
				if self.isAdmin(pl):
					i += 1
					j += 1
					
					if adm != "":
						adm += ", "
					adm += pl.getName()

					if i == 5:
						mm_utils.PersonalMessage(adm, p)
						i = 0
						adm = ""
			if i > 0:
				mm_utils.PersonalMessage(adm, p)

			if j == 0:
				mm_utils.PersonalMessage("none", p)
		except:
				self.Info("Exception in	TextAdmins()")


	# Display text (global)
	def TextSay(self, cmd, args, p):
		try:
			if len(args) < 1:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a message", p)
			else:
				i = 0
				message = ""
				while i < len(args):
					message += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				message = self.FindReason(message)

				self.SayAll(message, 2)
				self.Log(cmd, p.getName(), "", message)
		except:
			self.Info("Exception in TextSay()")


	# Display text
	def TextSayTeam(self, cmd, args, p):
		try:
			if len(args) < 2 or (args[0].lower() != "us" and args[0].lower() != "them"):
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a team [us/them] and a message", p)
			else:
				# Set the team
				if args[0].lower() == "us":
					team = p.getTeam()
				elif args[0].lower() == "them":
					if p.getTeam() == 1:
						team = 2
					else:
						team = 1

				# Form the text to display
				i = 1
				message = ""
				while i < len(args):
					message += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				message = self.FindReason(message)
			
				host.rcon_invoke('game.sayTeam %s "§3Team: %s"' % (team, message))
				self.Log(cmd, p.getName(), "team " + str(team), message)
		except:
			self.Info("Exception in TextSayTeam()")


	# Display helpmessages
	def TextHelp(self, cmd, args, p):
		try:
			mm_utils.PersonalMessage("§C1001Available commands:", p)
			i = 0
			keys = ""
			level = self.AdminLevel(p)
			for key in self.adminCommands:
				if not level > self.config.adm_adminPowerLevels[key]:
					i += 1
					if keys != "":
						keys += ", "
					if len(keys + self.config.adm_commandSymbol + key) < 243:
						keys += self.config.adm_commandSymbol + key
					else:
						mm_utils.PersonalMessage("§C1001" + keys, p)
						keys = self.config.adm_commandSymbol + key
			if len(keys) > 0:
				mm_utils.PersonalMessage("§C1001" + keys, p)	

			self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in TextHelp()")

	# Display the Rules of the Server
	def TextRules(self, cmd, args, p):
		try:
			if self.config.adm_rulesEnabled == True:
				for r in self.config.adm_rules:
					mm_utils.PersonalMessage(r, p)
		except:
			self.Info("Exception in TextRules()")


	# Display the "Mumble-message" as defined in the settings
	def TextMumble(self, cmd, args, p):
		try:
			mm_utils.PersonalMessage(self.config.adm_mumble, p)
		except:
			self.Info("Exception in TextMumble()")


	# Resign a player
	def PlayerResign(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else:
				i = 1
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					i = 1
					reason = ""
					while i < len(args):
						reason += str(args[i] + " ")
						i += 1

					# Find a predefined reason
					reason = self.FindReason(reason)

					# Resign the player
					self.AdminPM("§C1001" + foundPlayer.getName() + " has been resigned, " + reason, p)
					self.SayAll("§C1001RESIGNING PLAYER %s, %s" % (foundPlayer.getName(), reason))
					#bf2.gameLogic.sendGameEvent(foundPlayer, 13, 1) # Blurs the screen of the
					#resigned player for a second
					foundPlayer.setSuicide(1)
					if foundPlayer.getTeam() == 1:
						foundPlayer.setTeam(2)
						foundPlayer.setTeam(1)
					else:
						foundPlayer.setTeam(1)
						foundPlayer.setTeam(2)
					self.Log(cmd, p.getName(), foundPlayer.getName(), reason)
		except:
			self.Info("Exception in PlayerResign()")


	# Kill a player
	def PlayerKill(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else:
				i = 1
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)

				# Kill player
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					try:
						# Try to kill the player
						foundPlayer.getVehicle().setDamage(0.000000001)
						foundPlayer.setTimeToSpawn(0)
						self.AdminPM("§C1001" + foundPlayer.getName() + " has been killed, " + reason, p)
						self.SayAll("§C1001KILLING PLAYER %s, %s" % (foundPlayer.getName(), reason))
					except:
						# Couldn't kill the player (was probably in gunner-seat or so), mark him for death! (will die when he exits the vehicle)
						self.AdminPM("§C1001" + foundPlayer.getName() + " could not be killed now", p)
					self.Log(cmd, p.getName(), foundPlayer.getName(), reason)
		except Exception, e:			
			self.Info("Exception in PlayerKill")
			self.Info(e.message)


	# Take a punkbuster screenshot of a player
	def PlayerScreenshot(self, cmd, args, p):
		try:
			if len(args) < 1:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name", p)
			else:
				foundPlayer = mm_utils.FindPlayer(args[0])
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					# Set the height and width
					host.rcon_invoke('PB_SV_SsWidth %s' % self.config.adm_pbSsWidth)
					host.rcon_invoke('PB_SV_SsHeight %s' % self.config.adm_pbSsHeight)

					# Take the screenshot
					host.rcon_invoke('pb_sv_getss "%s"' % foundPlayer.getName())
					self.AdminPM("§C1001Screenshot taken of " + foundPlayer.getName(), p)
				self.Log(cmd, p.getName(), foundPlayer.getName(), "")
		except:
			self.Info("Exception in PlayerScreenshot()")


	# Kick a player
	def PlayerKick(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else:
				i = 1
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)

				# Kick player
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					self.KickPlayer(cmd, foundPlayer, reason, p)
		except Exception, e:
			self.Info("Exception in PlayerKick()")						
			self.Info(e.message)

	def KickPlayer(self, cmd, player, reason, p):
		try:
			self.AdminPM("§C1001" + player.getName() + " has been kicked, " + reason + "§C1001", p)
			self.SayAll("§C1001KICKING PLAYER §C1001%s§C1001, %s" % (player.getName(), reason))
			if self.config.usePunkbuster == True:
				host.rcon_invoke('pb_sv_kick "%s" %i "%s"' % (player.getName(), self.config.adm_kickTime, reason))
			else:
				host.rcon_invoke('admin.kickPlayer %d' % player.index)
		
			pName = "autoadmin"
			if p != None and p.isValid:
				pName = p.getName()
			self.Log(cmd, pName, player.getName(), reason)
		except:
			self.Info("Exception in KickPlayer")

	# Warn a player
	def PlayerWarn(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else:
				i = 1
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)

				# Warn player
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					self.AdminPM("§C1001" + foundPlayer.getName() + " has been warned, " + reason, p)
					self.SayAll("§C1001WARNING PLAYER %s, %s" % (foundPlayer.getName(), reason))	# Dispay warningmessage
					# AWARD_NAME_1220104_1 STOP DOING THAT
					host.sgl_sendMedalEvent(foundPlayer.index, 1220104, 1)
					self.Log(cmd, p.getName(), foundPlayer.getName(), reason)
		except Exception, e:
			self.Info("Exception in PlayerWarn()")
			self.Info(e.message)


	# Ban a player
	def PlayerBan(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else: 
				if len(args) == 2 and args[1].isdigit():
					mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
				else:
					i = 1
					reason = ""
					while i < len(args):
						if args[i].isdigit() == False:
							reason += str(args[i] + " ")
						i += 1
					
					# Find a predefined reason
					reason = self.FindReason(reason)
					banPeriod = None
					if args[1].isdigit():
						banPeriod = ":" + str(time.mktime(time.gmtime()) + int(args[1]) * 3600 * 24)
					# Ban player
					foundPlayer = mm_utils.FindPlayer(args[0])
					if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
						mm_utils.PersonalMessage("§C1001Not enough rights", p)
						return
					if foundPlayer == "none":
						mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
					elif foundPlayer == "more":
						mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
					else:
						self.AdminPM("§C1001" + foundPlayer.getName() + " has been banned, " + reason, p)
						self.SayAll("§C1001BANNING PLAYER %s, %s" % (foundPlayer.getName(), reason))	# Display banmessage
						self.mm.banManager().banPlayerNow(foundPlayer, reason, banPeriod, None, None, p.getName())
						self.Log(cmd, p.getName(), foundPlayer.getName(), reason)
		except:
			self.Info("Exception in PlayerBan()")

	# Ban a player by address
	def PlayerABan(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else:
				i = 1
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)
				
				# Ban player
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					self.AdminPM("§C1001" + foundPlayer.getName() + " has been banned, " + reason, p)
					self.SayAll("§C1001BANNING PLAYER %s, %s" % (foundPlayer.getName(), reason))	# Display banmessage
					self.mm.banManager().banPlayerNow(foundPlayer, reason, None, None, 'Address', p.getName())
					self.Log(cmd, p.getName(), foundPlayer.getName(), reason)
		except:
			self.Info("Exception in PlayerABan()")


	# Temp ban a player
	def PlayerBanTemp(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and a reason", p)
			else:
				i = 1
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)
				# Tempban the player
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					self.AdminPM("§C1001" + foundPlayer.getName() + " has been tempbanned, " + reason, p)
					self.SayAll("§C1001TEMP BANNING PLAYER %s, %s" % (foundPlayer.getName(), reason))	# Display banmessage
					self.mm.banManager().banPlayerNow(foundPlayer, reason, "Round", None, None, p.getName())
					self.Log(cmd, p.getName(), foundPlayer.getName(), reason)
		except:
			self.Info("Exception in PlayerBanTemp()")

	
	def TextBanList(self, cmd, args, p):
		try:
			nick = ""
			if len(args) > 0:
				#mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				nick = args[0]
			banList = self.mm.banManager().getBanList()
			for key in banList:
				ban = banList[key]
				if nick == "" or ban["nick"].lower().find(nick.lower()) > 0:
					expire = ban["period"]
					if ban["period"].find(":") == 0:
						expire = self.TimeString(int(float(ban["period"].split(":")[1])))					
					banstr = "'%s'  '%s'	§C1001'%s'§C1001	'%s'	§C1001'%s'" % (self.TimeString(ban["datetime"]), expire, ban["nick"], ban["reason"],ban["by"])
					mm_utils.PersonalMessage(banstr, p)
					#ban["datetime"], ban["nick"], ban["method"], ban["period"],
					#ban["address"], ban["cdkeyhash"], ban["profileid"], ban["by"],
					#ban["reason"]
		except:
			self.Info("Exception in TextBanList()")
		
	def TimeString(self, when):
		""" Returns a string representing the current GMT time."""
		if when is None:
			when = time.time()
		return time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(when))

	#Unban a player
	def PlayerUnban(self, cmd, args, p):
		try:
			if len(args) > 0:
				banList = self.mm.banManager().getBanList()
				all = False
				if len(args) == 2:
					if args[1].lower() == "all":
						all = True
				nick = args[0].lower()
				uban = []
				for key in banList:
					ban = banList[key]					
					if ban["nick"].lower().find(nick) > -1:
						if len(uban) != 0 and not all:
							mm_utils.PersonalMessage("§C1001More then one ban with name specified found. If you want to unban all specify second parameter as 'all'", p)
							return
						uban.append(ban)
				result = True
				if not len(uban) > 0:
					mm_utils.PersonalMessage("§C1001Ban with name specified was not found.", p)
					return
				key = "cdkeyhash"
				for ban in uban:
					if ban["method"] == mm_utils.BanMethod.key:
						key = "cdkeyhash"
					elif ban["method"] == mm_utils.BanMethod.address:
						key = "address"
					result = result and self.mm.banManager().unbanPlayer(ban[key])	
					if result:
						self.AdminPM("§C1001Player '%s' has been unbanned" % ban["nick"], p)
						self.Log(cmd, p.getName(), ban["nick"], "")
					else:
						mm_utils.PersonalMessage("§C1001Player '%s' unban failed" % ban["nick"], p)	
			else:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name", p)
		except:
			self.Info("Exception in PlayerUnban()")


	# Retrieve the hash of a player
	def PlayerHash(self, cmd, args, p):
		try:
			if len(args) < 1:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name", p)
			else:
				# Find the hash
				foundPlayer = mm_utils.FindPlayer(args[0])
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					h = mm_utils.get_cd_key_hash(foundPlayer)
					mm_utils.PersonalMessage("§C1001The hash of " + foundPlayer.getName() + " is: " + h, p)
				self.Log(cmd, p.getName(), foundPlayer.getName(), "")
		except:
			self.Info("Exception in PlayerHash()")


	# Fling a player
	def PlayerFly(self, cmd, args, p):
		try:
			if len(args) < 2:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and altitude (max: " + str(self.config.adm_maxAltitude) + ")", p)
			elif args[1].isdigit() == False or int(args[1]) > self.config.adm_maxAltitude:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and altitude (max: " + str(self.config.adm_maxAltitude) + ")", p)
			else:
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					if foundPlayer.isAlive() == 0 or foundPlayer.isManDown() == 1:
						mm_utils.PersonalMessage("§C1001" + foundPlayer.getName() + " is currently dead or down", p)
					else:
						if int(args[1]) > self.config.adm_maxAltitude:
							mm_utils.PersonalMessage("§C1001Altitude is too high. The max altitude is: " + self.config.adm_maxAltitude, p)
						else:
							pos = foundPlayer.getVehicle().getPosition()

							# Let the player fly
							pos1_n = pos[1] + abs(int(args[1]))
							foundPlayer.getVehicle().setPosition(tuple([float(pos[0]), float(pos1_n), float(pos[2])]))

							self.SayAll("§C1001FLINGING PLAYER %s" % foundPlayer.getName())
							self.Log(cmd, p.getName(), foundPlayer.getName(), args[1])
		except:
			self.Info("Exception in PlayerFly()")


	# Report a player
	def PlayerReport(self, cmd, args, p):
		try:
			if len(args) < 1:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name and/or reason", p)
			else:
				foundPlayer = mm_utils.FindPlayer(args[0])
				if self.AdminLevel(p) > self.AdminLevel(foundPlayer):
					mm_utils.PersonalMessage("§C1001Not enough rights", p)
					return
				if foundPlayer == "none" or foundPlayer == "more":
					i = 0
				else:
					i = 1

				# Reason
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)

				if foundPlayer == "none" or foundPlayer == "more":
					self.AdminPM("§C1001§2" + reason, p)
					self.Log(cmd, p.getName(), "", reason)
				else:
					self.AdminPM("§C1001§2" + foundPlayer.getName() + " is reported, " + reason, p)
					self.Log(cmd, p.getName(), foundPlayer.getName(), reason)

				# Report player
				mm_utils.PersonalMessage("§C1001Your report has been sent to all in-game admins", p)
		except:
			self.Info("Exception in PlayerReport()")


	# Teamswitch a player
	def PlayerSwitch(self, cmd, args, p):
		try:
			if len(args) < 1 or (len(args) > 1 and args[1].lower() != "now"):
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a name (and optional, [now])", p)
			else:
				foundPlayer = mm_utils.FindPlayer(args[0])
				if foundPlayer == "none":
					mm_utils.PersonalMessage("§C1001Sorry, no matching player found for '" + args[0] + "'", p)
				elif foundPlayer == "more":
					mm_utils.PersonalMessage("§C1001Multiple players found that match '" + args[0] + "'", p)
				else:
					# If the player is in a vehicle, don't switch, unless "now" is specified
					if len(args) == 1 and foundPlayer.getDefaultVehicle() != foundPlayer.getVehicle() and foundPlayer.getVehicle().templateName != "MultiPlayerFreeCamera":
						mm_utils.PersonalMessage("§C1001Player %s is in a vehicle (%s), so he can not be teamswitched" % (foundPlayer.getName(), foundPlayer.getVehicle().templateName), p)
						self.Log(cmd, p.getName(), foundPlayer.getName(), "Switch failed: Is in vehicle")
					elif len(args) == 1 and foundPlayer.isAlive() == 1:
						mm_utils.PersonalMessage("§C1001Player %s is not dead, so he can not be teamswitched" % foundPlayer.getName(), p)
						self.Log(cmd, p.getName(), foundPlayer.getName(), "Switch failed: Is alive")
					else:
						# Try to kill the player, he needs to be switched right away
						try:
							if foundPlayer.getVehicle().templateName == "MultiPlayerFreeCamera":
								foundPlayer.setSuicide(1)
								if foundPlayer.getTeam() == 1:
									foundPlayer.setTeam(2)
								else:
									foundPlayer.setTeam(1)
								self.AdminPM("§C1001" + foundPlayer.getName() + " got switched", p)								
							else:
								if foundPlayer.getDefaultVehicle() != foundPlayer.getVehicle():
									mm_utils.PersonalMessage("§C1001Player %s is in a vehicle (%s), so he can not be teamswitched" % (foundPlayer.getName(), foundPlayer.getVehicle().templateName), p)
								else:
									foundPlayer.getVehicle().setDamage(0.000000001)
									foundPlayer.setTimeToSpawn(0)
									foundPlayer.setSuicide(1)
									if foundPlayer.getTeam() == 1:
										foundPlayer.setTeam(2)
									else:
										foundPlayer.setTeam(1)
									self.AdminPM("§C1001" + foundPlayer.getName() + " got switched", p)
						except:
							mm_utils.PersonalMessage("§C1001Player %s is in a vehicle (%s), so he can not be teamswitched" % (foundPlayer.getName(), foundPlayer.getVehicle().templateName), p)
						self.Log(cmd, p.getName(), foundPlayer.getName(), "Instantly")
		except:
			self.Info("Exception in PlayerSwitch()")


	# Teamswap everyone
	def PlayerSwapTeams(self, cmd, args, p):
		try:
			self.Info("Teamswapping everone")
			self.AdminPM("§C1001Teamwapping everyone", p)
			self.SayAll("§C1001Teamswapping everyone...")
			for pl in bf2.playerManager.getPlayers():
				if pl.getTeam() == 1:
					pl.setTeam(2)
				else:
					pl.setTeam(1)
			self.Log(cmd, p.getName(), "", "")
		except:
			self.Info("Exception in PlayerTeamSwap()")


	# Stop the gameserver
	def ServerStop(self, cmd, args, p):
		try:
			if len(args) > 0:
				i = 0
				reason = ""
				while i < len(args):
					reason += str(args[i] + " ")
					i += 1

				# Find a predefined reason
				reason = self.FindReason(reason)

				# Stop the server
				self.Log(cmd, p.getName(), "", reason)
				self.AdminPM("§C1001Server has been terminated", p)
				self.SayAll("§C1001SERVER IS TERMINATED, PLEASE RECONNECT", 2)
				host.rcon_invoke("quit")
			else:
				mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a reason", p)
		except:
			self.Info("Exception in ServerStop")


	def ServerPBRestart(self, cmd, args, p):
		try:
			if self.config.usePunkbuster == False:
				mm_utils.PersonalMessage("§C1001Sorry, PBRestart only works when Punkbuster is enabled", p)
			else:
				if len(args) > 0:
					i = 0
					reason = ""
					while i < len(args):
						reason += str(args[i] + " ")
						i += 1

					# Find a predefined reason
					reason = self.FindReason(reason)

					# Stop the server
					self.Log(cmd, p.getName(), "", reason)
					host.rcon_invoke("pb_sv_restart 1")
					self.AdminPM("§C1001Punkbuster has been restarted", p)
				else:
					mm_utils.PersonalMessage("§C1001Incorrect usage of '" + cmd + "'. Please specify a reason", p)
		except:
			self.Info("Exception in ServerPBRestart")


	# Turn voting on/off
	def ServerVote(self, cmd, args, p):
		try:
			if len(args) > 0 and (args[0].lower() != "on" and args[0].lower() != "off"):
				mm_utils.PersonalMessage("§C1001Please specify a (correct) parameter (on/off)", p)
			else:
				if len(args) == 0:
					v = str(host.rcon_invoke('sv.votingEnabled').strip())
					if v == "1":
						v = "enabled"
					else:
						v = "disabled"
					mm_utils.PersonalMessage("§C1001Voting is " + v, p)
				else:
					if args[0].lower() == "on":
						host.rcon_invoke('sv.votingEnabled 1')
						self.AdminPM("§C1001Voting has been enabled", p)
					else:
						host.rcon_invoke('sv.votingEnabled 0')
						self.AdminPM("§C1001Voting has been disabled", p)
				self.Log(cmd, p.getName(), "", args[0].lower())
		except:
			self.Info("Exception in ServerVote()")

	# Display if Battlerecorder is enabled or disabled
	def TextBR(self, cmd, args, p):
		try:
			v = str(host.rcon_invoke('sv.autoRecord').strip())
			if v == "1":
				u = str(host.rcon_invoke('sv.demoQuality').strip())
				mm_utils.PersonalMessage("§C1001Battlerecorder is enabled with a quality of " + u, p)
			else:
				mm_utils.PersonalMessage("§C1001Battlerecorder is disabled", p)
		
		except:
			self.Info("Exception in TextBR()")	


	# Display the "Website-message" as defined in the settings
	def TextWebsite(self, cmd, args, p):
		try:
			mm_utils.PersonalMessage(self.config.adm_website, p)
		except:
			self.Info("Exception in TextWebsite()")


	def onVote(self, data):	
		try:
			if data[0] == 1:
				self.voteRunning = True
			else:
				self.voteRunning = False

			if self.voteTimer != None:
				self.voteTimer.destroy()
				self.voteTimer = None
				self.voteMsgTimer.destroy()
				self.voteMsgTimer = None
				vote_result = self.voteList.values()
				message = ""
				if len(self.voteMap) == 2:
					message = "§C1001Vote finished: §C1001" + str(self.voteMap[0]) + "§C1001: §C1001" + str(vote_result.count(1)) + "§C1001 | §C1001" + str(self.voteMap[1]) + "§C1001: §C1001" + str(vote_result.count(2)) + "§C1001"
				if len(self.voteMap) == 3:
					message = "§C1001Vote finished: §C1001" + str(self.voteMap[0]) + "§C1001: §C1001" + str(vote_result.count(1)) + "§C1001 | §C1001" + str(self.voteMap[1]) + "§C1001: §C1001" + str(vote_result.count(2)) + "§C1001 | §C1001" + str(self.voteMap[2]) + "§C1001: §C1001" + str(vote_result.count(3)) + "§C1001"
				self.SayAll(message, 3)
				self.AdminPM(message, data[1])
				self.voteResultMsg = message
				if data[1].isValid():
					self.voteResultMsg += " , initialized by §C1001" + data[1].getName()
		except:
			self.Info("Exception in onVote()")


	# Sends out the vote option messages (used by a self.voteMsgTimer))
	def onVoteMsgTimer(self, data):
		try:
			message = data
			msgs = self.MsgSplitter(message, 130)
			if len(msgs) < 4:
				self.SayAll(message, 2)
				self.SayAll("§C1001Type §C10011 - %d§C1001 in chat!" % len(self.voteMap), 2)
			else:
				arr = {"msg": msgs, "timer": None}
				timer = bf2.Timer(self.onMultilineMessageTimer, 0, 1, arr)
				arr["timer"] = timer
				self.timers.append(timer)
				timer.setRecurring(10)
			#timerMessage = "§C1001Mapvote is running...  §C1001%d§C1001 seconds left!
			#Vote Now!" % self.voteTimeLeft
			#self.SayAll(timerMessage)
			self.voteTimeLeft -= self.config.adm_mvoteRecurrence
		except:
			self.Info("Exception in onVoteMsgTimer()")

	def onMultilineMessageTimer(self, data):
		try:
			d = []
			for i in range(4):				
				if(len(data["msg"]) > i):
					d.append(data["msg"][i])
			for m in d:
				self.SayAll(m, 2)
				data["msg"].remove(m)			
			self.SayAll("§C1001Type §C10011 - %d§C1001 in chat!" % len(self.voteMap), 2)
			if len(data["msg"]) == 0:
				self.timers.remove(data["timer"])
				data["timer"].destroy()
				data["timer"] = None				
		except:
			self.Info("Exception in onMultilineMessageTimer")
			
	def SayAll(self, message, size=1):
		messages = self.MsgSplitter(message)
		for m in messages:
			host.rcon_invoke('game.sayall "§%d%s"' % (size, m))

	def MsgSplitter(self, message, maxlen=243):
		messages = []
		while len(message) > maxlen:	
			rf = message.rfind(":", 1, maxlen - 1) 
			if not rf > 0:
				rf = maxlen - 1
			rf = message.rfind(" ", 1, rf)
			if not rf > 0:
				rf = maxlen - 1
			sm = message[:rf + 1]
			message = message[rf + 1:]
			messages.append(sm)
		if len(message) > 0:
			messages.append(message)
		return messages

	def MapVote(self, cmd, args, p):
		try:
			# in case there is already running a vote
			if self.voteRunning == False:
				count = 0
				temp_str = ""
				temp_args = []
				for k in args:
					count+= k.count("'")
				if count % 2 == 0:
					delimiters = 0
					for k in args:
						if k.count("'") == 1:
							delimiters += 1
							if k.startswith("'"):
								temp_str+= k[1:] + " "
							elif k.endswith("'"):
								temp_str+= k[:-1] + " "
								temp_args.append(temp_str.strip())
								temp_str = ""
						elif delimiters % 2 != 0:
							temp_str+= k + " "
						else:
							temp_args.append(k)
					args = temp_args

				if len(args) == 0:
					if self.voteResultMsg != "":
						mm_utils.PersonalMessage("Last vote: " + self.voteResultMsg, p)
					else:
						mm_utils.PersonalMessage("§C1001There has been no vote yet in this round! Please name 2 or 3 maps for voting!", p)
				elif len(args) > 3 or len(args) < 2:
					mm_utils.PersonalMessage("§C1001Please name 2 or 3 maps for voting!", p)
				else:
					self.voteList.clear()
					message = ""					
					margs = args
					self.ConstructMaplist()
			
					for nextMap in self.mapList:
						map = nextMap.split("|")
						
						fMapName = self.FormatMapProperties(map[1])
						if map[1].lower().find(args[0].lower()) != -1:
							margs[0] = fMapName
						if map[1].lower().find(args[1].lower()) != -1:
							margs[1] = fMapName
						if len(args) == 3 and map[1].lower().find(args[2].lower()) != -1:
							margs[2] = fMapName
					self.voteMap = margs
					if len(args) == 2:
						message = "§C1001Vote:§C1001 1: §C1001" + margs[0] + "§C1001     2: §C1001" + margs[1] #+ "§C1001 | Type '§C10011§C1001' or '§C10012§C1001' in chat!"
					if len(args) == 3:
						message = "§C1001Vote:§C1001 1: §C1001" + margs[0] + "§C1001 2: §C1001" + margs[1] + "§C1001 3: §C1001" + margs[2] #+ "§C1001 | Type '§C10011§C1001','§C10012§C1001' or '§C10013§C1001' in chat!"

					self.voteTimeLeft = self.config.adm_mvoteDuration
					self.voteMsgTimer = bf2.Timer(self.onVoteMsgTimer, 0, 1, message)
					self.voteMsgTimer.setRecurring(self.config.adm_mvoteRecurrence)
					self.Log(cmd, p.getName(), "", message)
					self.onVote([1,p])
					self.voteTimer = bf2.Timer(self.onVote, self.config.adm_mvoteDuration, 1, [0, p])	
					self.AdminPM("§C1001Vote has been initialized...§C1001", p)
			# if there is a vote in this moment, check if it should be canceled
			else:
				if len(args) == 1 and args[0] == "cancel":
					self.onVote([0,p])
					self.SayAll("§C1001Vote has been terminated")
				else:
					mm_utils.PersonalMessage("§C1001Vote is already running, type \"!mvote cancel\" to stop it!", p)				
		except:
			self.Info("Exception in MapVote()")

	def AutoRunNext(self, cmd, args, p):		
		try:# in case there is already running a vote
			self.Log(cmd, p.getName(), "", "")
			if self.voteRunning == False:
				currWallTime = host.timer_getWallTime()
				self.Info("RStart: %d TDelta: %d Curr: %d Last: %d " % (self.roundStartTime, (currWallTime - self.lastAutoRunNextTime), currWallTime, self.lastAutoRunNextTime))
				if self.isAdmin(p) and len(args) == 1 and args[0] == "reset":					
					self.Info("!anext reset")
				else:
					canrun = True
					if (self.roundStartTime + self.config.adm_autoVoteDelay * 60) > currWallTime:
						canrun = False
					if self.lastAutoRunNextTime > 0 and ((currWallTime - self.lastAutoRunNextTime) < (self.config.adm_autoVoteTimer * 60)):
						canrun = False
					if not canrun:
						mm_utils.PersonalMessage("§C1001You cann't run vote more than once in %d minutes or within %d minutes from the start!" % (self.config.adm_autoVoteTimer, self.config.adm_autoVoteDelay), p)						
						return
				self.lastAutoRunNextTime = currWallTime
				self.voteList.clear()
				message = ""
				self.voteRunning = True	
				self.voteMap = ["Play this", "Run next"]
				message = "§C1001Auto mapvote Run Next or Play This:§C1001"
				i = 1
				for val in self.voteMap:
					message += " %d:§C1001%s§C1001" % (i, val)
					i += 1					
				i -= 1	   
				#message += " | Type §C10011 - %d§C1001 in chat!" % i
				self.voteTimeLeft = self.config.adm_mvoteDuration
				self.voteMsgTimer = bf2.Timer(self.onVoteMsgTimer, 0, 1, message)
				self.voteMsgTimer.setRecurring(self.config.adm_mvoteRecurrence)
				self.voteTimer = bf2.Timer(self.onAutoRunNext, self.config.adm_mvoteDuration, 1, 1)	
				self.AdminPM("§C1001AutoRunNext has been initialized...", p)
			# if there is a vote in this moment, check if it should be canceled
			else:
				if self.isAdmin(p):
					if len(args) == 1 and args[0] == "cancel":
						if self.voteTimer != None:
							self.voteTimer.destroy()
							self.voteTimer = None
						if self.voteMsgTimer != None:
							self.voteMsgTimer.destroy()
							self.voteMsgTimer = None
						self.voteRunning = False
						self.SayAll("§C1001Auto vote has been terminated")
					else:
						mm_utils.PersonalMessage("§C1001Auto vote is already running, type \"!avote cancel\" to stop it!", p)				
				else:
					mm_utils.PersonalMessage("§C1001Vote is already running!", p)
		except:
			self.Info("Exception in AutoRunNext()")


	def AutoVote(self, cmd, args, p):
		try:
			self.Log(cmd, p.getName(), "", "")
			# in case there is already running a vote
			if self.voteRunning == False:
				currWallTime = host.timer_getWallTime()
				self.Info("RStart: %d TDelta: %d Curr: %d Last: %d " % (self.roundStartTime, (currWallTime - self.lastAutoVoteTime), currWallTime, self.lastAutoVoteTime))	
				if self.isAdmin(p) and len(args) == 1 and args[0] == "reset":					
					self.Info("!avote reset")
				else:
					canrun = True
					if (self.roundStartTime + self.config.adm_autoVoteDelay * 60) > currWallTime:
						canrun = False
					if(currWallTime - self.lastAutoVoteTime) < (self.config.adm_autoVoteTimer * 60) and self.lastAutoVoteTime > 0:
						canrun = False
					if not canrun:
						mm_utils.PersonalMessage("§C1001You cann't run vote more than once in %d minutes or within %d minutes from the start!" % (self.config.adm_autoVoteTimer, self.config.adm_autoVoteDelay), p)						
						self.Info("!avote timed interval check doesn't pass")
						return
				self.lastAutoVoteTime = currWallTime
				self.voteList.clear()
				message = ""
				self.voteRunning = True	
				self.ConstructMaplist()
				maptypes = {}
					
				for nextMap in self.mapList:
					map = nextMap.split("|")
					if not maptypes.has_key(map[2]):											
						fMapType = self.FormatMapProperties(map[2])
						maptypes[map[2]] = fMapType					
				self.voteMap = maptypes
				message = "§C1001Auto mapvote Mode:§C1001"
				i = 1
				for key, val in maptypes.iteritems():
					message += " §C1001%d:§C1001%s" % (i, val)
					i += 1					
				i -= 1	   
				#message += "§C1001 | Type §C10011 - %d§C1001 in chat!" % i
				self.voteTimeLeft = self.config.adm_mvoteDuration
				self.voteMsgTimer = bf2.Timer(self.onVoteMsgTimer, 0, 1, message)
				self.voteMsgTimer.setRecurring(self.config.adm_mvoteRecurrence)
				self.voteTimer = bf2.Timer(self.onAutoVote, self.config.adm_mvoteDuration, 1, 1)	
				self.AdminPM("§C1001Autovote has been initialized...", p)
			# if there is a vote in this moment, check if it should be canceled
			else:
				if self.isAdmin(p):
					if len(args) == 1 and args[0] == "cancel":
						if self.voteTimer != None:
							self.voteTimer.destroy()
							self.voteTimer = None
						if self.voteMsgTimer != None:
							self.voteMsgTimer.destroy()
							self.voteMsgTimer = None
						self.voteRunning = False
						self.SayAll("§C1001Auto vote has been terminated")
					else:
						mm_utils.PersonalMessage("§C1001Auto vote is already running, type \"!avote cancel\" to stop it!", p)				
				else:
					mm_utils.PersonalMessage("§C1001Vote is already running!", p)
		except:
			self.Info("Exception in AutoVote()")
	
	def onAutoVote(self, data):	
		try:
			if self.voteTimer != None:
				self.voteTimer.destroy()
				self.voteTimer = None
				self.voteMsgTimer.destroy()
				self.voteMsgTimer = None

			vote_result = self.voteList.values()
			self.voteList.clear()
			if len(vote_result) == 0:
				self.SayAll("§C1001Vote failed, nobody voted!", 3)
				self.voteRunning = False
				return

			message = "§C1001Vote:§C1001"
			
			i = 1
			max = 0
			maxKey = ""
			for key, val in self.voteMap.iteritems():
				c = vote_result.count(i)
				if c > max:
					max = c
					maxKey = key
				vres = " §C1001%s:§C1001%d" % (val, c)
				i += 1
				message += vres
			self.SayAll(message)
			message = "%s §C1001WIN!" % self.voteMap[maxKey]
			self.SayAll(message, 3)
			self.AdminPM(message, None)
			
			self.Info("onAVote flag:%d key: %s" % (data, maxKey))
			if data == 1:
				self.aVoteMode = maxKey
				if maxKey.find("skirm") > -1:
					maxKey = "inf"
					data = 2
				else:
					mapsizes = {}
					
					for nextMap in self.mapList:
						map = nextMap.split("|")
						if not mapsizes.has_key(map[3]) and map[2] == self.aVoteMode:											
							size = self.FormatMapProperties(map[3])
							mapsizes[map[3]] = size					
					self.voteMap = mapsizes
										
					message = "§C1001Auto mapvote Size:§C1001"
					i = 1
					for key, val in mapsizes.iteritems():
						message += " §C1001%d:§C1001%s" % (i, val)
						i += 1					
					i -= 1	   
					#message += " | Type §C10011 - %d§C1001 in chat!" % i
					self.voteTimeLeft = self.config.adm_mvoteDuration
					self.voteMsgTimer = bf2.Timer(self.onVoteMsgTimer, 0, 1, message)
					self.voteMsgTimer.setRecurring(self.config.adm_mvoteRecurrence)
					self.voteTimer = bf2.Timer(self.onAutoVote, self.config.adm_mvoteDuration, 1, 2)	
			if data == 2:
				self.aVoteSize = maxKey
				
				mapnames = {}

				for nextMap in self.mapList:
					map = nextMap.split("|")
					if not mapnames.has_key(map[1]) and map[2] == self.aVoteMode and map[3] == self.aVoteSize:											
						name = self.FormatMapProperties(map[1])
						mapnames[map[1]] = name					
				self.voteMap = mapnames
										
				message = "§C1001Auto mapvote Map (§C1001%d maps§C1001):§C1001" % len(self.voteMap)
				i = 1
				for key, val in mapnames.iteritems():
					message += " §C1001%d:§C1001%s" % (i, val)
					i += 1					
				i -= 1	   
				#message += "§C1001 | Type §C10011 - %d§C1001 in chat!" % i
				self.voteTimeLeft = self.config.adm_mvoteDuration
				self.voteMsgTimer = bf2.Timer(self.onVoteMsgTimer, 0, 1, message)
				self.voteMsgTimer.setRecurring(self.config.adm_avoteRecurrence)
				self.voteTimer = bf2.Timer(self.onAutoVote, self.config.adm_avoteDuration, 1, 3)				
			if data == 3:
				self.aVoteMap = maxKey
				
				map = []
				for nextMap in self.mapList:
					map = nextMap.split("|")
					if map[1] == self.aVoteMap and map[2] == self.aVoteMode and map[3] == self.aVoteSize:
						break

				host.rcon_invoke("admin.nextLevel %s" % map[0])
				fMapName = self.FormatMapProperties(map[1])
				fMapType = self.FormatMapProperties(map[2])
				fMapSize = self.FormatMapProperties(map[3])
				self.autoVoteResultMsg = "§C1001" + fMapName + " (" + fMapType + ", " + fMapSize + ")§C1001"
				# Display text
				self.AdminPM("§C1001Next map in rotation set to: §C1001" + fMapName + " (" + fMapType + ", " + fMapSize + ")§C1001", None)
				self.Log("setnext", "autoadmin", "", fMapName + " (" + fMapType + ", " + fMapSize + ")")				
				#self.lastAutoVoteTime = host.timer_getWallTime()
				self.voteRunning = False
		except:
			self.Info("Exception in onAutoVote()")

	def onAutoRunNext(self, data):	
		try:
			if self.voteTimer != None:
				self.voteTimer.destroy()
				self.voteTimer = None
				self.voteMsgTimer.destroy()
				self.voteMsgTimer = None

			vote_result = self.voteList.values()
			if len(vote_result) == 0:
				self.SayAll("§C1001Vote failed, nobody voted!", 3)
				self.voteRunning = False
				return

			self.voteList.clear()
			message = "§C1001Vote:"
			
			i = 1
			max = 0
			maxKey = ""
			for val in self.voteMap:
				c = vote_result.count(i)
				if c > max:
					max = c
					maxKey = val
				vres = " §C1001%s§C1001:§C1001%d§C1001" % (val, c)
				i += 1
				message += vres
			self.SayAll(message)			
			self.voteRunning = False
			if maxKey == "Run next":
				if max < (bf2.playerManager.getNumberOfPlayers() * self.config.adm_autoVoteBalance / 100 - 1):
					message = "§C1001Not enough players took part in vote, to change map it's needed atleast %d\% - 1 player voice!" % self.config.adm_autoVoteBalance
					self.SayAll(message, 3)
					return
				self.AdminPM("§C1001Running next map...", None)
				self.SayAll("§C1001Running next map...")
				host.rcon_invoke('admin.runNextLevel')
				self.Log("admin.runNextLevel", "autoadmin", "", "")
			else:
				message = "§C1001Play this WIN!"
		except:
			self.Info("Exception in onAutoRunNext()")
	#
	# ======================= EVENT HANDLERS =======================
	#


	# Whenever a chat message is sent on any channel, check it for commands; if
	# there are any, check if it's an admin saying it and if so, execute the
	# command
	def onChatMessage(self, playerID, msgText, channel, flags):
		try:
			if len(msgText) > 1 and playerID != -1:
				# Remove unnecessary stuff that precedes the chat
				msgText = msgText.replace("HUD_TEXT_CHAT_TEAM", "")
				msgText = msgText.replace("HUD_TEXT_CHAT_SQUAD", "")
				msgText = msgText.replace("HUD_TEXT_CHAT_DEADPREFIX", "")
				msgText = msgText.replace("HUD_CHAT_DEADPREFIX", "")

				# Remove the space and/or star that preceed the message in chat
				if msgText.startswith("*"):
					msgText = msgText.replace("*", "", 1)
				if msgText.startswith(" "):
					msgText = msgText.replace(" ", "", 1)
				
				#self.Info("Processing chat message: \"%s\"" % (msgText))
				# If the entered text doesn't start with a admin command symbol, cancel
				# further execution
				if not msgText.startswith(self.config.adm_commandSymbol):
					return

				# Split the entered text and remove the admin command symbol
				command = msgText.split(" ")[0].replace(self.config.adm_commandSymbol, "", 1)

				# If the command doesn't exist in the adminCommands dictionary, cancel
				# further execution
				if not self.adminCommands.has_key(command):
					self.Info("The \"%s\" was not a command" % (msgText))
					return

				# Set the P(layer) object
				p = bf2.playerManager.getPlayerByIndex(playerID)

				# If this is a dedicated server and the command is NOT an "open" command
				# (like !r)
				if self.isDedicated and self.config.adm_adminPowerLevels[command] != 777:
					self.Info("Server is dedicated, proceeding with hash checks")

					if self.isAdmin(p) == False:
						return

				# Server is not dedicated, admin commands are available to all human
				# players
				else:
					self.Info("Server is not dedicated (or an 'open' command was used), not performing hash check!")

				# If the server is dedicated and the command is NOT an "open" command,
				# check
				# if the admin has the rights to execute the command
				if self.config.adm_adminPowerLevels[command] != 777:
					if self.isDedicated and self.AdminLevel(p) > self.config.adm_adminPowerLevels[command]:
						self.Info("Admin doesn't have enough rights to execute this command!")
						mm_utils.PersonalMessage("§C1001You do not have sufficient rights to execute this command", p)
						return

				# Execute the command and pass the arguments along as an array (without the
				# admin command symbol and the command)
				self.Info("Executing command now... %s" % (self.config.adm_commandSymbol + command))
				args = msgText.replace(self.config.adm_commandSymbol + command, "", 1).strip().split()
				self.adminCommands[command](command, args, p)
				self.Info("Done executing %s" % (self.config.adm_commandSymbol + command))
		except Exception, e:
			self.Info("Exception in onChatMessage()")
			self.Info(e.message)

	def GetCleanName(self, name):
		cleanName = name
		if name.find(" ") > 0:
			cleanName = name.split()[1]
		else:
			cleanName = name.split()[0]
		return cleanName

	def onPlayerConnectLog(self, p):
		try:			
			self.CreateFile()
			
			dtm = time.strftime("%d/%m/%Y %H:%M:%S UTC", time.gmtime(time.time()))				
			self.logFile.write("[" + dtm + " " + "CONNECT]\t\t" + p.getName() + "\t\t'" + mm_utils.get_cd_key_hash(p) + "'\t " + p.getAddress() + "\n")				
			pName = self.GetCleanName(p.getName())
			banList = self.mm.banManager().getBanList()			
			for key in banList:
				ban = banList[key]
				nick = self.GetCleanName(ban["nick"])
				if nick.lower() == pName.lower():
					reason = "BAN BREAK!"
					self.logFile.write("[" + dtm + " " + "BAN BREAK DETECTED!]\t\t" + p.getName() + "\t\t'" + mm_utils.get_cd_key_hash(p) + "'\t " + p.getAddress() + "\n")				
					self.SayAll("§C1001BANNING PLAYER %s, %s" % (p.getName(), reason))
					self.mm.banManager().banPlayerNow(p, reason, None, None, 'Address', "Auto Admin")
					self.Log(cmd, "Auto Admin", p.getName(), reason)
					return
		except Exception, e:
			self.Info("Exception in onPlayerConnectLog()")
			self.Info(e.message)		

	def onChatLog(self, playerID, msgText, channel, flags):
		try:
			if len(msgText) > 1 and playerID != -1:
				p = bf2.playerManager.getPlayerByIndex(playerID)
				self.CreateFile()
		
				msgText = msgText.replace("HUD_TEXT_CHAT_TEAM", "")
				msgText = msgText.replace("HUD_TEXT_CHAT_SQUAD", "")
				msgText = msgText.replace("HUD_TEXT_CHAT_DEADPREFIX", "DEAD")
				msgText = msgText.replace("HUD_CHAT_DEADPREFIX", "DEAD")

				if msgText.startswith("*"):
					msgText = msgText.replace("*", "", 1)
				if msgText.startswith(" "):
					msgText = msgText.replace(" ", "", 1)

				if channel == "team":
					channel = "Team: " + str(p.getTeam()) + "  "
				elif channel == "squad":
					channel = "Squad: " + str(p.getSquadId()) + " "
				elif channel == "global":
					channel = "Global: "

				dtm = time.strftime("%d/%m/%Y %H:%M:%S UTC", time.gmtime(time.time()))				
				self.logFile.write("[" + dtm + " " + channel + "]  \t" + p.getName() + "\t\t: " + msgText + "\n")				
		except Exception, e:
			self.Info("Exception in onChatLog()")
			self.Info(e.message)

	def onPlayerKilledLog(self, victim, attacker, weapon, assists, object):
		try:		
			if not victim or not attacker: 
				return False
			tk = victim.getTeam() == attacker.getTeam()			
			self.CreateFile()			
			dtm = time.strftime("%d/%m/%Y %H:%M:%S UTC", time.gmtime(time.time()))			
			if tk:
				self.logFile.write("[" + dtm + "\t TEAMKILL]\t" + attacker.getName() + "\t\t TEAMKILLS \t\t" + victim.getName() + "\n")
			else:
				self.logFile.write("[" + dtm + "\t KILL]\t" + attacker.getName() + "\t\t KILLS \t\t" + victim.getName() + "\n")
		except:
			self.Info("Exception in onPlayerKilled()")


	def CreateFile(self):		
		# If the round just started, display a message about it
		if self.logFile == None:
			dtm = time.strftime("%d/%m/%Y %H:%M:%S UTC", time.gmtime(time.time()))			
			self.logFile = DebugLogger("chat", True, True)
			self.logFile.write("Log file created: " + dtm + "\n\n")			

	def onChatMessageVote(self, playerID, msgText, channel, flags):
		try:    		
			if self.voteRunning == True and playerID != -1:				
				# Remove unnecessary stuff that precedes the chat
				msgText = msgText.replace("HUD_TEXT_CHAT_TEAM", "")
				msgText = msgText.replace("HUD_TEXT_CHAT_SQUAD", "")
				msgText = msgText.replace("HUD_TEXT_CHAT_DEADPREFIX", "")
				msgText = msgText.replace("HUD_CHAT_DEADPREFIX", "")

				# Remove the space and/or star that preceed the message in chat
				if msgText.startswith("*"):
					msgText = msgText.replace("*", "", 1)
				if msgText.startswith(" "):
					msgText = msgText.replace(" ", "", 1)

				# Set the P(layer) object
				p = bf2.playerManager.getPlayerByIndex(playerID)

				#Filter 1, 2, 3 and check for the right vote "amount"
				vote_res = filter(self.filterVote, msgText.split())
				if len(vote_res) == 0:
					return
				if len(vote_res) > 1 or int(vote_res[0]) == 0:
					mm_utils.PersonalMessage("§C1001Please specify your choice with only one vote!", p)
					return					
				if len(vote_res) == 1: 
					#If you try to vote with 3 but there are only 2 Maps to vote for, cancel further execution
					vres = int(vote_res[0])
					if vres > len(self.voteMap):
						mm_utils.PersonalMessage("§C1001You can only vote for 1 - %d!" % len(self.voteMap), p)
						return

					#Check for player already voted and if check for double vote else update
					#or insert
					vals = self.voteMap
					try:
						vals = self.voteMap.values()
					except:
						pass
					if self.voteList.has_key(playerID):
						if self.voteList[playerID] != vres:
							self.voteList[playerID] = vres
							mm_utils.PersonalMessage("§C1001Vote was accepted and changed! You voted for: §C1001" + str(vals[vres - 1]), p)
						else:
							mm_utils.PersonalMessage("§C1001You have already voted for: §C1001" + str(vals[vres - 1]), p)
							mm_utils.PersonalMessage("§C1001Stop it! It is not possible to vote more then once for one map! However you can always change your vote!", p)
							host.sgl_sendMedalEvent(playerID, 1220104, 1)
					else:
						self.voteList[playerID] = vres
						mm_utils.PersonalMessage("§C1001Vote was accepted! You voted for: §C1001" + str(vals[vres - 1]), p)
		except:
			self.Info("Exception in onChatMessageVote()")		
	
	def Info(self, msg):
		self.mm.info("AD: " + msg)
	
	def Log(self, cmd, an, pn, text):
		try:
			while len(cmd) < 15:
				cmd += " "
			if pn == "":
				self.Info(cmd.upper() + " performed by '" + an + "': " + text + "\n")
			else:
				self.Info(cmd.upper() + " performed by '" + an + "' on '" + pn + "': " + text + "\n")				
		except:
			self.Info("Exception in Log()")

	# This function constructs the self.mapList
	def ConstructMaplist(self):
		try:
			self.mapList = []
			map_list = host.rcon_invoke("maplist.list").strip().split("\n")

			for map in map_list:
				# Get rid of the " around the mapname
				map = map.replace("\"", "")

				# Split the map, to extract the ID
				map_splitted = map.split(": ")
				map_id = map_splitted[0]

				# Save the map information to the self.mapList
				map_splitted = map_splitted[1].split(" ")

				# Translate mapsize
				if map_splitted[2] == "16":
					map_splitted[2] = "inf"
				elif map_splitted[2] == "32":
					map_splitted[2] = "alt"
				elif map_splitted[2] == "64":
					map_splitted[2] = "std"

				# Add map to array
				mapDetails = str(map_id) + "|" + map_splitted[0] + "|" + map_splitted[1] + "|" + map_splitted[2]
				self.mapList[len(self.mapList):] = [mapDetails]
		except:
			self.Info("Exception in ConstructMaplist")


	# Format mapproperties
	def FormatMapProperties(self, value):
		containsGamemode = False

		# If the string contains the gamemode, replace it with 'words'
		if value.lower().find("gpm_") != -1:
			containsGamemode = True
			value = value.replace("gpm_cnc", "Command And Control")
			value = value.replace("gpm_coop", "COOP")
			value = value.replace("gpm_cq", "AAS")
			value = value.replace("gpm_insurgency", "Insurgency")
			value = value.replace("gpm_skirmish", "Skirmish")
			value = value.replace("gpm_vehicles", "Vehicle Warfare")

		value = value.replace("_", " ")

		# Only "title()" the string when no gamemode is found (otherwise "AAS" would
		# become "Aas", which is lame)
		if value == "inf":
			value += "(x16)"
		elif value == "alt":
			value += "(x32)"
		elif value == "std":
			value += "(x64)"

		if containsGamemode == False:
			value = value.title()

		return value


	# Search for a custom reason
	def FindReason(self, reason):
		try:
			if self.config.adm_reasons.has_key(reason.lower().strip()):				
				reason = self.config.adm_reasons[reason.lower().strip()]
			return reason
		except:
			self.Info("Exception in FindReason()")


	# Send a personal message to all in-game admins.  Argument "p" represents
	# the
	# admin that's causing it
	def AdminPM(self, msg, p):
		# Loop through all players, find all admins
		try:
			if p != None and p.isValid():
				msg += " [" + p.getName() + "]"

			# If we're running a dedicated server, send a personal message, otherwise
			# send a message
			if self.isDedicated == True:
				for pl in bf2.playerManager.getPlayers():			
					if self.isAdmin(pl) == True:
						mm_utils.PersonalMessage(msg, pl)		
			else:
				self.SayAll(msg)
		except:
			self.Info("Exception in AdminPM()")

	def AdminLevel(self, p):
		try:
			if p:
				if p == "none":
					return 777
				cdkeyhash = mm_utils.get_cd_key_hash(p)
				if cdkeyhash != None:
					cdkeyhash = str(cdkeyhash)
				else:
					cdkeyhash = "invalid cdkeyhash"
				profileid = str(p.getProfileId())
				playername = str(p.getName())
				if playername.find(" ") != 0:
					playername = str(playername.split()[1])
				else:
					playername = str(playername.split()[0])
				self.Info("Looking for: %s, %s, %s" % (cdkeyhash, profileid, playername))
				if self.config.adm_adminHashes.has_key(cdkeyhash):
					return self.config.adm_adminHashes[cdkeyhash]
				if self.config.adm_adminHashes.has_key(profileid):
					return self.config.adm_adminHashes[profileid]
				if self.config.adm_adminHashes.has_key(playername):
					return self.config.adm_adminHashes[playername]
				return 777						
		except Exception, e:
			self.Info("Exception in AdminLevel()")
			self.Info(e.message)
			return 777

	# returns true if player (p) is an admin
	def isAdmin(self, player):
		try:
			if player:
				cdkeyhash = mm_utils.get_cd_key_hash(player)
				#self.Info("'%s'" % cdkeyhash)
				profileid = str(player.getProfileId())
				#self.Info("'%s'" % profileid)
				playername = player.getName()
				#self.Info("'%s'" % playername)
				if playername.find(" ") != 0:
					playername = playername.split()[1]
				else:
					playername = playername.split()[0]
				#self.Info("Looking for Admin: %s, %s, %s" % (cdkeyhash, profileid, playername))
				if self.config.adm_adminHashes.has_key(cdkeyhash) or self.config.adm_adminHashes.has_key(profileid) or self.config.adm_adminHashes.has_key(playername):
					return True
				else:					
					return False						
		except:
			self.Info("Unexpected error: IsAdmin()")
			return False

	def filterVote(self, s):
		try:
			return s.isdigit()
		except:
			self.Info("Unexpected error: filterVote()")
			return False

	def shutdown(self):
		"""Shutdown and stop processing."""
		# Flag as shutdown as there is currently way to:
		# host.unregisterHandler
		host.unregisterHandler(self.onChatMessage)
		host.unregisterHandler(self.onChatMessageVote)
		host.unregisterHandler(self.onPlayerChangedSquad)
		host.unregisterHandler(self.onChangedCommander)		
		host.unregisterHandler(self.onChatLog)
		host.unregisterHandler(self.onPlayerConnectLog)
		host.unregisterHandler(self.onPlayerKilledLog)
		host.unregisterGameStatusHandler(self.onGameStatusChanged)			
		self.logFile.close()
		self.__state = 2

def mm_load(modManager):
	"""Creates the Admin object."""
	modManager.debug(1,"calling Admin constructor")
	return Admin(modManager)

# ------------------------------------
# Hash to PBGUID

class utils(object):
	def _bytefy(self, longs):
		# convert a list of 32 bit long to a string
		chars = []
		for n in longs:
			bytes = [(n & 0x000000ffL) >> 0,
						(n & 0x0000ff00L) >> 8,
						(n & 0x00ff0000L) >> 16,
						(n & 0xff000000L) >> 24,]
			chars.extend(bytes)
			
		return ''.join(map(chr, chars))

	def _longfy(self, bytes):
		# convert a string into a list of 32 bit longs
		words = [bytes[i:i + 4] for i in range(0, len(bytes), 4)]
		longs = []
		
		for w in words:
			b = map(ord, w)
			n = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
			longs.append(n)

		return longs

	### md5 implementation

	PADDING = [chr(0x80)] + [chr(0x00)] * 63

	# F, G, H and I are basic MD5 functions

	def F(self, x, y, z):
		return (((x) & (y)) | ((~x) & (z)))

	def G(self, x, y, z):
		return (((x) & (z)) | ((y) & (~z)))

	def H(self, x, y, z):
		return ((x) ^ (y) ^ (z))

	def I(self, x, y, z):
		return ((y) ^ ((x) | (~z)))

	# ROTATE_LEFT rotates x left n bits
	def ROTATE_LEFT(self, x, n):
		return (((x) << (n)) | ((x) >> (32 - (n))))
	
	# FF, GG, HH, and II transformations for rounds 1, 2, 3, and 4

	# Rotation is separate from addition to prevent recomputation

	def XX(self, X, a, b, c, d, x, s, ac):
		a += X(b, c, d)
		a &= 0xffffffffL

		a += x
		a &= 0xffffffffL

		a += ac
		a &= 0xffffffffL

		a = self.ROTATE_LEFT(a, s)
		a &= 0xffffffffL

		a += b
		a &= 0xffffffffL
		return a

	def FF(self, a, b, c, d, x, s, ac):
		return self.XX(self.F, a, b, c, d, x, s, ac)

	def GG(self, a, b, c, d, x, s, ac):
		return self.XX(self.G, a, b, c, d, x, s, ac)

	def HH(self, a, b, c, d, x, s, ac):
		return self.XX(self.H, a, b, c, d, x, s, ac)

	def II(self, a, b, c, d, x, s, ac):
		return self.XX(self.I, a, b, c, d, x, s, ac)

class md5(object):
	def __init__(self, seed=None):
		self.count = [0, 0]

		# load magic initialization constants.
		if seed == None:
			self.buf = [0x67452301L,
						0xefcdab89L,
						0x98badcfeL,
						0x10325476L,]
		else:
			self.buf = seed

		self.in_data = []
	
	def md5(self, data):
		self.update(data)
		return self.hexdigest()

	def update(self, data):
		in_buf = data
		in_len = len(data)

		# compute number of bytes mod 64
		mdi = (self.count[0] >> 3) & 0x3F

		# update number of bits
		if self.count[0] + (in_len << 3) < self.count[0]:
			self.count[1] += 1

		self.count[0] += (in_len << 3)
		self.count[1] += (in_len >> 29)

		part_len = 64 - mdi

		# transform as many times as possible
		if in_len >= part_len:
			self.in_data[mdi:] = in_buf[:part_len]
			self.transform(_longfy(self.in_data))

			i = part_len
			while i + 63 < in_len:
				self.transform(_longfy(in_buf[i:i + 64]))
				i = i + 64
			else:
				self.in_data = list(in_buf[i:in_len])
		else:
			self.in_data.extend(list(in_buf))

	def digest(self):		
		# save number of bits and data
		count = self.count[:]
		in_data = self.in_data[:]
		buf = self.buf[:]
		
		# compute number of bytes mod 64
		mdi = (self.count[0] >> 3) & 0x3F

		# pad out to 56 mod 64
		if mdi < 56:			
			pad_len = 56 - mdi
		else:
			pad_len = 120 - mdi

		self.update(utils.PADDING[:pad_len])

		# append length in bits and transform
		bits = utils._longfy(utils(), self.in_data[:56]) + count

		self.transform(bits)

		digest = utils._bytefy(utils(), self.buf)

		# copy number of bits and data back
		self.count = count
		self.in_data = in_data
		self.buf = buf

		return digest

	def hexdigest(self):
		d = ''.join(['%02x' % ord(x) for x in self.digest()])
		return d

	def transform(self, x):
		a, b, c, d = self.buf

		# round 1
		S11, S12, S13, S14 = 7, 12, 17, 22		
		
		a = utils.FF(utils(), a, b, c, d, x[0], S11, 0xD76AA478L)
		d = utils.FF(utils(), d, a, b, c, x[1], S12, 0xE8C7B756L)
		c = utils.FF(utils(), c, d, a, b, x[2], S13, 0x242070DBL)
		b = utils.FF(utils(), b, c, d, a, x[3], S14, 0xC1BDCEEEL)
		a = utils.FF(utils(), a, b, c, d, x[4], S11, 0xF57C0FAFL)
		d = utils.FF(utils(), d, a, b, c, x[5], S12, 0x4787C62AL)
		c = utils.FF(utils(), c, d, a, b, x[6], S13, 0xA8304613L)
		b = utils.FF(utils(), b, c, d, a, x[7], S14, 0xFD469501L)
		a = utils.FF(utils(), a, b, c, d, x[8], S11, 0x698098D8L)
		d = utils.FF(utils(), d, a, b, c, x[9], S12, 0x8B44F7AFL)
		c = utils.FF(utils(), c, d, a, b, x[10], S13, 0xFFFF5BB1L)
		b = utils.FF(utils(), b, c, d, a, x[11], S14, 0x895CD7BEL)
		a = utils.FF(utils(), a, b, c, d, x[12], S11, 0x6B901122L)
		d = utils.FF(utils(), d, a, b, c, x[13], S12, 0xFD987193L)
		c = utils.FF(utils(), c, d, a, b, x[14], S13, 0xA679438EL)
		b = utils.FF(utils(), b, c, d, a, x[15], S14, 0x49B40821L)

		# round 2
		S21, S22, S23, S24 = 5, 9, 14, 20

		a = utils.GG(utils(), a, b, c, d, x[1], S21, 0xF61E2562L)
		d = utils.GG(utils(), d, a, b, c, x[6], S22, 0xC040B340L)
		c = utils.GG(utils(), c, d, a, b, x[11], S23, 0x265E5A51L)
		b = utils.GG(utils(), b, c, d, a, x[0], S24, 0xE9B6C7AAL)
		a = utils.GG(utils(), a, b, c, d, x[5], S21, 0xD62F105DL)
		d = utils.GG(utils(), d, a, b, c, x[10], S22, 0x02441453L)
		c = utils.GG(utils(), c, d, a, b, x[15], S23, 0xD8A1E681L)
		b = utils.GG(utils(), b, c, d, a, x[4], S24, 0xE7D3FBC8L)
		a = utils.GG(utils(), a, b, c, d, x[9], S21, 0x21E1CDE6L)
		d = utils.GG(utils(), d, a, b, c, x[14], S22, 0xC33707D6L)
		c = utils.GG(utils(), c, d, a, b, x[3], S23, 0xF4D50D87L)
		b = utils.GG(utils(), b, c, d, a, x[8], S24, 0x455A14EDL)
		a = utils.GG(utils(), a, b, c, d, x[13], S21, 0xA9E3E905L)
		d = utils.GG(utils(), d, a, b, c, x[2], S22, 0xFCEFA3F8L)
		c = utils.GG(utils(), c, d, a, b, x[7], S23, 0x676F02D9L)
		b = utils.GG(utils(), b, c, d, a, x[12], S24, 0x8D2A4C8AL)

		# round 3
		S31, S32, S33, S34 = 4, 11, 16, 23
		
		a = utils.HH(utils(), a, b, c, d, x[5], S31, 0xFFFA3942L)
		d = utils.HH(utils(), d, a, b, c, x[8], S32, 0x8771F681L)
		c = utils.HH(utils(), c, d, a, b, x[11], S33, 0x6D9D6122L)
		b = utils.HH(utils(), b, c, d, a, x[14], S34, 0xFDE5380CL)
		a = utils.HH(utils(), a, b, c, d, x[1], S31, 0xA4BEEA44L)
		d = utils.HH(utils(), d, a, b, c, x[4], S32, 0x4BDECFA9L)
		c = utils.HH(utils(), c, d, a, b, x[7], S33, 0xF6BB4B60L)
		b = utils.HH(utils(), b, c, d, a, x[10], S34, 0xBEBFBC70L)
		a = utils.HH(utils(), a, b, c, d, x[13], S31, 0x289B7EC6L)
		d = utils.HH(utils(), d, a, b, c, x[0], S32, 0xEAA127FAL)
		c = utils.HH(utils(), c, d, a, b, x[3], S33, 0xD4EF3085L)
		b = utils.HH(utils(), b, c, d, a, x[6], S34, 0x04881D05L)
		a = utils.HH(utils(), a, b, c, d, x[9], S31, 0xD9D4D039L)
		d = utils.HH(utils(), d, a, b, c, x[12], S32, 0xE6DB99E5L)
		c = utils.HH(utils(), c, d, a, b, x[15], S33, 0x1FA27CF8L)
		b = utils.HH(utils(), b, c, d, a, x[2], S34, 0xC4AC5665L)

		# round 4
		S41, S42, S43, S44 = 6, 10, 15, 21

		a = utils.II(utils(), a, b, c, d, x[0], S41, 0xF4292244L)
		d = utils.II(utils(), d, a, b, c, x[7], S42, 0x432AFF97L)
		c = utils.II(utils(), c, d, a, b, x[14], S43, 0xAB9423A7L)
		b = utils.II(utils(), b, c, d, a, x[5], S44, 0xFC93A039L)
		a = utils.II(utils(), a, b, c, d, x[12], S41, 0x655B59C3L)
		d = utils.II(utils(), d, a, b, c, x[3], S42, 0x8F0CCC92L)
		c = utils.II(utils(), c, d, a, b, x[10], S43, 0xFFEFF47DL)
		b = utils.II(utils(), b, c, d, a, x[1], S44, 0x85845DD1L)
		a = utils.II(utils(), a, b, c, d, x[8], S41, 0x6FA87E4FL)
		d = utils.II(utils(), d, a, b, c, x[15], S42, 0xFE2CE6E0L)
		c = utils.II(utils(), c, d, a, b, x[6], S43, 0xA3014314L)
		b = utils.II(utils(), b, c, d, a, x[13], S44, 0x4E0811A1L)
		a = utils.II(utils(), a, b, c, d, x[4], S41, 0xF7537E82L)
		d = utils.II(utils(), d, a, b, c, x[11], S42, 0xBD3AF235L)
		c = utils.II(utils(), c, d, a, b, x[2], S43, 0x2AD7D2BBL)
		b = utils.II(utils(), b, c, d, a, x[9], S44, 0xEB86D391L)

		self.buf[0] = (self.buf[0] + a) & 0xffffffffL
		self.buf[1] = (self.buf[1] + b) & 0xffffffffL
		self.buf[2] = (self.buf[2] + c) & 0xffffffffL
		self.buf[3] = (self.buf[3] + d) & 0xffffffffL

def pb_md5_magic(seed):
	return [(seed * 11) + 0x67452301L,
			(seed * 71) - 0x10325477L,
			(seed * 37) - 0x67452302L,
			(seed * 97) + 0x10325476L]

def calculate_md5(data, seed=0):
	m = md5(pb_md5_magic(seed))
	return m.md5("".join(data))

def cdhash_to_pbguid(hash):
	try:
		cdhashlist = list(hash)

		cdhashlist[0] = '7'
		cdhashlist[len(cdhashlist) - 1] = '\x00'
		cdhashlist = calculate_md5(cdhashlist, 0x12063)
		cdhashlist = calculate_md5(cdhashlist, 0x11c85)

		return "".join(cdhashlist)
	except:
		self.Info("Exception in cdhash_to_pbguid()")

class DebugLogger:
	"""The logger used for debugging ModManager."""
	def __init__(self, filename, logAppend, autoFlush):
		"""Opens the given filename for appending."""
		self.autoFlush = autoFlush
		dtm = time.strftime("_%Y%m%d_%H%M", time.gmtime(time.time()))
		fname = filename + dtm + ".log"
		try:
			if logAppend:
				self.__file = open(fname, 'a+')
			else:
				self.__file = open(fname, 'w+')

		except StandardError, detail:
			msg = "Failed to open '%s' (%s)" % (fname, detail)
			raise IOError, msg

	def write(self, str):
		"""Writes to the debug log flushing if required."""
		self.__file.write(str)
		if self.autoFlush:
			self.__file.flush()

	def close(self):
		"""Close the debug log."""
		if self.__file:
			self.__file.close()