from card import Card, Color
from typing import List
from state import State


def choose_action(state):
    pass


def evaluate_play_move(state):
    # Initialize score lists
    g: list[float] = []
    e: list[float] = []
    priority: list[int] = []

    # Evaluate how good is to play each card
    for i, card in enumerate(state.players[state.player_turn].card_in_hand):
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
    
    return max_index


def evaluate_discard_move(state):
    return 0


def evaluate_hint_move(state: "State"):

    ##Function to evaluate which hint to give to the partner.
    highest_prio = -1
    best_hint = -1

    for i, card in enumerate(state.players[state.player_turn].card_in_hand):
        hint_prio = 0

        # Checking the card's playability
        if card in state.playable_cards:
            hint_prio += 5

        # No hint received but useful in future
        if (card.hinted_color and card.hinted_number) == False:  # No hint received yet
            hint_prio += 3

        # Give hints that require less tokens (if tokens are low)
        if state.hint_tokens > 1:
            hint_prio += 2

      ## protect critical cards like 5
        if card.get_number() == 5 or card in state.discard_pile:
            hint_prio += 3

        # partner knows either color/number
        if card.hinted_color or card.hinted_number:
            hint_prio += 1

        # If the card should be discarded soon, avoid giving hints about it
        if card in state.board_cards:
            hint_prio -= 3

        #  hints that provide more value
        if (card not in state.board_cards and card.get_number() == 1) or card.get_number() == 5:
            hint_prio += 4

        # Compare with highest priority so far and update the best_hint
        if hint_prio > highest_prio:
            highest_prio = hint_prio
            best_hint = i

    return best_hint

