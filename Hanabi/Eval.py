import numpy as np

import Agent
import State

# Evaluation function to choose with card to discard 
def eval_discard (player: "Agent", discard_pile, board_pile):
    #Prioritizing which card to discard first
    #higher numbers in discard_prio means that this card should be discarded first 
    highest_prio = -1
    best2discard = -1

    for i, card in enumerate(player.card_in_hand):
        # Card is already on the board
        if (player.hint_color[i] != 0) & (player.hint_number[i] != 0): #we got hints about that exact card
            if (card in board_pile): # card is already been played
                player.discard_prio[i] = 100
        elif (player.hint_color[i] != 0) & (player.hint_number[i] == 0): #we know just the color
            cards_color_played = sum(1 for card in board_pile if card.color == player.hint_color[i])
            if cards_color_played == 5:
                player.discard_prio[i] = 100
            else:
                player.discard_prio[i] += cards_color_played*0.1
        elif (player.hint_color[i] == 0) & (player.hint_number[i] != 0): #we just know the number
            cards_number_played = sum(1 for card in board_pile if card.number == player.hint_number[i])
            if cards_number_played == 5:
                player.discard_prio[i] = 100
            else:
                player.discard_prio[i] += cards_number_played*0.1
        # No hints for that card
        elif (player.hint_color[i] == 0) & (player.hint_number[i] == 0): #we don't know anything about the card
            player.discard_prio[i] += 1
        # Protect unique cards
        if (player.hint_number[i] == 5)|((player.hint_color[i] != 0) & (player.hint_number[i] != 0) & (card in discard_pile)):
            player.discard_prio[i] = 0
    
    #choose the card with the highest number of discard_prio to discard
        if player.discard_prio[i] > highest_prio:
            highest_prio = player.discard_prio[i]
            best2discard = i
    
    return best2discard

# Evaluation function to choose with card to play 
def eval_play (player: "Agent", state: "State"):
    # Initialize score lists
    g: list[float] = []
    priority: list[int] = []
    e1: list[float] = []
    e2: list[float] = []

    # Calculate mistakes coefficient
    m = (state.Fuse_Tokens ** 2 + 1) / 10

    # Evaluate how good is to play each card
    for i, card in enumerate(player.card_in_hand):
        # First evaluation component based on the probability matrix
        e1[i] = sum(player.card_in_hand[i].probability_matrix[state.Play_pile._number][state.Play_pile._color])

        # Playable cards after playing the z-th card
        for state.
        n_z[i] = 

        # Average playable cards after playing the i-th card
        for 
        n_p[i] = sum(player.card_in_hand[i].probability_matrix[][])

        # Second evaluation component based on the number of playable cards after playing the i-th card
        e2[i] = (n_p[i] / 12) * (1 - e1[i])

        # Check if the card can be surely played successfully
        if e1[i] == 1:
            g[i] = 1
            priority[i] = 3
        # Check if the card can be surely played unsuccessfully
        elif e1[i] == 0:
            g[i] = 0
            priority[i] = 0
        else:
            # Check if the cards received hints during last turn
            if player.card_in_hand[i].hint_color_pending or player.card_in_hand[i].hint_number_pending: 
                g[i] = 1
                priority[i] = 2
            else:
                # Just calculate a value in between [0, 1]
                g[i] = m*(e1[i] + e2[i])
                priority[i] = 1
    
    ### Decision process
    value = max(g)

    # Check if more than one card share the same g value
    position = np.argmax(g)
    if len(position) == 1:
        return position, value
    
    # Check if more than one card share the same priority value
    position = np.argmax(priority[position])
    if len(position) == 1:
        return position, value
    
    # Check if more than one card share the same e1 value
    position = np.argmax(e1[position])
    if len(position) == 1:
        return position, value
    
    # Check if more than one card share the same e2 value
    position = np.argmax(e2[position])
    if len(position) == 1:
        return position, value
    
    # Just choose a random card
    position = np.random.choice(position)

    return position, value