
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
"db8e98d81cb04e924dcea1583f1ea9de":     0,  # makeich74 , SuperAdmin
"54d157c81c111b406881f77357a84586":     1,  # zloyrash , InGameAdmin
"4d21e04f81dd115f1f0e4870af7badc9":     1,  # Unmanned / Sober, InGameAdmin
"223fa84be2eccedbfd101cf15dab06b1":     1,  # PReferens, InGameAdmin
"871df9189175c0d5d60d0104ad6b8b29":     1,  # Bishop.A , InGameAdmin
"34d74d956c369167d3b2742929061dc4":     1,  # Shmayser , InGameAdmin
"3e9f1995c87226eaf0a53e107db6c98c":     1,  # Spak , InGameAdmin
"9a0beaece76d3d9753f16467c0c84e92":     1,  # Kittenko , InGameAdmin
"729b510f2648b65c5c6f32fe7480df40":     1,  # roofer_nsk , InGameAdmin
"5673518431ed276414981e9310f53a8a":     2,  # Andryhgan , assistant
"fa22b834eab5805770911af2041e2bde":     2,  # FIDE1iTY , assistant
"1b41cba38a417fdb1244199d858735c1":     2,  # KIA Raubti3r , assistant
"6e11a1aeaf87cbcfaa76cbae75df167a":     2,  # LorD ChuPA , assistant
"3ba03aa47c69c56e1b66b6ab91839b3d":     2,  # DremuchiiLOX2 , assistant
"b697bc044a6a00ea692ff21377b189bd":     2,  # D}ll{EM , assistant
"8235f7aa7e43a7b7c7fb24100a5fad3a":     2,  # _Reality_r , assistant
"fd2e92ed2f615c62cdae0b1032563b91":     2,  # PEGAS75 , assistant
"02d85dd8eed65142778d11003e28d03f":     2,  # wAn7eD.md , assistant
"b35ce044cdfae2a58afce10a897cba62":		2,  # USSR* BUTCH1dfgdr	, assistant
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
"restart":		0,# Restart the round
"runnext":		0,# -Run the next map
"save":			0,# Save the maplist
"maplist":		2,# Shows the maplist to user
"setnext":		0,# -Set a next map
"mvote":		0,# -Initializes a server mapvote between 2-3 maps.  People can then vote
            # with either writing 1,2 or 3 in chat.  All admins will receive a
                        # message
                                    # which map won after a configured time.
"mapvote":		0,# -same as mvote
              # Player control
"b":			1,# Ban a player
"ban":			1,# Ban a player (same as !b)
"ab":			1,# Ban a player
"aban":			1,# Ban a player (same as !ab)
"banlist":		1,
"ub":			1,# Unbans the player
"unban":		1,# same as !ub
"fly":			0,# Send a player up in the air
"hash":			2,# Retrieves the hash of certain player
"k":			1,# Kick a player
"kick":			1,# Kick a player (same as !k)
"kill":			1,# Kill a player
"resign":		1,# Resign a player from being squad leader or commander
"ss":			2,# Take a screenshot of a player (through punkbuster)
"switch":		2,# Teamswitch a player
"tb":			1,# Temporary ban a player (basically extended 'kick')
"w":			1,# Warn a player
"warn":			1,# Warn a player (same as !w)
          # Text messages
"s":			2,# Switch player
"say":			2,# Send a message to everybody
"st":			1,# Same as !say, but for one team only
"sayteam":		1,# Same as !say, but for one team only (same as !st)
            
"init":			0,# Reload some settings
"swapteams":	0,# Swap the teams
"stopserver":	2,# Stops the server
"pb":			0,# Restarts punkbuster
"pbrestart":    0,# Restarts punkbuster (same as !pb)
"vote":			2,# Enable/disable voting
# Open commands # Please note that 777 is a fixed value for "open" commands!
          # This means everybody on the server can use them
"help":			777,# Show help about commands that are available to player
"admins":		777,	# Returns a list of online admins
"r":			777,	# Report a player
"report":		777,	# Report a player (same as !r)
"rules":		777,	# Shows the serverrules
"shownext":		777,	# Show the next map
"website":		777,	# Displays a link to the server website
"avote":		0,
"autovote":		0,
"anext":		0,
"arunnext":		0,
}

# This text will be sent to the player issueing !website
adm_website = "?C1001http://otstrel.ru/forum/#forum296"
# Predefined reasons, so you only have to type a keyword as a reason.  The
# script will automatically replace it with the reason you enter below.
# Note: only use lowercase in the reason "keys", you can use all cases in the
# reason itself
adm_reasons = {														
	"afk": 			"You were AFK!",
	"dis": 			"You're bringing the game into disrepute. Be gone, foul demon!",
	"fail": 		"You are a failure",
	"steal": 		"Asset stealing",
	"tk": 			"Stop teamkilling!",
	"lang": 		"Watch your language!",
}
adm_rulesEnabled = True
# Array in which the rules of the server will be saved.  Five rules is the max,
# the player can't see more than five lines.  Remove lines if desired
adm_rules = [
	"Fair play is the Rule here! No kit,asset stealing! No cheat and glitches!",
	"Do not insult others. No Team Killing(TK),No Team Attack(TA),No Team Vehicle Damage (TVD).",
	"No BaseRape.No Mortars in Dome of Death(DOD). No Solo at Heavy Vehicles.",
	"No locked squads with less 5 members."]
	
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