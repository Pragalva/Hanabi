from Card import Card
from Card import Color
from typing import List

#Definiton of out agent
#Our Agent will have a hand which we will use to generate what the other players can see
class Agent:
    def __init__(self, player_name: str, player_index: int):
        self.name: str = player_name
        self.player_index: int = player_index
        self.card_in_hand: Card = [] #The deck of the player
        self.cards_visible: Card = [] #The visible card of other players
        self.hint_color: int = [0,0,0,0,0]
        self.hint_number: int = [0,0,0,0,0]
    
    ################################################################
    #get functions
    def get_cards_in_hand(self):
        return self.card_in_hand # Return the hand of the player
    
    def get_visible_cards(self):
        return self.cards_visible #Returns the visible hand of the agent
    #######################################################################

    #########################################################################
    #Set funtions
    def set_visible_cards(self, agent1: "Agent", agent2: "Agent") -> None:
        #Updates the agent's cards_visible with the hands of two other agents.
        self.cards_visible = agent1.card_in_hand + agent2.card_in_hand  # Combine hands
    ############################################################################

    ###############################################################################
    #Actions
    def draw_card(self, deck = List[Card]):
        if(deck and (len(self.card_in_hand)<= 5)): # Check if the agent can draw the card
            new_card = deck.pop(0)  # Remove the first card from the deck
            self.card_in_hand.append(new_card)  # Add it to the player's hand
    
    def discard_card(self, deck = List[Card],discard =List[Card], discard_index =int ):
        discard_card = self.card_in_hand.pop(discard_index) #Remove the discard card from the hand
        self.hint_number.pop(discard_index) #Discard the hint assosicated with the card
        self.hint_color.pop(discard_index)
        discard.append(discard_card) #add the discard card to the discard pile
        self.draw_card(deck) #draw a new card
    ###################################################################################


        
    
