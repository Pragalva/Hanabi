from card import Card, Color
from typing import List
from state import State
import numpy as np



def choose_action(state):

    play_index, certainty_play = evaluate_play_move(state)
    discard_index, certainty_discard = evaluate_discard_move(state)
    _, _, _, ratio = evaluate_hint_move(state)

    expected_outcome = [0,0,0]

    #Outcome of playing a card
    expected_outcome[0] = certainty_play - (1 - certainty_play)*len(state.board_cards) #/(state.fuse_tokens)

    #Outcome of discarding a card
    expected_outcome[2] = certainty_discard*(state.max_hint_tokens - state.hint_tokens)/state.max_hint_tokens
    
    #Outcome of hinting an other player
    if state.hint_tokens > 0:
        expected_outcome[1] = state.hint_tokens/state.max_hint_tokens*ratio 
        if play_index == discard_index:
            expected_outcome[1] = 100
    else:
        expected_outcome[1] = -100

    print("Expected outcome: ", expected_outcome)
    best_action = np.argmax(expected_outcome) #0-> play card, 1-> hint, 2-> discard

    return best_action


def evaluate_play_move(state):
    # Initialize score lists
    g = [0] * len(state.players[state.player_turn].hand_cards)
    e = [0] * len(state.players[state.player_turn].hand_cards)
    priority = [0] * len(state.players[state.player_turn].hand_cards)

    # Evaluate how good is to play each card
    for i, card in enumerate(state.players[state.player_turn].hand_cards):
        # Evaluation component based on the probability matrix
        e[i] = 0
        for playable_card in state.playable_cards:
            e[i] += card.probability_matrix[playable_card.color.value - 1][playable_card.number - 1]
        
        # Check if the card can be surely played successfully
        if e[i] == 1:
            g[i] = 1
            priority[i] = 3
        # Check if the card can be surely played unsuccessfully
        elif e[i] == 0:
            g[i] = 0
            priority[i] = 0
        else:
            # Check if the cards received hints during last turn
            if card.hinted_number or card.hinted_color: 
                g[i] = 1
                priority[i] = 2
            else:
                # Just calculate a value in between [0, 1]
                g[i] = e[i]
                priority[i] = 1
    
    max_index = 0
    max_value = 0
    for i in range(len(g)):
        if g[i] > max_value:
            max_value = g[i]
            max_index = i
        elif g[i] == max_value:
            if priority[i] > priority[max_index]:
                max_value = g[i]
                max_index = i
    
    certainty = e[max_index]
    print("Best play card: ", state.players[state.player_turn].hand_cards[max_index])

    return max_index, certainty


def evaluate_discard_move(state):
    e = [0] * len(state.players[state.player_turn].hand_cards)
    priority = [0] * len(state.players[state.player_turn].hand_cards)

    #Look at all of the cards in the players hand
    for i, card in enumerate(state.players[state.player_turn].hand_cards):
        e[i] = 0

        #Compare the cards to cards, which are already played on the board pile
        for played_cards in state.board_cards:
            e[i] += card.probability_matrix[played_cards.color.value - 1][played_cards.number - 1]

        #Card is surely already played on the board
        if e[i] == 1:
            priority[i] = 3
        #Card is surely still needed
        elif e[i] == 0:
            priority[i] = 0
        else:
            #Cards with information
            if card.hinted_number or card.hinted_color: 
                priority[i] = 1
            #Probability of this card still needed
            else:
                priority[i] = e[i] + 1

    #Index of the card with the highest priority
    discard_index = priority.index(max(priority))
    certainty = e[discard_index]

    print("Best discard card: ", state.players[state.player_turn].hand_cards[discard_index])
               
    return discard_index, certainty

def evaluate_hint_move(state: "State"):
    #initialize the hint choice, player to be hinted, hint value and information gain
    hint_choice = "o"
    player_hint_index = -1
    hint_value = -1
    ratio = 0

    #Look at the other players
    other_players = [0,1,2]
    other_players.pop(state.player_turn)

    max_num_hint_cards = 0

    #Who to be hinted?
    for j, players in enumerate(other_players):
        num_hint_cards = 0
        for i, card in enumerate(state.players[players].hand_cards):
            #card is playable
            if card in state.playable_cards:
                num_hint_cards += 1
            #card is unique
            if card.get_number() == 5 or card in state.discard_pile:
                num_hint_cards += 1
            #Is card already hinted?
            if card.hinted_number & card.hinted_color:
                num_hint_cards -= 1
        #take the player with the higher number of hintable cards
        if num_hint_cards > max_num_hint_cards:
            player_hint_index = players
            max_num_hint_cards = num_hint_cards

    #Which hint is the best?

    max_ratio_color = 0
    max_color = Color.RED

    #possible color hints:
    for colors in Color:
        num_hint_cards_color_playable = 0
        num_hint_cards_color_nonplayable = 0
        for i, card in enumerate(state.players[player_hint_index].hand_cards):
            #Is card already hinted?
            if card.get_color() == colors:
                if (card.hinted_color == False):
                    if card in state.playable_cards:
                        num_hint_cards_color_playable += 1
                    else:
                        num_hint_cards_color_nonplayable += 1
                    #card is unique
                    if card in state.discard_pile:
                        num_hint_cards_color_playable += 1    
        #check if there are even cards of this color            
        if (num_hint_cards_color_playable > 0) | (num_hint_cards_color_nonplayable > 0):
            ratio_color = num_hint_cards_color_playable/(num_hint_cards_color_playable + num_hint_cards_color_nonplayable)
        else:
            ratio_color = 0
        if ratio_color > max_ratio_color:
            max_ratio_color = ratio_color
            max_color = colors

    max_ratio_number = 0
    max_number = 1

    #possible number hints:
    for numbers in range(1,6):
        num_hint_cards_number_playable = 0
        num_hint_cards_number_nonplayable = 0
        for i, card in enumerate(state.players[player_hint_index].hand_cards):
            #Is card already hinted?
            if card.get_number() == numbers:
                if (card.hinted_number == False):
                    if card in state.playable_cards:
                        num_hint_cards_number_playable += 1
                    else:
                        num_hint_cards_number_nonplayable += 1
                    #card is unique
                    if (card in state.discard_pile) or (card.get_number() == 5):
                        num_hint_cards_number_playable += 1   
        #check if there are even cards of this number
        if (num_hint_cards_number_playable > 0) | (num_hint_cards_number_nonplayable > 0):
            ratio_number = num_hint_cards_number_playable/(num_hint_cards_number_playable + num_hint_cards_number_nonplayable)
        else:
            ratio_number = 0
        if ratio_number > max_ratio_number:
            max_ratio_number = ratio_number
            max_number = numbers

    if max_ratio_color > max_ratio_number:
        hint_choice = "c"
        hint_value = max_color
        ratio = max_ratio_color
    else:
        hint_choice = "n"
        hint_value = max_number
        ratio = max_ratio_number        


    return hint_choice, player_hint_index, hint_value, ratio