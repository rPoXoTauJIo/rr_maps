
adm_kickTime = 1		# In time a player is kicked
adm_banTime = 180		# Time in minutes a player is temp banned (if you use the temp-ban command,
                 		# normal ban is forever!).  Note: if the server is
                                    		# restarted, the ban is
                                                       		# lifted
usePunkbuster = False
adm_commandSymbol = "!"	# Admincommand symbol
adm_maxAltitude = 1000	# Define the maximum altitude (used in the fly-command)
adm_mvoteDuration = 90	# Time how long a mapvote will take
adm_avoteDuration = 180
adm_mvoteRecurrence = 15 # Time between the !mvote message pops up in the upper left corner
adm_avoteRecurrence = 30
adm_squadRecurrence = 10 
adm_squadTimeAllowed = 90
adm_autoVoteTimer = 20 # limitation in minutes for autovoting, to prevent spam
adm_autoVoteDelay = 5
adm_autoVoteBalance = 50

adm_adminHashes = {  	# Array in which the names of the administrators will be saved.  Make sure
                  		# there are NO duplicates!
"cb86c64c89fe9b70c6cb41f99ef5f6ce": 0,  # zloyrash , SuperAdmin
"e1ea6cb9a6690db80521a7452c063977": 1,  # Unmanned / Sober, InGameAdmin
"a6468f275982b29df4f30d8a89b45460": 1,  # PReferens, InGameAdmin
"787c499fc4d1d4ff444abeb3ae64f84c": 1,  # Bishop.A , InGameAdmin
"a35d8486d3115572f025047c3ca6e3c7": 1,  # Kittenko , InGameAdmin
"87cb4e207de668d32783fb63cd29be88": 2,  # roofer_nsk , InGameAdmin
"7c5bfc02e59a52197fb0a6dbb6edc237": 1,  # _Reality_r , InGameAdmin
"abbf34140c3465e9962ea30ea70dcebb": 2,  # KIA Dantist , InGameAdmin
"3e53c1fdd4106b90afc929d26ce9ee47":	0,  # Flechis , InGameAdmin	
"caa1936fad0301ad63a2ced18d5f9088": 1,  # D}ll{EM , InGameAdmin
"f828e81f291b0596844dfbf9471bb23d":	0,  # Akvian , InGameAdmin
"6e2f653b6abe8e9edf772728170a0d45":	0,  # GLUK , InGameAdmin
"fb60dc480f0c51440a9eef45dc80d514":	1,  # KIA Gimley , InGameAdmin
"9a856b769e51ff21457f3c4f0a958a9b":	0,  # SRF Mojo, InGameAdmin
"23fb10dadaeae76bb5d9281f1d7840e7":	1,  # SRF MrGorin, InGameAdmin
"64484dd1e048a872ba740232459c091f":	1,  # ViLKiS , InGameAdmin
"4f89618f9bf3c9cdb10c78847223a240":	1,  # Kasper63 , InGameAdmin
"d781b91d754574605262b8d07ddaba92":	1,  # rusvitalik , Assistant
"084ef46ef82a66fc33c350d356b256da": 2,  # Andryghan , Assistant
"a9c3401734fb750b0a5c3fcbdb34b0ac": 1,  # PYCb EasyGess , InGameAdmin
"685fba37925a22d13cc64e88db17c4d9": 1,	# [e!]TiP , InGameAdmin
"b9f3a94a336053819e23d95d17e13c6a": 1,	# <A>EPOXA , InGameAdmin
"bcb9ec73fd939227e3581bcea5881732":	1,	# ZUBR , InGameAdmin
"cf7ae3082d6a66776a0eff6f2d3f60dc":	1,	# Dyson , InGameAdmin
"349c80d3afe0942c755e09660bc7904f":	1,	# KIA Chuva , InGameAdmin
"4f78b1f0ccfd01870a9ed8f57b29950c":	1,	# MireX , InGameAdmin
"3989c20f634b2253044e935b8e6cd486":	1,	# rpoxo , InGameAdmin
}

