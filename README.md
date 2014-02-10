#RoboGM
A series of modules for willie (willie.dftba.net) to ease the use of IRC for RPGs

##Modules
###nicedice
* rolls NdM+K, support Fate die

Currently refactoring to support:
* Support Fate and White Wolf die (exploding)
* Colored output
* totals, including success counts for White Wolf

###rolltables
Create and edit tables to generate random results from. Saves to a JSON file
Planned:
* Weighted tables
* class based structuring
Horizon:
* interface overhaul
* bulk loading
* linked tables

###sockpuppet
PM RoboGM with ```.puppet-channel``` to set an output channel, then all text of the form ```>Message for channel``` to RoboGM will be sent through it.

###ircformat
Not a willie module, just functions for adding styles and colors to text for irc

###Upcoming modules
* npcgenerator: Generate simple filler npcs, physical description, quirks
* charsheet: Dictionary associated with a character name. Characters will have "owners", associated nicks.
