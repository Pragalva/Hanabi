from Agent import Agent
from Card import Card, Color
from State_Andrea import State
from typing import List
import numpy as np

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
            cards_color_played = sum(1 for cards in board_pile if cards.get_color() == player.hint_color[i])
            if cards_color_played == 5:
                player.discard_prio[i] = 100
            else:
                player.discard_prio[i] += cards_color_played*0.1
        elif (player.hint_color[i] == 0) & (player.hint_number[i] != 0): #we just know the number
            cards_number_played = sum(1 for cards in board_pile if cards.get_number() == player.hint_number[i])
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

def playable(Card_to_check:"Card",Last_played: List[Card])->bool:
    for i in Last_played:
        if i.get_color() == Card_to_check.get_color() : #Loop through to find the right color
            if (i.get_number()+1) == Card_to_check.get_number(): #Check if the card if playable
                return True
    return False

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
        p_matrix = player.probability_matrix(player, state.Discard_pile, state.Board_pile)

        for playable_card in state.Play_pile:
            e1[i] += p_matrix[playable_card._color][playable_card._number][i]

        # Playable cards after playing the z-th card
        n_z: List[List[int]] = []
        for c, color in Color:
            for number in range(5):
                new_play_pile = state.Play_pile

                playable_cards_after_z = 0

                z_card = Card(number,color)

                if z_card in new_play_pile:
                    new_play_pile.remove(z_card)
                    y_card = Card(number + 1,color)
                    new_play_pile.append(y_card)
                    for player in range(3):
                        if player != state.player_turn:
                            for card in state.hands[player]:
                                if card in new_play_pile:
                                    playable_cards_after_z += 1
                
                n_z[c][number] = playable_cards_after_z

        # Average playable cards after playing the i-th card
        n_p: List[int] = [0, 0, 0, 0, 0]
        for c, color in Color:
            for number in range(5):
                n_p[i] += n_z[c][number] * p_matrix[color][number][i]

        # Second evaluation component based on the number of playable cards after playing the i-th card
        e2[i] = (n_p[i] / 10) * (1 - e1[i])

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
        return position
    
    # Check if more than one card share the same priority value
    position = np.argmax(priority[position])
    if len(position) == 1:
        return position
    
    # Check if more than one card share the same e1 value
    position = np.argmax(e1[position])
    if len(position) == 1:
        return position
    
    # Check if more than one card share the same e2 value
    position = np.argmax(e2[position])
    if len(position) == 1:
        return position
    
    # Just choose a random card
    position = np.random.choice(position)

    return position