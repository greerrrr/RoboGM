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

tarot_deck = ["The Fool - 0", "The Magician - I", "The High Priestess - II",
              "The Empress - III", "The Emperor - IV", "The Hierophant - V",
              "The Lovers - VI", "The Chariot - VII", "Strength - VIII",
              "The Hermit - IX", "The Wheel of Fortune - X", "Justice - XI",
              "The Hanged Man - XII", "Death - XIII", "Temperance - XIV",
              "The Devil - XV", "The Tower - XVI", "The Star - XVI",
              "The Moon - XVIII", "The Sun- XIX", "Judgment - XX",
              "The World - XXI"]

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

heart   = color(u"\u2660", "red")
spade   = u"\u2665"
diamond = color(u"\u2666", "red")
spade   = u"\u2663"
suits = [heart, spade, diamond, spade]
unsuited_cards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
                  "Queen", "King", "Ace"]
normal_deck = []
for suit in suits:
    for card in unsuited_cards:
        normal_deck.append(card+" of "+suit)

decks = {"tarot": tarot_deck,
         "normal": normal_deck}
class Card:
    def __init__(self, value, deck_type, orientation="Unreversed"):
        self.value = value
        self.orientation = orientation
        self.deck_type = deck_type

    def flip(self):
        if self.orientation == "Unreversed":
            self.orientation = "Reversed"
        if self.orientation == "Reversed":
            self.orientation = "Unreversed"

    def shuffle(self):
        self.orientation = random.choice(["Reversed", "Unreversed"])

    @property
    def value(self):
        if self.deck_type == "tarot" and self.orientation == "Reversed":
            string = "Reversed" + self.value
            return string
        else:
            return self.value


class Deck:
    def __init__(self, deck_type, name):
        self.deck_type = deck_type.lower()
        self.deck = []
        self.drawn = []
        self.name = name
        logging.debug("Created new deck of type "+self.deck_type)
        for card_value in decks[deck_type]:
            self.deck.append(Card(card_value, self.deck_type))

    def shuffle(self):
        logging.debug("Shuffling deck")
        for card in self.deck:
            card.shuffle()
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) == 0:
            return -1
        else:
            drawn_card = self.deck.pop()
            self.drawn.append(drawn_card)
            return drawn_card

    def collect_drawn(self):
        self.deck = self.deck + self.drawn
        self.drawn = []


@willie.module.commands('newdeck')
def newdeck(bot, trigger):
    logging.debug("Triggered on "+trigger)
    deck_type = trigger.group(2).partition(" ")[0]
    deck_name = trigger.group(2).partition(" ")[2] 
    if deck_name == None:
        deck_name = "unnamed"
    logging.debug("Creating deck"+deck_name+" of type "+deck_type)
    new_deck = Deck(deck_type, deck_name)
    bot.memory['decks'] = {}
    bot.memory['decks'][deck_name] = new_deck
    bot.memory['lastdeck'] = deck_name

@willie.module.commands('draw')
def drawcard(bot, trigger):
    if trigger.group(2) == None:
        deck_name = bot.memory['lastdeck']
    else:
        deck_name = trigger.group(2)
        bot.memory['lastdeck'] = deck_name
    logging.debug("Drawing card from deck "+deck_name)
    bot.say(bot.memory['decks'][deck_name].draw().value)
