# vim: ts=4 sw=4 noexpandtab
"""Debug module.

This is a Debug ModManager module

===== Config =====

===== History =====
 v1.0 - 30/10/2006:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import bf2
import host
import mm_utils

# Set the version of your module here
__version__ = 1.0

# Set the required module versions here
__required_modules__ = {
	'modmanager': 1.6
}

# Does this module support reload ( are all its reference closed on shutdown? )
__supports_reload__ = True

# Sets which games this module supports
__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True
}

# Set the description of your module here
__description__ = "Debug v%s" % __version__

# Add all your configuration options here
configDefaults = {
}

class Debug( object ):
	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0

		# Add any static initialisation here.
		# Note: Handler registration should not be done here
		# but instead in the init() method

	def onPlayerConnect( self, player ):
		"""Outputs the player rank on connect."""
		if 1 != self.__state:
			return 0

		# Put your actions here
		self.mm.info( "Player(%d,%d,%s) is rank %d" % ( player.index, player.getProfileId(), player.getName(), player.score.rank ) )

	def onStatsResponse( self, succeeded, player, stats ):
		"""Outputs details about the stats response of a player."""
		if 1 != self.__state:
			return 0

		if player is None:
			self.mm.error( "Received stats for None player!" )
			return 0

		if self.mm.isBattleField2():
			rank_key = "rank"
			if "<html>" in stats:
				self.mm.error( "The stats response seems wrong:" )
				self.mm.error( stats )
				self.mm.error( "<end-of-stats>" )
				return 0
		else:
			rank_key = "rnk"
			if "<html>" in stats or "server" not in stats:
				self.mm.error( "The stats response seems wrong:" )
				self.mm.error( stats )
				self.mm.error( "<end-of-stats>" )
				return 0

		if not rank_key in stats:
			self.mm.error( "Rank not found for player %s!" % player.getName() )
			return 0

		self.mm.info( "Rank %s received for player(%d,%d,%s)" % ( host.pers_getStatsKeyVal( rank_key, player.getProfileId() ), player.index, player.getProfileId(), player.getName() ) )

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )

		# Register your game handlers and provide any
		# other dynamic initialisation here

		if not bf2.g_debug:
			self.mm.info( "Global python debugging is disabled" )
			self.mm.info( "To enable edit: python/bf2/__init__.py" )
			self.mm.info( "and set 'g_debug = 1'" )
		else:
			self.mm.warn( "Global python is enabled." )
			self.mm.warn( "This may have unexpected side effects and a performance impact!" )

		if not host.ss_getParam('ranked'):
			self.mm.error( "This server is NOT ranked!" )
		else:
			self.mm.info( "This server is ranked!" )
			if 0 == self.__state:
				# Register your host handlers here
				host.registerHandler( 'PlayerConnect', self.onPlayerConnect, 1 )
				host.registerHandler( 'PlayerStatsResponse', self.onStatsResponse, 1 )

			# Update to the running state
			self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway

		# Flag as shutdown as there is currently way to:
		# host.unregisterHandler
		self.__state = 2

	def update( self ):
		"""Process and update.
		Note: This is called VERY often processing in here should
		be kept to an absolute minimum.
		"""
		pass

def mm_load( modManager ):
	"""Creates and returns your object."""
	return Debug( modManager )
