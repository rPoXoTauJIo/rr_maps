# vim: ts=4 sw=4 noexpandtab
""" Team autobalance system.

This is a autobalance system ModManager module

===== Config =====

 # Allow Commander if 0 then we never autobalance the commander
 mm_autobalance.allowCommander 0
 
 # Allow Squad Leader if 0 then we only autobalance squad leaders
 # if they are the only member of that squad
 mm_autobalance.allowSquadLeader 0
 
 # Allow Squad Member if 0 then we only autobalance squad members
 # if there are no none squad members / commander on the team
 mm_autobalance.allowSquadMember 0
 
 mm_autobalance.clantags ["clantag1","clantag2"...]
 
 # Allows plays to be switched teams at the end of a round
 # 0 => No swap
 # 1 => Swap teams
 # 2 => Randomise teams
 mm_autobalance.roundSwitch

===== History =====
v2.8 20/04/2013:
made some fixes

v2.7 - 14/04/2013:
Clan autodetect added. Copyright: CSP.Wizard.

v2.6 - 14/04/2013:
Clan autobalance added. Copyright: CSP.Wizard.

 v2.5 - 12/10/2011:
 Fixed being able to load on Heroes

 v2.4 - 12/10/2011:
 Added BFP4F Support

 v2.3 - 14/07/2009:
 Disabled this module for Heroes as its never valid due to the fixed player classes
 
 v2.2 - 07/10/2006:
 Fixed off by one issue on player connect

 v2.1 - 03/10/2006:
 Merged with ClanMatch and enhanced to have multiple on round change methods
 
 v2.0 - 13/09/2006:
 Enhancements / fixes merged from BF2142 Closed BETA 2
 
 v1.9 - 30/08/2006:
 Added supported games
 Included changes from BF2142 Tuning BETA 2

 v1.8 - 13/07/2006
 Added gpm_coop checks from v1.4 patch

 v1.7 - 20/05/2006:
 Added gpm_coop check from v1.3 patch
 
 v1.6 - 08/08/2005:
 Fix for player joining during pre / post game not being balanced
 correctly.

 v1.5 - 03/08/2005:
 Optimised onPlayerConnect team check
 
 v1.4 - 21/07/2005:
 Flagged as reload safe
 
 v1.3 - 13/07/2005:
 Enhanced squad based autobalance descision making to take
 into account team composition.
 
 v1.2 - 09/07/2005:
 Added commander, and squad balance options
 
 v1.1 - 30/06/2005:
 Updated to ModManager format by Steven 'Killing' Hartland
 
 v1.0:
 Created by: DICE
"""

import bf2
import host
import random
import sys
import mm_utils


__version__ = 2.8

__required_modules__ = {
	'modmanager': 1.6
}

__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bfheroes': False,
	'bfp4f': True,
	'pr': True,
}

__description__ = "ModManager Team autobalance v%s" % __version__

configDefaults = {
	'allowCommander': 0,
	'allowSquadLeader': 0,
	'allowSquadMember': 0,
	'roundSwitch': 0,
	'clantags':[],
}

