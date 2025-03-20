from Agent import Agent
from State_Andrea import State
from Card import Color
import numpy as np

def probability_matrix (player:"Agent", state:"State", hint_type, hint_index):

    cards_seen = player.get_visible_card(state) + state.Discard_pile + state.Board_pile
    cards_left = 50 - len(cards_seen) 
    
    cards_of_a_color = 10
    
    cards_in_game = [1,1,1,2,2,3,3,4,4,5]
    
    prop_matrix = np.zeros((5, 5, 5))
    post_hint_number = state.hands[player.player_index].get_number_hint()
    post_hint_color = state.hands[player.player_index].get_color_hint()

    if hint_type == 0: #color
        for i in hint_index:
            card_hint = state.hands[player.player_index[i]]
            post_hint_color[i] = card_hint.get_color()  
    elif hint_type == 1: #number
        for i in hint_index:
            card_hint = state.hands[player.player_index[i]]
            post_hint_number[i] = card_hint.get_number()  

    for i in range(len(player.card_in_hand)):
        if (post_hint_color[i] != 0) & (post_hint_number[i] != 0): #we got hints about that exact card
            prop_matrix[post_hint_color[i] - 1, post_hint_number[i]-1, i] = 1 # we are certain, that it is that card

        elif (post_hint_color[i] != 0) & (post_hint_number[i] == 0): #we know just the color
            cards_color_seen = sum(1 for card in cards_seen if card.get_color() == post_hint_color[i])
            for numbers in range(5):
                this_card_seen = sum(1 for card in cards_seen if (card.get_color() == post_hint_color[i]) & (card.get_number() == numbers + 1))
                n_tot = sum(np.sum(cards_in_game == numbers + 1))
                prop_matrix[post_hint_color[i] - 1, numbers, i] = (n_tot - this_card_seen)/(cards_of_a_color - cards_color_seen)

        elif (post_hint_color[i] == 0) & (post_hint_number[i] != 0): #we just know the number
            cards_number_seen = sum(1 for card in state.Board_pile if card.get_number() == post_hint_number[i])
            for colors in Color:
                this_card_seen = sum(1 for card in cards_seen if (card.get_color() == colors) & (card.get_number() == post_hint_number[i]))
                n_tot = sum(np.sum(cards_in_game == post_hint_number[i]))
                prop_matrix[colors - 1, post_hint_number[i] - 1, i] = (n_tot - this_card_seen)/(n_tot*5 - cards_number_seen)

        elif (post_hint_color[i] == 0) & (post_hint_number[i] == 0): #we don't know anything about the card
            for numbers in range(5):
                for colors in Color:
                    this_card_seen = sum(1 for card in cards_seen if (card.get_color() == colors) & (card.get_number() == numbers + 1))
                    n_tot = sum(np.sum(cards_in_game == numbers + 1))
                    prop_matrix[colors - 1, numbers, i] = (n_tot - this_card_seen)/(cards_left)
        
    return prop_matrix
