import random
from Card import Color
from Card import Card
from typing import List
class State:
    def _init_(self):
        self.Game_Deck = [] #Game deck
        self.Discard_pile = [] #List of discarded cards
        self.Play_pile = [] #List of next playable cards
        self.Board_pile = [] #List of played cards
        self.Total_hints = 8
        self.Fuse_Token = 3

    #Creation of Deck for the game
    #Create a blanks list of card, adds card for each color and number in the game. Then randomizes the array and returns a array
    def generate_deck(self):
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
        self.Game_Deck = deck
           
    #Create a blank special deck for playing cards
    def generate_play_pile(self):
        play_pile: List[Card] = []
        #Create a Card with zero color
        for color in Color:
            card = Card(0,color)
            play_pile.append(card)
        
        #Return the play pile
        self.Play_pile = play_pile