class AutoBalance(object):

	def __init__(self, modManager):
		self.mm = modManager
		self.__state = 0

	def onPlayerConnect(self, p):
		"""Autobalance the new player if required."""
		try:			
			if 1 != self.__state:
				return
			
			if self.mm.isBattleField2142() and not p.isValid():
				return

			# dont team switch alive players, or they will have the wrong teams kit
			if p.isAlive():
				return
		
			clanTags = getClanTags()
			clanPlayers = dict.fromkeys(clanTags,[0,0])
			t1cCount = 0
			t2cCount = 0
			pClan = ""
			isClanPlayer = 0
			name = p.getName() 
			for clan in clanTags:
				if name.find(clan) == 0: 
					isClanPlayer = 1
					pClan = clan
					break
				
			# place player on the team with least players
			team1 = bf2.playerManager.getNumberOfPlayersInTeam(1)
			team2 = bf2.playerManager.getNumberOfPlayersInTeam(2) 
			for tp in bf2.playerManager.getPlayers():
				t1 = 1 == tp.getTeam()
				name = tp.getName() 
				for clan in clanTags:
					if name.find(clan) == 0: 
						if t1:
							clanPlayers[clan][0] += 1
							t1cCount += 1
						else:
							clanPlayers[clan][1] += 1
							t2cCount += 1
						break

			# Ignore the new player's team entry
			# N.B.  Doing it this way avoids a loop level check
			if 1 == p.getTeam():
				team1 -= 1
			else:
				team2 -= 1
			team2 = (team2 * bf2.serverSettings.getTeamRatioPercent() / 100.0)
			self.Info("AB: Connect T1-T2: %d" % (team1 - team2))
			pTeam = 1
			if not isClanPlayer or abs(team2 - team1) > 2:
				if team2 > team1:
					pTeam = 1
				elif (team2 == team1):
					if t1cCount > t2cCount:
						pTeam = 1
					else:
						pTeam = 2
				else:
					pTeam = 2
			else:
				self.Info("AB: Connect TC1-TC2: %d" % (t1cCount - t2cCount))
				t1 = clanPlayers[pClan][0] > clanPlayers[pClan][1]
				if clanPlayers[pClan][0] > 0 or clanPlayers[pClan][1] > 0:
					self.Info("AB: Connect TPC1-TPC2 '%s': %d" % (pClan, clanPlayers[pClan][0] - clanPlayers[pClan][1]))
					if t1:
						pTeam = 1
					else:
						pTeam = 2					
				elif t1cCount < t2cCount:
					pTeam = 1
				else:
					pTeam = 2
			p.setTeam(pTeam)
			self.Info("AB: Player Connect: \"%s\" Clan: \"%s\" Set team %d" % (name, pClan, pTeam))
		except:
			self.Error("AB: Unexpected error: onPlayerConnect")

	def onPlayerDeath(self, p, vehicle):
		"""Autobalance a player that has died if required and allowed by the balance rules."""
		try:
			if 1 != self.__state:
				return

			if p == None or not p.isValid():
				return

			team1 = bf2.playerManager.getNumberOfPlayersInTeam(1)
			team2 = bf2.playerManager.getNumberOfPlayersInTeam(2) 
			team2 = team2 * bf2.serverSettings.getTeamRatioPercent() / 100.0

			self.Info("AB: Player death: \"%s\" isCommander: \"%d\" isSL: \"%d\" T1-T2: %d" % (p.getName(), p.isCommander(), p.isSquadLeader(), (team1 - team2)))
			if not abs(team2 - team1) > 1:
				return
			#if not bf2.serverSettings.getAutoBalanceTeam():
			#	return

			# dont use autobalance when its suicide/changes team
			if p.getSuicide():
				p.setSuicide(0)
				return
			
			if (not self.__config['allowCommander']) and p.isCommander():
				# dont autobalance the commander
				return

			squadid = p.getSquadId()
			teamid = p.getTeam()
			players = bf2.playerManager.getPlayers()

			if (not self.__config['allowSquadLeader']) and p.isSquadLeader():
				# only autobalance the squad leader if they are the only
				# member of that squad
				squad_members = 0
				for tp in players:
					if squadid == tp.getSquadId() and tp.index != p.index:
						# we have other members in this squad dont autobalance
						#self.mm.debug( 2, "AB: no ( squad leader with members )" )
						return
			
			t1cCount = 0
			t2cCount = 0

			if (not self.__config['allowSquadMember']) and (squadid > 0):
				# only autobalance squad members if there are no none
				# squad members / commander on this team
				basic_players = 0
				for tp in players:
					if (0 == tp.getSquadId()) and (teamid == tp.getTeam()) and (not tp.isCommander()):
						# none squad member / commander of this team
						basic_players += 1
				#self.Info("AB: Player death T1-T2: %d" % (team1 - team2))
				if 0 != basic_players and abs(team1 - team2) < 3:
					# we have basic players in this team we
					# will balance them instead
					self.Info("AB: no ( basic players avail ) T1: %d T2: %d" % (t1cCount, t2cCount))
					return
			
			clanTags = getClanTags()
			clanPlayers = dict.fromkeys(clanTags,[0,0])
			
			pClan = ""
			isClanPlayer = 0
			name = p.getName() 
		
			for clan in clanTags:
				if name.find(clan) == 0: 
					isClanPlayer = 1
					pClan = clan
					break
		
			aiPlayerBalance = 0
			
			for tp in players:
				t1 = 1 == tp.getTeam()
				name = tp.getName() 
				for clan in clanTags:
					if name.find(clan) == 0: 
						if t1:
							clanPlayers[clan][0] += 1
							t1cCount += 1
						else:
							clanPlayers[clan][1] += 1
							t2cCount += 1
						break
			
			if pClan in clanPlayers:
				if (clanPlayers[pClan][teamid - 1] == 1):
					isClanPlayer = 0
						
			self.Info("AB: Switch T1-T2: %d" % (team1 - team2))
			pTeam = 0
			if (not isClanPlayer and abs(team2 - team1) > 1) or abs(team2 - team1) > 2:
				if (teamid == 1):
					if (team2 + 1) < team1:
						#self.mm.debug( 2, "AB: player '%s' -> team %d" % ( p.getName(), 2 ) )
						pTeam = 2					
				else:
					if (team1 + 1) < team2:
						#self.mm.debug( 2, "AB: player '%s' -> team %d" % ( p.getName(), 1 ) )
						pTeam = 1
				if pTeam > 0:
					p.setTeam(pTeam)			
					self.Info("AB: Player Switch: \"%s\" Clan: \"%s\" Set team %d" % (name, pClan, pTeam))
		except:
			self.Error("AB: Unexpected error: onPlayerDeath")		

	def onPlayerChangeTeams(self, p, humanHasSpawned):
		"""Ensure the player isnt unbalancing the teams."""
		try:
			if 1 != self.__state:
				return

			self.mm.debug(2, "AB: change")

			#if not bf2.serverSettings.getAutoBalanceTeam():
			#	return

			# dont teamswitch alive players, or they will have the wrong teams kit
			if p.isAlive():
				return

			# checking to see if player is allowed to change teams
			clanTags = getClanTags()
			pClan = ""
			isClanPlayer = 0
			name = p.getName() 
			for clan in clanTags:
				if name.find(clan) == 0: 
					isClanPlayer = 1
					pClan = clan
					break

			team1 = bf2.playerManager.getNumberOfPlayersInTeam(1)
			team2 = bf2.playerManager.getNumberOfPlayersInTeam(2) 
			
			self.Info("AB: Player tried to Switch: \"" + name + "\" Clan:\"" + pClan + "\"")
			team2 = team2 * bf2.serverSettings.getTeamRatioPercent() / 100.0
			self.Info("AB: PSwitch T1-T2: %d" % (team1 - team2))
			if (abs(team1 - team2) > 1 and not isClanPlayer) or abs(team1 - team2) > 2:
				if p.getTeam() == 1 and team2 < team1:
					p.setTeam(2)
					self.Info("AB: Player Switch back: \"" + p.getName() + "\" Set team 2")
				elif team2 > team1:
					p.setTeam(1)
					self.Info("AB: Player Switch back: \"" + p.getName() + "\" Set team 1")
		except:
			self.Error("AB: Unexpected error: onPlayerChangeTeams")

	def onGameStatusChanged(self, status):
		"""Make a note of the game status"""
		"""Switch players to the other team if end of round"""
		try:
			if 0 != self.__config['roundSwitch'] and bf2.GameStatus.PreGame == status and bf2.GameStatus.EndGame == self.mm.lastGameStatus:
				# End of round so swap players
				
				if 1 == self.__config['roundSwitch']:
					try:
						# Straight swap
						t1 = 0
						t2 = 0
						clanTags = getClanTags()
						clanPlayers = dict.fromkeys(clanTags,[0,0])
						t1cCount = 0
						t2cCount = 0
						for player in bf2.playerManager.getPlayers():
							if player != None and player.isValid():						
								# avoid autobalance changing us back
								player.setSuicide(1)
								# Change their team
								if 1 == player.getTeam():
									player.setTeam(2)
									t2 += 1
								else:
									player.setTeam(1)
									t1 += 1
						
								isT1 = 1 == player.getTeam()
								name = player.getName() 
								for clan in clanTags:
									if name.find(clan) == 0: 
										if isT1:
											clanPlayers[clan][0] += 1
											t1cCount += 1
										else:
											clanPlayers[clan][1] += 1
											t2cCount += 1
										break
					except:
						self.Error("AB: Unexpected error: onGameStatusChanged in swap mudule")
					try:
						#autobalance teams
						if abs(t1 - t2 * bf2.serverSettings.getTeamRatioPercent() / 100.0) > 1:
							dif = abs(t1 - t2)
							swichT = 1
							if t1 > t2:
								swichT = 0
							clanSwitched = 0
							if abs(t1cCount - t2cCount) >= dif and ((t1cCount > t2cCount and not switchT) or (t1cCount < t2cCount and switchT)):
								for clan in clanTags:
									if clanPlayers[clan][switchT] == dif or clanPlayers[clan][switchT] == (dif + 1) or clanPlayers[clan][switchT] == (dif - 1):
										for player in bf2.playerManager.getPlayers():
											if player.isValid() and player.getName().find(clan) == 0:
												if switchT == 0:
													player.setTeam(2)
												else:
													player.setTeam(1)
												dif -= 1
										clanSwitched = 1
										break
							if dif > 0:
								for player in bf2.playerManager.getPlayers():
									for clan in clanTags:
										if player.isValid() and player.getName().find(clan) != 0:
											if switchT == 0:
												player.setTeam(2)
											else:
												player.setTeam(1)
											dif -= 1
											break
									if dif == 0:
										break
					except:
						self.Error("AB: Unexpected error: onGameStatusChanged in ab module")

										
				elif 2 == self.__config['roundSwitch']:
					# Randomise
					random.seed()
					players = bf2.playerManager.getPlayers()
					random.shuffle(players)
					i = 1
					half = int(len(players) / 2)
					for player in players:
						# avoid autobalance changing us back
						player.setSuicide(1)
						# Change their team
						if i <= half:
							player.setTeam(1)
						else:
							player.setTeam(2)
						i += 1
		except:
			self.Error("AB: Unexpected error: onGameStatusChanged")

	def onPlayerDisconnect(self, disconnectedPlayer):
		"""Try to rebalance players on mass disconnect"""	
		try:
			#if not bf2.serverSettings.getAutoBalanceTeam():
			#	return
			self.Info("AB: Player disconnect: \"" + disconnectedPlayer.getName() + "\"")
			team1 = bf2.playerManager.getNumberOfPlayersInTeam(1)
			team2 = bf2.playerManager.getNumberOfPlayersInTeam(2) 
			
			team2 = team2 * bf2.serverSettings.getTeamRatioPercent() / 100.0
			if 	abs(team1 - team2) < 2:				
				return
			#autobalance teams
			self.Info("AB: Trying to balance PDisconnect T1-T2: %d" % (team1 - team2))
			teamid = 2
			if team1 > team2:
				teamid = 1
			steam = 1
			if teamid == 1:
				steam = 2
			else:
				steam = 1
			tPlayers = []
			for player in bf2.playerManager.getPlayers():
				if player.isValid() and not player.isAlive() and (teamid == player.getTeam()):
					tPlayers.append(player)
			
			for player in tPlayers:
				if (0 == player.getSquadId()) and (not player.isCommander()) and dif > 1:
					isClanPlayer = 0
					for clan in clanTags:
						if player.getName().find(clan) == 0:
							isClanPlayer = 1
							break
					if not isClanPlayer:
						player.setSuicide(1)
						player.setTeam(steam)
						self.Info("AB: Player Switch on disconnect: \"%s\" Set team %d" % (player.getName(), steam))
						dif -= 1

			if dif > 1:
				for player in tPlayers:
					if (not player.isSquadLeader()) and (not player.isCommander()) and dif > 1:
						isClanPlayer = 0
						for clan in clanTags:
							if player.getName().find(clan) == 0:
								isClanPlayer = 1
								break
						if not isClanPlayer:
							player.setSuicide(1)
							player.setTeam(steam)
							self.Info("AB: Player Switch on disconnect: \"%s\" Set team %d" % (player.getName(), steam))
							dif -= 1

			if dif > 1:
				for player in tPlayers:
					if (not player.isSquadLeader()) and (not player.isCommander()) and dif > 1:
						player.setSuicide(1)
						player.setTeam(steam)
						self.Info("AB: Player Switch on disconnect: \"%s\" Set team %d" % (player.getName(), steam))
						dif -= 1

		except:
			self.Error("AB: Unexpected error: onPlayerDisconnect")

	def init(self):
		"""Provides default initialisation."""
		self.__config = self.mm.getModuleConfig(configDefaults)

		# Register our game handlers
		if 0 == self.__state:
			host.registerHandler('PlayerConnect', self.onPlayerConnect, 1)
			host.registerHandler('PlayerDeath', self.onPlayerDeath, 1)
			host.registerHandler('PlayerChangeTeams', self.onPlayerChangeTeams, 1)
			#host.registerHandler('PlayerDisconnect', self.onPlayerDisconnect, 1)

		# Register your game handlers and provide any
		# other dynamic initialisation here
		host.registerGameStatusHandler(self.onGameStatusChanged)

		self.__state = 1

	def Info(self, msg):
		#self.mm.info(msg)
		return

	def Error(self, msg):
		self.mm.info(msg)

	def shutdown(self):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway
		host.unregisterGameStatusHandler(self.onGameStatusChanged)
		host.unregisterHandler(self.onPlayerConnect)
		host.unregisterHandler(self.onPlayerDeath)
		host.unregisterHandler(self.onPlayerChangeTeams)
		#host.unregisterHandler(self.onPlayerDisconnect)
		
		# Flag as shutdown as there is currently way to do this
		self.__state = 2

def getClanTags():
	clanTags = []
	tClans = []
	players = bf2.playerManager.getPlayers()
	for tp in players:
		try:
			name = tp.getName()
			if name.find(" ") > 0:
				clan = name.split()[0]
				if not clan in clanTags:
					clanTags.append(clan)
				#if clan in tClans:
				#	clanTags.append(clan)
				#else:
				#	tClans.append(clan)
		except:
			pass
	return clanTags


def mm_load(modManager):
	"""Creates the auto balance object."""
	return AutoBalance(modManager)