adm_adminPowerLevels = {	
						# Rights management.  The lower the powerlevel, the more power one has.
						# Two
                       	# powerlevels are defined by default, but you can
                       	# define as many as you want.
						# 0: Superadmin, can do everything.  1: Moderator, can't do everything.
                       						# 2: Meant to use for liteadmins.  777: used for
                       						# commands that everyone
                       						# can use
	# Map control
	
"change":		0,# Change to a next map and run it
"reload":		0,# Reload the current map
"remove":		0,# Remove a map from the maplist
"restart":		1,# Restart the round
"runnext":		1,# Run the next map
"save":			0,# Save the maplist
"maplist":		1,# Shows the maplist to user
"setnext":		1,# Set a next map
"mvote":		0,# Initializes a server mapvote between 2-3 maps.  People can then vote
            			# with either writing 1,2 or 3 in chat.  All admins will receive a
                       		 # message
                                    # which map won after a configured time.
"mapvote":		0,# same as mvote
            # Player control
"b":			2,# Ban a player
"ban":			2,# Ban a player (same as !b)
"ab":			0,# Ban a player
"aban":			0,# Ban a player (same as !ab)
"banlist":		2,
"ub":			2,# Unbans the player
"unban":		2,# same as !ub
"fly":			0,# Send a player up in the air
"hash":			2,# Retrieves the hash of certain player
"k":			2,# Kick a player
"kick":			2,# Kick a player (same as !k)
"kill":			2,# Kill a player
"resign":		2,# Resign a player from being squad leader or commander
"ss":			0,# Take a screenshot of a player (through punkbuster)
"switch":		2,# Teamswitch a player
"tb":			2,# Temporary ban a player (basically extended 'kick')
"w":			2,# Warn a player
"warn":			2,# Warn a player (same as !w)
          # Text messages
"s":			2,# Switch player
"say":			2,# Send a message to everybody
"st":			2,# Same as !say, but for one team only
"sayteam":		2,# Same as !say, but for one team only (same as !st)
            
"init":			0,# Reload some settings
"swapteams":	1,# Swap the teams
"stopserver":	2,# Stops the server
"pb":			0,# Restarts punkbuster
"pbrestart":    0,# Restarts punkbuster (same as !pb)
"vote":			0,# Enable/disable voting
# Open commands # Please note that 777 is a fixed value for "open" commands!
          # This means everybody on the server can use them
"help":			777,# Show help about commands that are available to player
"admins":		777,	# Returns a list of online admins
"r":			777,	# Report a player
"report":		777,	# Report a player (same as !r)
"rules":		777,	# Shows the serverrules
"shownext":		777,	# Show the next map
"website":		777,	# Displays a link to the server website
"avote":		1,
"autovote":		1,
"anext":		1,
"arunnext":		1,
}

# This text will be sent to the player issueing !website
adm_website = "?C1001www.realitymod.ru"
# Predefined reasons, so you only have to type a keyword as a reason.  The
# script will automatically replace it with the reason you enter below.
# Note: only use lowercase in the reason "keys", you can use all cases in the
# reason itself
adm_reasons = {														
	"rules":		"Pls read the Server Rules @ realitymod.ru",
	"manual":		"Pls read Project Reality Manual",		
	"afk?": 		"Are you AFK? Type !r NO to respond",	
	"afk": 			"You were AFK!",
	"mic?":			"Have microphone?",
	"mic": 			"All players must have microphone!",
	"steal": 		"Stop Asset stealing",
	"tk": 			"Stop TeamKilling!",
	"ta":			"Stop TeamAttacking!",
	"lang": 		"Watch your language!",
	"spam":			"Stop spamming!",
	"tvd":			"Team Vehicle Damage!",
	"waste":		"Stop wasting assets!",
	"taxi":			"Don't use vehicle as taxi! Return it!",
	"talk":			"Numpad0 - talk to squad. H - local talk",
	"br":			"Stop baseraping! Stop camping near base!",
	"solo":			"NO SOLO! Return to mainbase or be punished!",
	"unlock":		"Unlock your squad. Dont lock squad before 4 members in it.",
	"113":			"You shouldn't discuss administration or its actions in game. Visit our forum and share your opinion - http://otstrel.ru/forum/",
	"wsn":			"Wrong squad name!",
	"rsteal":		"BopoBcTBo TexHuku \ KuToB!",
	"rtk":			"TuMKuJlJl !!",
	"rta":			"Hvatit strelyat po svoim!",
	"rlang":		"Mat, oskorbleniya zaprescheny!",
	"rspam":		"Stop Spam!",
	"rtvd":			"Prekrati atakovat' svoyu tehniku!",
	"rwaste":		"Hvatit slivat' tehniku! Esli ne umeete polzovatsa tehnikoy - ne ispolzuyte ee!",
	"rbr":			"Prekrati atakovat' bazu protivnika!",
	"rsolo":		"Stop Solo! Nelzya ispolzovat' tyajeluyu tehniku bez strelka!",
	"runlock":		"Otkroy skvad! Nelzya zakryvat' skvad do 4x igrokov",
	"r113":			"Zaprescheno obsujdat' deystviya administracii v igre. Dlya etogo est' forum - http://otstrel.ru/forum/",
}
adm_rulesEnabled = True
# Array in which the rules of the server will be saved.  Five rules is the max,
# the player can't see more than five lines.  Remove lines if desired
adm_rules = [
	"Communicate and Teamwork!  No AssetRule here.   No TK\TA\TVD.   No Baserape\basecamp",
	"Do not insult others.   No kit\asset stealing.   No cheat\glitches!",
	"No Mortars in Dome of Death(DOD).   No Solo at Heavy Vehicles.   Dont learn to fly here",
	"Dont lock squad before 6 members.   Use microphone and mumble.   Do not spam!",
	"Full RuleSet @ www.realitymod.ru"]
	
