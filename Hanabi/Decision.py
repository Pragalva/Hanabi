from Eval import eval_discard, playable
from State import State
from Agent import Agent
from Prob import probability_matrix
import numpy as np

def Decision_for_action(current_state:"State",current_agent:"Agent"):
    best_discard_index =eval_discard(current_agent,current_state.Discard_pile,current_state.Board_pile)
    '''Check with the board to see if it is there'''
    best_play_index= 1
    best_hint= 1


    current_probability_tensor =probability_matrix(current_agent,current_state.Discard_pile,current_state.Board_pile)
    expected_outcome = 0

    #Checking for best play
    for i in range(5):
        for j in range(5):
            expected_outcome += current_probability_tensor[i,j,best_play_index]*playable(current_agent.card_in_hand[best_play_index],current_state.Play_pile)

    #Set parameters for when it can be played




