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
Speak through RoboGM to a channel
####Usage
* ```.puppet-channel #channel``` output messages to #channel
* ```>Message``` Say Message in #channel

###deck
Create, name, and draw from decks of cards. Simulates a depleting deck.
* Normal playing cards
* Major Arcana
* Remembers last used deck

####Usage
* .newdeck deck_type [deck_name]
* .draw [deck_name]

Implementing:
* shuffle
* shuffle drawn cards back into deck
* reversed/unreversed tarot cards

###Upcoming modules
* npcgenerator: Generate simple filler npcs, physical description, quirks
* charsheet: Dictionary associated with a character name. Characters will have "owners", associated nicks.
