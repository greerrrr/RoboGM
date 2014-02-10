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

@willie.module.rule(r'(.+\s)?((\d+)d(\d+|F)((\+|-)(\d+))?)(\s.+)?')
def nada(bot, trigger):
    match = re.search(r'(.+\s)?((\d+)d(\d+|F)((\+|-)(\d+))?)(\s.+)?', trigger)
    
    #for index in range(9):
    #    if match.group(index) is None:
    #      bot.say("Index "+str(index)+" is empty.")
    #    else:
    #      bot.say("Index "+str(index)+":"+match.group(index))
    whole     = match.group(0)
    prefix    = match.group(1)
    diceexpr  = match.group(2)
    quantity  = match.group(3)
    diesize   = match.group(4)
    mod       = match.group(5)
    sign      = match.group(6)
    magnitude = match.group(7)
    suffix    = match.group(8)

    rolls = roll(quantity, diesize, mod)
    rollsstr = ','.join(map(str, rolls))
    bot.say(rollsstr)
    if not mod is None:
      total = sum(rolls)+int(mod)
    else:
      total = sum(rolls)
      bot.say("Total is \x035,12" + str(total)+"\x03")
