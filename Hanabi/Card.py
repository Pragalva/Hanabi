#Files that defines class card
import random
from enum import Enum
from typing import List
#Setting int values to colours
class Color(Enum):
    NO_COLOR = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    WHITE = 5

#Card has two attributes number and color
class Card:
    def __init__(self, number: int, color: Color):
        self._number: int = number
        self._color: Color = color

        self.number_hint: int = 0
        self.color_hint: int = 0

    def __repr__(self):
        return f"Card({self._number}, {self._color.name})"
    def get_number(self):
        return self._number
    def get_color(self):
        return self._color
    
    def get_color_hint(self):
        return self.color_hint
    def get_number_hint(self):
        return self.number_hint

    
    def set_color_hint(self, hint):
        self.color_hint = hint
    
    def set_number_hint(self, hint):
        self.number_hint = hint
    #Creation of Deck for the game
    #Create a blanks list of card, adds card for each color and number in the game. Then randomizes the array and returns a array
    def generate_deck()-> List["Card"]:
        deck: List[Card]= []
        #Defining the number of cards that we will have for our game
        Cards_in_game = [1,1,1,2,2,3,3,4,4,5]
        #Loop for creation
        for color in list(Color)[1:]:
            for i in Cards_in_game:
                card = Card(i,color)
                deck.append(card)
        #Randomize the list created and return the deck
        random.shuffle(deck)
        return deck
    #Create a blank special deck for playing cards
    def generate_play_pile()-> List["Card"]:
        play_pile: List[Card] = []
        #Create a Card with zero color
        for color in Color:
            card = Card(0,color)
            play_pile.append(card)
        
        #Return the play pile
        return play_pile
