from Card import Card
from Card import Color
from typing import List
from State_Andrea import State
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
        self.hint_color_pending: int = [0,0,0,0,0] #To track what hints are pending this turn
        self.hint_number_pending: int = [0,0,0,0,0] #To track what hints are pending this turn
        self.discard_prio: int = [0,0,0,0,0] #added
    
    ################################################################
    #get functions
    def get_cards_in_hand(self):
        return self.card_in_hand # Return the hand of the player
    
    def get_visible_cards(self, current_state: "State"):
        temp_hands = current_state.hands
        temp_hands.pop[self.player_index]
        return temp_hands #Returns the visible hand of the agent
    #######################################################################
    #########################################################################
    #Set funtions
    ''';def set_visible_cards(self, agent1: "Agent", agent2: "Agent") -> None:
        #Updates the agent's cards_visible with the hands of two other agents.
        self.cards_visible = agent1.card_in_hand + agent2.card_in_hand  # Combine hands
    def set_color_hint(self,hint_index: int, hint: int):
        #Updates the agent's pending color hint list
        self.hint_color_pending[hint_index] = hint
        card_for_hint = self.card_in_hand[hint_index]
        card_for_hint.set_color_hint(hint)
    
    def set_number_hint(self,hint_index: int, hint: int):
        #Updates the agent's pending number hint list
        self.hint_number_pending[hint_index] = hint
        card_for_hint = self.card_in_hand[hint_index]
        card_for_hint.set_number_hint(hint)'''
    ############################################################################

    ###############################################################################
    #Actions
    #Function to draw a card
    def draw_card(self, current_state: "State"):
        if(current_state.Game_Deck != 0 and (len(current_state.hands[self.player_index])<= 5)): # Check if the agent can draw the card
            new_card = current_state.Game_Deck.pop(0)  # Remove the first card from the deck
            current_state.hands[self.player_index].append(new_card)

            '''self.card_in_hand.append(new_card)  # Add it to the player's hand
            self.hint_color.append(0) #Add a blank hint for new card
            self.hint_number.append(0) #Add a blank hint for new card'''
    
    #Function to discard card
    def discard_card(self, current_state: "State", discard_index =int ):
        discard_card = current_state.hands[self.player_index].pop(discard_index) #Remove the discard card from the hand
        '''self.hint_number.pop(discard_index) #Discard the hint assosicated with the card
        self.hint_color.pop(discard_index)'''

        current_state.Discard_pile.append(discard_card) #add the discard card to the discard pile
        self.draw_card(current_state.Game_Deck) #draw a new card
        if(current_state.Total_hints <=8):
            current_state.Total_hints = current_state.Total_hints +1 #adds the token to the

    #Function to play a card
    def play_card(self, current_state: "State", play_index =int):
        Card_play = current_state.hands[self.player_index].pop(play_index) #Remove the play card from hand

        '''self.hint_number.pop(play_index) #Discard the hint assosicated with the card
        self.hint_color.pop(play_index)'''
        for i in current_state.Play_pile:
            if i.get_color() == Card_play.get_color() : #Loop through to find the right color
                if (i.get_number()+1) == Card_play.get_number(): #Check if the card if playable
                    i.number = Card_play.get_number() #Change the number to the current playable card.
                    current_state.Board_pile.append(i)#Add the card to list of cards played
                else:
                    current_state.Fuse_Token = current_state.Fuse_Token -1 #Lose a life for losing a life
                    print(f"Oh no!!, you lost a life.")
                    current_state.Discard_pile.append(Card_play) #Add the card to the discard pile
        
        self.draw_card(current_state)#Draw a card form the deck

    #Function to give hint
    def give_hint(self, current_state: "State", hint_type = int, hint_index = int, hint = int, player_hint_index = int):
        if(current_state.Total_hints > 0 ): #Check if you have hints left
            #For color hint
            if hint_type == 0:
                #Agent.set_color_hint(hint_index,hint) #Call the set funtion to give color hint
                current_state.hands[player_hint_index][hint_index].set_color_hint(hint)

            #For number hint
            elif hint_type == 1:
                #Agent.set_number_hint(hint_index,hint) #Call the set function to give number hint
                current_state.hands[player_hint_index][hint_index].set_number_hint(hint)
            
            current_state.Total_hints = current_state.Total_hints -1 #Decrease the hint total
        else:
            print("Sorry you have no hints left")
    ###################################################################################
