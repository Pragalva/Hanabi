from Eval import eval_discard, playable, eval_play
from State import State
from Agent import Agent
from Prob import probability_matrix
import numpy as np

def Decision_for_action(current_state:"State",current_agent:"Agent", lifes_left:int):
    Player_2 = Agent('Player_2',2)

    best_discard_index = eval_discard(current_agent,current_state.Discard_pile,current_state.Board_pile)
    best_play_index= eval_play(current_agent, current_state)
    best_hint_index, hint_type, hinted_agent = (1, Player_2)


    current_probability_tensor = probability_matrix(current_agent,current_state,2,0)
    hint_probability_tensor = probability_matrix(hinted_agent,current_state,2,0)
    after_hint_probability_tensor = probability_matrix(hinted_agent,current_state,hint_type, best_hint_index)
    expected_outcome = [0,0,0]

    #Checking for best play
    for i in range(5):
        for j in range(5):
            if (lifes_left == 1):
                expected_outcome[0] += current_probability_tensor[i,j,best_play_index]*playable(current_agent.card_in_hand[best_play_index],current_state.Play_pile) + current_probability_tensor[i,j,best_play_index]*(1-playable(current_agent.card_in_hand[best_play_index],current_state.Play_pile))*(-len(current_state.Board_pile))
            else:
                expected_outcome[0] += current_probability_tensor[i,j,best_play_index]*playable(current_agent.card_in_hand[best_play_index],current_state.Play_pile)

    #Checking for best hint
    for i in range(5):
        for j in range(5):
            expected_outcome[1] += (after_hint_probability_tensor[i,j,best_hint_index] - hint_probability_tensor[i,j,best_hint_index])*playable(hinted_agent.card_in_hand[best_hint_index], current_state.Play_pile)

    #Checking for best discard
    for i in range(5):
        for j in range(5):
            expected_outcome[2] += current_probability_tensor[i,j, best_discard_index]*(1 if (current_agent.card_in_hand[best_discard_index] in current_state.Board_pile) else 0)

    best_action = np.argmax(expected_outcome) #0-> play card, 1-> give hint, 2-> discard

    return best_action




