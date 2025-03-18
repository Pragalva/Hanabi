import Agent
from Card import Color
import numpy as np

def probability_matrix (player:"Agent", discard_pile, board_pile):

    cards_seen = player.cards_visible + discard_pile + board_pile
    cards_left = 50 - len(cards_seen) 
    
    cards_of_a_color = 10
    
    cards_in_game = [1,1,1,2,2,3,3,4,4,5]
    
    prop_matrix = np.zeros((5, 5, 5))

    for i in range(len(player.card_in_hand)):
        if (player.hint_color[i] != 0) & (player.hint_number[i] != 0): #we got hints about that exact card
            prop_matrix[player.hint_color[i] - 1, player.hint_number[i]-1, i] = 1 # we are certain, that it is that card

        elif (player.hint_color[i] != 0) & (player.hint_number[i] == 0): #we know just the color
            cards_color_seen = sum(1 for card in cards_seen if card.color == player.hint_color[i])
            for numbers in range(5):
                this_card_seen = sum(1 for card in cards_seen if (card.color == player.hint_color[i]) & (card.number == numbers + 1))
                n_tot = sum(np.sum(cards_in_game == numbers + 1))
                prop_matrix[player.hint_color[i] - 1, numbers, i] = (n_tot - this_card_seen)/(cards_of_a_color - cards_color_seen)

        elif (player.hint_color[i] == 0) & (player.hint_number[i] != 0): #we just know the number
            cards_number_seen = sum(1 for card in board_pile if card.number == player.hint_number[i])
            for colors in Color:
                this_card_seen = sum(1 for card in cards_seen if (card.color == colors) & (card.number == player.hint_number[i]))
                n_tot = sum(np.sum(cards_in_game == player.hint_number[i]))
                prop_matrix[colors - 1, player.hint_number[i] - 1, i] = (n_tot - this_card_seen)/(n_tot*5 - cards_number_seen)

        elif (player.hint_color[i] == 0) & (player.hint_number[i] == 0): #we don't know anything about the card
            for numbers in range(5):
                for colors in Color:
                    this_card_seen = sum(1 for card in cards_seen if (card.color == colors) & (card.number == numbers + 1))
                    n_tot = sum(np.sum(cards_in_game == numbers + 1))
                    prop_matrix[colors - 1, numbers, i] = (n_tot - this_card_seen)/(cards_left)
        
    return prop_matrix
