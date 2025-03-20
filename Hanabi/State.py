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
        self.Counter_Last_Round = 3

        #Player Hands
        self.Player_1_card_in_hand: Card = []
        self.Player_2_card_in_hand: Card = []
        self.Player_3_card_in_hand: Card = []

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

    def starting_hand(self,deck = List[Card]):
        for x in 5:
            new_card1 =deck.pop(0)
            self.Player_1_card_in_hand.appened(new_card1)

            new_card2 =deck.pop(0)
            self.Player_2_card_in_hand.appened(new_card2)

            new_card3 =deck.pop(0)
            self.Player_3_card_in_hand.appened(new_card3)

    def termination_test(self):
        terminate = False
        if (len(self.Game_Deck == 0)):
            Counter_Last_Round = Counter_Last_Round - 1
        if len(self.Board_pile == 25) | (self.Fuse_Token == 0) | (Counter_Last_Round == 0):
            terminate = True

        return terminate
