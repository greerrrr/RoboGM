"""
nicedice.py - a custom dice module
by spr-k3737
Any use of this code is unlicensed
http://willie.dftba.net
"""
import willie, re, random, logging

logging.basicConfig(level=logging.DEBUG)

def roll(quantity, diesize, mod):
    rolls = []
    if diesize == "F":
        for die in range(int(quantity)):
		rolls.append(random.randint(-1, 1))
    else:
        for die in range(int(quantity)):
            rolls.append(random.randint(1, int(diesize)))
    return rolls

@willie.module.rule(r'\>(.*)')
def say(bot, trigger):
    bot.msg(bot.memory['puppet_channel'], trigger.group(1))

@willie.module.commands('puppet-channel')
def setchannel(bot, trigger):
    bot.memory['puppet_channel'] = trigger.group(2)
    bot.say("Outputting puppet text to "+bot.memory['puppet_channel'])
