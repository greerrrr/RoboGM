"""
diebot.py - a custom dice module
by spr-k3737
Any use of this code is unlicensed
http://willie.dftba.net
"""
import willie, re, random, logging, nicedice

logging.basicConfig(level=logging.DEBUG)

@willie.module.rule(r'(.+\s)?((\d+)d(\d+|F)((\+|-)(\d+))?)(\s.+)?')
def nada(bot, trigger):
    match = re.search(r'(.+\s)?((\d+)d(\d+|F)((\+|-)(\d+))?)(\s.+)?', trigger)
    
    whole     = match.group(0)
    prefix    = match.group(1)
    diceexpr  = match.group(2)
    quantity  = match.group(3)
    diesize   = match.group(4)
    mod       = match.group(5)
    sign      = match.group(6)
    magnitude = match.group(7)
    suffix    = match.group(8)

    r = nicedice.RollGroup(diceexpr)
    r.roll()
    bot.say(r.result_string)