# All available maps.  This is NOT the maplist on your server!  Don't change
# anything!  DARN IT, don't touch it!  :p
adm_mapListAll = []
adm_mapListOld = ["albasrah|gpm_coop|inf",
    "albasrah|gpm_coop|std",
    "albasrah|gpm_insurgency|inf",
    "albasrah|gpm_insurgency|alt",
    "albasrah|gpm_insurgency|std",
    "albasrah|gpm_skirmish|inf",
    "asad_khal|gpm_coop|inf",
    "asad_khal|gpm_skirmish|inf",
    "asad_khal|gpm_cq|inf",
    "asad_khal|gpm_cq|alt",
    "asad_khal|gpm_cq|std",
    "battle_for_qinling|gpm_cnc|inf",
    "battle_for_qinling|gpm_cnc|std",
    "battle_for_qinling|gpm_coop|inf",
    "battle_for_qinling|gpm_cq|inf",
    "battle_for_qinling|gpm_cq|alt",
    "battle_for_qinling|gpm_cq|std",
    "battle_for_qinling|gpm_skirmish|inf",
    "battle_for_qinling|gpm_vehicles|std",
    "beirut|gpm_coop|std",
    "beirut|gpm_cq|inf",
    "beirut|gpm_cq|alt",
    "beirut|gpm_cq|std",
    "beirut|gpm_skirmish|inf",
    "burning_sands|gpm_cq|inf",
    "burning_sands|gpm_cq|alt",
    "burning_sands|gpm_cq|std",
    "burning_sands|gpm_skirmish|inf",
    "dragon_fly|gpm_cq|inf",
    "dragon_fly|gpm_cq|std",
    "dragon_fly|gpm_insurgency|inf",
    "dragon_fly|gpm_insurgency|std",
    "dragon_fly|gpm_skirmish|inf",
    "fallujah_west|gpm_coop|std",
    "fallujah_west|gpm_insurgency|inf",
    "fallujah_west|gpm_insurgency|std",
    "fallujah_west|gpm_skirmish|inf",
    "fools_road|gpm_coop|std",
    "fools_road|gpm_cq|inf",
    "fools_road|gpm_cq|std",
    "fools_road|gpm_skirmish|inf",
    "gaza|gpm_coop|inf",
    "gaza|gpm_coop|std",
    "gaza|gpm_cq|inf",
    "gaza|gpm_cq|std",
    "gaza|gpm_insurgency|inf",
    "gaza|gpm_insurgency|std",
    "gaza|gpm_skirmish|inf",
    "iron_eagle|gpm_cq|inf",
    "iron_eagle|gpm_cq|alt",
    "iron_eagle|gpm_cq|std",
    "iron_eagle|gpm_skirmish|inf",
    "iron_ridge|gpm_cq|inf",
    "iron_ridge|gpm_cq|std",
    "iron_ridge|gpm_insurgency|inf",
    "iron_ridge|gpm_insurgency|std",
    "iron_ridge|gpm_skirmish|inf",
    "jabal|gpm_cq|inf",
    "jabal|gpm_cq|std",
    "jabal|gpm_skirmish|inf",
    "karbala|gpm_coop|std",
    "karbala|gpm_insurgency|inf",
    "karbala|gpm_insurgency|std",
    "karbala|gpm_skirmish|inf",
    "kashan_desert|gpm_cnc|inf",
    "kashan_desert|gpm_cnc|alt",
    "kashan_desert|gpm_cnc|std",
    "kashan_desert|gpm_coop|std",
    "kashan_desert|gpm_cq|inf",
    "kashan_desert|gpm_cq|alt",
    "kashan_desert|gpm_cq|std",
    "kashan_desert|gpm_skirmish|inf",
    "kashan_desert|gpm_vehicles|std",
    "kokan|gpm_insurgency|inf",
    "kokan|gpm_insurgency|alt",
    "kokan|gpm_insurgency|std",
    "kokan|gpm_skirmish|inf",
    "kokan|gpm_skirmish|alt",
    "korengal|gpm_cq|std",
    "korengal|gpm_insurgency|inf",
    "korengal|gpm_insurgency|std",
    "korengal|gpm_skirmish|inf",
    "kozelsk|gpm_coop|inf",
    "kozelsk|gpm_cq|inf",
    "kozelsk|gpm_cq|alt",
    "kozelsk|gpm_cq|std",
    "kozelsk|gpm_skirmish|inf",
    "lashkar_valley|gpm_coop|inf",
    "lashkar_valley|gpm_insurgency|inf",
    "lashkar_valley|gpm_insurgency|std",
    "lashkar_valley|gpm_skirmish|inf",
    "muttrah_city_2|gpm_coop|alt",
    "muttrah_city_2|gpm_coop|std",
    "muttrah_city_2|gpm_cq|inf",
    "muttrah_city_2|gpm_cq|std",
    "muttrah_city_2|gpm_skirmish|inf",
    "operation_archer|gpm_coop|inf",
    "operation_archer|gpm_coop|std",
    "operation_archer|gpm_insurgency|inf",
    "operation_archer|gpm_insurgency|alt",
    "operation_archer|gpm_insurgency|std",
    "operation_archer|gpm_skirmish|inf",
    "op_barracuda|gpm_coop|std",
    "op_barracuda|gpm_cq|inf",
    "op_barracuda|gpm_cq|std",
    "op_barracuda|gpm_skirmish|inf",
    "qwai1|gpm_coop|std",
    "qwai1|gpm_cq|inf",
    "qwai1|gpm_cq|std",
    "qwai1|gpm_skirmish|inf",
    "ramiel|gpm_coop|inf",
    "ramiel|gpm_coop|std",
    "ramiel|gpm_insurgency|inf",
    "ramiel|gpm_insurgency|alt",
    "ramiel|gpm_insurgency|std",
    "ramiel|gpm_skirmish|inf",
    "shijiavalley|gpm_cnc|std",
    "shijiavalley|gpm_cq|alt",
    "shijiavalley|gpm_cq|std",
    "shijiavalley|gpm_skirmish|inf",
    "siege_at_ochamchira|gpm_cq|inf",
    "siege_at_ochamchira|gpm_cq|alt",
    "siege_at_ochamchira|gpm_skirmish|inf",
    "silent_eagle|gpm_cnc|inf",
    "silent_eagle|gpm_cnc|std",
    "silent_eagle|gpm_cq|inf",
    "silent_eagle|gpm_cq|alt",
    "silent_eagle|gpm_cq|std",
    "silent_eagle|gpm_skirmish|inf",
    "silent_eagle|gpm_vehicles|std",
    "yamalia|gpm_cnc|inf",
    "yamalia|gpm_cnc|std",
    "yamalia|gpm_cq|inf",
    "yamalia|gpm_cq|alt",
    "yamalia|gpm_cq|std",
    "yamalia|gpm_skirmish|inf",
    "yamalia|gpm_vehicles|std",
    "assault_on_mestia|gpm_cq|inf",
    "assault_on_mestia|gpm_cq|std",
    "assault_on_mestia|gpm_skirmish|inf",
    "black_gold|gpm_cq|inf",
    "black_gold|gpm_cq|alt",
    "black_gold|gpm_cq|std",
    "black_gold|gpm_cq|lrg",
    "black_gold|gpm_skirmish|inf",
    "black_gold|gpm_cnc|inf",
    "black_gold|gpm_cnc|alt",
    "black_gold|gpm_cnc|std",
    "black_gold|gpm_cnc|lrg",
    "black_gold|gpm_vehicles|alt",
    "black_gold|gpm_vehicles|std",
    "operation_ghost_train|gpm_cq|inf",
    "operation_ghost_train|gpm_cq|std",
    "operation_ghost_train|gpm_skirmish|inf",
    "operation_marlin|gpm_cq|inf",
    "operation_marlin|gpm_cq|std",
    "operation_marlin|gpm_skirmish|inf",
    "operation_marlin|gpm_insurgency|std",
    "pavlovsk_bay|gpm_cq|inf",
    "pavlovsk_bay|gpm_cq|alt",
    "pavlovsk_bay|gpm_cq|std",
    "pavlovsk_bay|gpm_cq|lrg",
    "pavlovsk_bay|gpm_skirmish|inf",
    "tad_sae|gpm_cq|inf",
    "vadso_city|gpm_cq|inf",
    "vadso_city|gpm_cq|alt",
    "vadso_city|gpm_cq|std",
    "vadso_city|gpm_cq|lrg",
    "vadso_city|gpm_skirmish|inf"]