from card import Card, Color
from typing import List
from state import State
import numpy as np



def choose_action(state):

    _, certainty_play = evaluate_play_move(state)
    _, certainty_discard = evaluate_discard_move(state)
    _, _, _, information_gain = evaluate_hint_move(state)

    expected_outcome = [0,0,0]

    #Outcome of playing a card
    expected_outcome[0] = certainty_play - (1 - certainty_play)*1/(state.fuse_tokens) #*len(state.board_cards)

    #Outcome of discarding a card
    expected_outcome[2] = certainty_discard*(state.max_hint_tokens - state.hint_tokens)/state.max_hint_tokens
    
    #Outcome of hinting an other player
    if state.hint_tokens > 0:
        expected_outcome[1] = state.hint_tokens/state.max_hint_tokens*information_gain
    else:
        expected_outcome[1] = -100

    print("Expected outcome: ", expected_outcome)
    print("Information gain: ", information_gain)
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
            #Card got a hint in the last turn
            if card.hinted_number or card.hinted_color: 
                priority[i] = 1
            #Probability of this card still needed
            else:
                priority[i] = e[i] + 1

    #Index of the card with the highest priority
    discard_index = priority.index(max(priority))
    certainty = e[discard_index]
               
    return discard_index, certainty


def evaluate_hint_move(state: "State"):

    ##Function to evaluate which hint to give to the partner.
    highest_prio = -1
    best_hint = -1
    player_evaluate_hint = [0,1,2]
    player_evaluate_hint.pop(state.player_turn)
    player_hint_index = -1

    for item in player_evaluate_hint:
        for i, card in enumerate(state.players[item].hand_cards):
            hint_prio = 0

            # Checking the card's playability
            if card in state.playable_cards:
                hint_prio += 5

            '''# No hint received but useful in future
            if (card.hinted_color and card.hinted_number) == False:  # No hint received yet
                hint_prio += 1'''

            # Give hints that require less tokens (if tokens are low)
            '''if state.hint_tokens > 1:
                hint_prio += 2'''

        ## protect critical cards like 5
            if card.get_number() == 5 or card in state.discard_pile:
                hint_prio += 3

            # partner knows either color/number
            if card.hinted_color or card.hinted_number:
                hint_prio -= 100

            #if card.hinted_color and card.hinted_number:
                #hint_prio -= 100

            # If the card should be discarded soon, avoid giving hints about it
            if card in state.board_cards:
                hint_prio -= 3

            #  hints that provide more value
            #if ( card.get_number() == 1  and card not in state.board_cards) or card.get_number() == 5:
                #hint_prio += 4

            # Compare with highest priority so far and update the best_hint
            if hint_prio > highest_prio:
                highest_prio = hint_prio
                best_hint = i
                player_hint_index = item

    #Logic to determine which hint to give
    hint_choice ="o"
    hint_value = -1

    hint_hand = state.players[player_hint_index].hand_cards
    #print(hint_hand)
    info_before = np.zeros((5,5,5))

    for idx, j in enumerate(hint_hand):
        j.evaluate_probability_matrix(state)
        info_before[:, :, idx] = j.probability_matrix


    hint_card = hint_hand[best_hint]

    color_hint_priority = 1
    number_hint_priority = 0

    if hint_card.get_number() == 5:
        number_hint_priority = 5

    else:
        for x in hint_hand:
            if (x.get_number () == hint_card.get_number()):
                if x is state.playable_cards:
                    number_hint_priority += 1
            if (x.get_color() == hint_card.get_color()):
                color_hint_priority -= 1
            
    if color_hint_priority > number_hint_priority:
        hint_choice = "c"
        hint_value = hint_card.get_color()
        hint_array=[Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.WHITE]
        hint_array.remove(hint_value)
        hint_card.hinted_excluded_colors = hint_array
        hint_card.set_color_hint(True)

    elif color_hint_priority <= number_hint_priority:
        hint_choice = "n"
        hint_value = hint_card.get_number()

        hint_array=[1,2,3,4,5]
        hint_array.pop(hint_value-1)
        hint_card.hinted_excluded_numbers = hint_array
        hint_card.set_number_hint(True)

    info_after = np.zeros((5,5,5))

    for idx, j in enumerate(hint_hand):
        j.evaluate_probability_matrix(state)
        info_before[:, :, idx] = j.probability_matrix

    Total_info = 0.0

    for i in range(5):
        for j in range(5):
            for k in range(5):
                Total_info = abs(info_after[i,j,k]-info_before[i,j,k])
        
    return hint_choice,player_hint_index, hint_value, Total_info

