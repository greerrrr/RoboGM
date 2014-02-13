"""
nicedice.py - a custom dice module
by spr-k3737
Any use of this code is unlicensed
http://willie.dftba.net
"""
import willie, random, re, logging

logging.basicConfig(level=logging.DEBUG)
codes = {"bold": "\x02",
         "color": "\x03",
         "italic": "\x09",
         "strikethrough": "\x13",
         "reset": "\x0f",
         "underline": "\x15",
         "underline2": "\x1f",
         "reverse": "\x16"}

colors = {"white": "0",
          "black": "1",
          "dark_blue": "2",
          "green": "3",
          "red": "4",
          "dark_red": "5",
          "dark_violet": "6",
          "orange": "7",
          "yellow": "8",
          "light_green": "9",
          "cyan": "10",
          "light_cyan": "11",
          "blue": "12",
          "violet": "13",
          "dark_grey": "14",
          "light_grey": "15"}

fate_synonyms = ['F',"f","fate","fudge","Fate", "FATE", "Fudge"]
wod_synonyms = ["W", "w", "WW", "ww", "wod", "WoD"] 

def style(text, style):
	return codes[style]+text+codes[style]

def color(text, fgcolor, bgcolor=None):
	if fgcolor in colors and bgcolor in colors:
		colorstring = colors[fgcolor]+","+colors[bgcolor]
		return codes['color']+colorstring+text+codes['color']
	else:
		return codes['color']+colors[fgcolor]+text+codes['color']

def parse_roll(roll_expr):
        dienames = '|'.join(fate_synonyms+wod_synonyms)
        dice_regex = r'(\d+)d(\d+|[FfWw])'
        mod_regex = r'(\+|-)(\d+)'
        optional_mod = '('+mod_regex+')?'
        match = re.search(dice_regex+optional_mod, roll_expr)
        for index in range(5):
            if match.group(index) is None:
              print("Index "+str(index)+" is empty.")
            else:
              print("Index "+str(index)+":"+match.group(index))
        
        parsedroll = {'quantity': int(match.group(1)),
                      'faces': match.group(2),
                      'signedmod': match.group(3)}
        return parsedroll


class Die:
    def __init__(self, faces, number):
        self.faces = faces
        self.number = number
        logging.debug("faces = "+faces)
        #result is a list, to allow for standard coding and chains for WW die
        self.results = []
        if faces in fate_synonyms:
            logging.debug("recognized F")
            self.faces = "f"
            self.facelist = [-1, 0, 1]
            self.strversion = {-1: color(u"\u2212", "red"  ), 
                                0: color("0", "dark_grey" ), 
                                1: color("+", "green")}

            self.values = {-1: -1,
                            0:  0,
                            1:  1}
        elif faces in wod_synonyms:
            self.faces = "w"
            self.facelist = range(1,11)
            self.successes = 0
            self.strversion = {1 : "1",
                               2 : "2",
                               3 : "3",
                               4 : "4",
                               5 : "5",
                               6 : "6",
                               7 : "7",
                               8 : color("8" , "green" ),
                               9 : color("9" , "green" ),
                               10: color("10", "orange")}
            self.values = {1 : 0,
                           2 : 0,
                           3 : 0,
                           4 : 0,
                           5 : 0,
                           6 : 0,
                           7 : 0,
                           8 : 1,
                           9 : 1,
                           10: 1}
        else:
            self.facelist = range(1,int(faces)+1)
            self.strversion = {x: str(x) for x in range (1, int(faces)+1)}
            self.values = {x: x for x in range (1, int(faces)+1)}

    def __str__(self):
        return "d"+faces+": [ "+", ".join(self.history)+" ]"

    def roll(self):
        result = random.choice(self.facelist)
        result_arr = [result]
        if self.faces == "w" and result in [8, 9, 10]:
            result_arr+=self.roll()
        self.results = result_arr
        logging.debug("result = "+str(result_arr))
        return result_arr

    @property
    def total(self):
        return sum(self.values[result] for result in self.results)


    @property
    def result_string(self):
        return "!".join(self.strversion[result] for result in self.results)

class RollGroup:
    def __init__(self, rollexpression):
        parsed = parse_roll(rollexpression)
        quantity = parsed['quantity']
        faces = parsed['faces']
        self.modifier = parsed['signedmod']
        if self.modifier is None:
            self.modifier = 0
        self.dice = []
        self.rolled = False
        for die in range(1,quantity+1):
            self.dice.append(Die(faces, die))

    def roll(self):
        for die in self.dice:
            logging.debug("Rolling die #"+str(die.number))
            die.roll()
        self.rolled = True

    @property
    def total(self):
        return sum(die.total for die in self.dice)+int(self.modifier)

    @property
    def result_string(self):
        if self.rolled:
            die = ', '.join(str(die.result_string) for die in self.dice)
            total = "Total: "+style(str(self.total), "bold") 
            return die+total
        else:
            return "Unrolled"



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

    r = RollGroup(diceexpr)
    r.roll()
    bot.say(r.result_string)
