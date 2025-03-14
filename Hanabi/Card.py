#Files that defines class card

import random
from enum import Enum
from typing import List

#Setting int values to colours
class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    WHITE = 5

#Defintion of Class card
#Card has two attributes number and color
class Card:
    def __init__(self, number: int, color: Color):
        self._number: int = number
        self._color: Color = color

    def __repr__(self):
        return f"Card({self._number}, {self._color.name})"

    def get_number(self):
        return self._number

    def get_color(self):
        return self._color

    #Creation of Deck for the game
    #Create a blanks list of card, adds card for each color and number in the game. Then randomizes the array and returns a array
    def generate_deck()-> List["Card"]:
        deck: List[Card]= []

        #Defining the number of cards that we will have for our game
        Cards_in_game = [1,1,1,2,2,3,3,4,4,5]

        #Loop for creation
        for color in Color:
            for i in Cards_in_game:
                card = Card(i,color)
                deck.append(card)

        #Randomize the list created and return the deck
        random.shuffle(deck)
        return deck

