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

colors = {"white": "00",
          "black": "01",
          "dark_blue": "02",
          "green": "03",
          "red": "04",
          "dark_red": "05",
          "dark_violet": "06",
          "orange": "07",
          "yellow": "08",
          "light_green": "09",
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
        output = codes['color']+colorstring+text+codes['color']
    else:
        output = codes['color']+colors[fgcolor]+text+codes['color']
    logging.debug("Returning colorized "+text+" as "+output)
    return output

logging.debug("8 green is "+str(color("8", "green")))

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
        logging.debug("Creating die #"+str(self.number)+" with faces ="
                      +str(faces))
        #result is a list, to allow for standard coding and chains for WW die
        self.results = []
        self.strversion = {}
        if faces in fate_synonyms:
            logging.debug("Fugde die")
            self.faces = "f"
            self.facelist = [-1, 0, 1]
            self.strversion = {-1: style(color(u"\u2212", "red"  ), "bold"), 
                                0: color("0", "dark_grey" ), 
                                1: style(color("+", "green"), "bold")}

            self.values = {-1: -1,
                            0:  0,
                            1:  1}
        elif faces in wod_synonyms:
            logging.debug("White wolf die")
            self.faces = "w"
            self.facelist = range(1,11)
            self.successes = 0
            self.strversion = {1: "1",
                               2: "2",
                               3: "3",
                               4: "4",
                               5: "5",
                               6: "6",
                               7: "7",
                               8:  style(color("8",  "green"), "bold"),
                               9:  style(color("9",  "green"), "bold"),
                               10: style(color("10", "green"), "bold")}
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
            logging.debug("Normal die")
            self.facelist = range(1,int(faces)+1)
            self.strversion = {x: str(x) for x in range (1, int(faces)+1)}
            self.values = {x: x for x in range (1, int(faces)+1)}

        for key in self.strversion:
            logging.debug(str(key)+"Assigned to:")
            logging.debug(self.strversion[key])

    def __str__(self):
        return "d"+faces+": [ "+", ".join(self.history)+" ]"

    def roll(self):
        result = random.choice(self.facelist)
        result_arr = [result]
        if self.faces == "w" and result in [10]:
            result_arr+=self.roll()
        self.results = result_arr
        logging.debug("result = "+str(result_arr))
        return result_arr

    @property
    def total(self):
        return sum(self.values[result] for result in self.results)


    @property
    def result_string(self):
        return style("!", "bold").join(self.strversion[result] for result in self.results)

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
            die = ', '.join(die.result_string for die in self.dice)
            total = "Total: "+style(str(self.total), "bold") 
            return " ".join([die, total])
        else:
            return "Unrolled"

@willie.module.rule(r'(.+\s)?((\d+)d(\d+|[FfWw])((\+|-)(\d+))?)(\s.+)?')
def nada(bot, trigger):
    logging.debug("Triggered on "+trigger)
    match = re.search(r'(.+\s)?((\d+)d(\d+|[FfWw])((\+|-)(\d+))?)(\s.+)?', trigger)
    
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
