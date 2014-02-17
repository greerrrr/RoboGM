#RoboGM
A series of modules for willie (willie.dftba.net) to ease the use of IRC for RPGs

##Modules
###nicedice
* rolls NdM+K, support Fate and White Wolf die (exploding d10s)
* colorized output
* total/success counting
* Fate ladder

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

###deck
Create, name, and draw from decks of cards. Simulates a depleting deck.
* Normal playing cards
* Major Arcana

Implementing:
* shuffle
* shuffle drawn cards back into deck
* reversed/unreversed tarot cards

###Upcoming modules
* npcgenerator: Generate simple filler npcs, physical description, quirks
* charsheet: Dictionary associated with a character name. Characters will have "owners", associated nicks.
