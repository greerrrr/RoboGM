import willie, random, json, logging
from os.path import expanduser

"""
rolltable.py - table rolling code for willie
by spr-k3737
All use of this code is unlicensed
http://willie.dftba.net
"""
home = expanduser("~")+"/"

logging.basicConfig(level=logging.DEBUG)

tables = {}

def save():
    try:
        with open(home+".willie/tables.json", "w+") as tablesfile:
            json.dump(tables, tablesfile)
    except IOError:
        logging.exception("Error writing tables file")

def load():
    global tables
    try:
        with open(home+".willie/tables.json", "r") as tablesfile:
            tables = json.load(tablesfile)
    except IOError:
        logging.exception("No tables file found, creating now")
        save()
    except AttributeError:
        logging.exception("Well fuck...")

load()

@willie.module.commands('tablehelp')
def tablehelp(bot, trigger):
    bot.say('Using rolltable.py for willie:')
    bot.say('.addtable tablename')
    bot.say('.addentry tablename: the text of your entry')
    bot.say('.rolltable tablename')
    bot.say('.printtable tablename')
    bot.say('.listtables')

@willie.module.commands('listtables')
def listtables(bot, trigger):
    for key in tables:
	#output the title of each table and the number of entries
        bot.say(key+': '+str(len(tables[key]))+' entries')

@willie.module.commands('printtable')
def printtable(bot, trigger):
    bot.say("Table "+trigger.group(2)+" contains:")
    index = 0
    for entry in tables[trigger.group(2)]:
        bot.say(str(index)+": "+entry)
        index = index+1

@willie.module.commands('addtable')
def addtable(bot, trigger):
    tables[trigger.group(2)] = []
    bot.say('Added new table: "'+trigger.group(2)+'"')
    save()

@willie.module.commands('addentry')
def addentry(bot, trigger):
    tablename = trigger.group(2).partition(": ")[0]
    entry     = trigger.group(2).partition(": ")[2]
    tables[tablename].append(entry)
    bot.say('Added "'+entry+'" to table "'+tablename+'"')
    save()

@willie.module.commands('rolltable')
def rolltable(bot, trigger):
    bot.say(random.choice(tables[trigger.group(2)]))

@willie.module.commands('reloadtables')
def reloadtables(bot, trigger):
    load()
    bot.say("Reloaded tables")
