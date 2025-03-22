from Card import Card
from Agent import Agent
from State_Andrea import State
from Decision import Decision_for_action
from Eval import eval_discard, eval_play 
from eval_hint import eval_hint

#Setting the Deck and discard Pile
Game_Deck = Card.generate_deck() #Game deck
Discard_pile = [] #List of discarded cards
Play_pile = Card.generate_play_pile() #List of next playable cards
Board_pile = [] #List of played cards

#Setting Game parameters
Total_hints = 8
Fuse_Token = 3

# Initilizing the Agents
player_0 = Agent('Player_1', 0)
player_1 = Agent('Player_2', 1)
player_2 = Agent('Player_3', 2)
players = [player_0, player_1, player_2]

# Set state
state = State(Game_Deck, Discard_pile, Play_pile, Board_pile, Total_hints, Fuse_Token)

#Players draw their initial hand
for card in range(5):
    for player in players:
        player.draw_card(state)

# Game loop
while not state.termination_test():
    # Start of turn
    #setting hands in agent as a lot of our functions use this value
    player_0.set_card_in_hand(state)
    player_1.set_card_in_hand(state)
    player_2.set_card_in_hand(state)


    print(f"Turn of Player {state.player_turn}")

    # Real person player management
    if state.player_turn == 0:
        print("Visible Cards: ", player_0.get_visible_cards(state))
        print("Board: ", state.Board_pile)
        print(f"Player {state.player_turn}, what's your move?\n")
        print("Type 'p' to play a card\n")
        print("Type 'd' to discard a card\n")
        print("Type 'h' to give a hint\n")

        # Check the player's action
        valid_action = False
        while not valid_action:
            action_choice = input(">>> ")
            
            # Check valid action
            if action_choice not in ('p', 'd', 'h'):
                print("Invalid action! Please try again\n")
                continue
            valid_action = True

            # Resolve play action
            if action_choice == 'p':
                print(f"What card do you want to play?\n")
                print("Type a number from 1 to 5\n")
                play_card_index = (int(input(">>> ")) - 1) % 5

                players[state.player_turn].play_card(state, play_card_index)

            # Resolve discard action
            elif action_choice == 'd':
                print(f"What card do you want to discard?\n")
                print("Type a number from '1' to '5'\n")
                discard_card_index = (int(input(">>> ")) - 1) % 5

                players[state.player_turn].discard_card(state, discard_card_index)

            # Resolve hint action
            elif action_choice == 'h':
                print(f"What type of hint do you want to give?\n")
                print("Type 'n' or 'c'\n")

                valid_hint_type = False
                while not valid_hint_type:
                    hint_type_choice = input(">>> ")
                    
                    # Check valid hint choice
                    if hint_type_choice not in ('n', 'c'):
                        print("Invalid action! Please try again\n")
                        continue
                    valid_hint_type = True
                
                # Choosing player target for hint
                print("Which player should be target for the hint?\n")
                print("Type '1' or '2'\n")
                player_hint_index = (int(input(">>> ")) - 1) % 2

                # Choosing card target for hint
                print("What card should be target for the hint?\n")
                print("Type a number from '1' to '5'\n")
                card_hint_index = (int(input(">>> ")) - 1) % 5

                players[state.player_turn].give_hint(state, hint_type_choice, player_hint_index, card_hint_index)
    
    if state.player_turn != 0:
        print(f"Player {state.player_turn} is playing\n")
        
        '''Something is wrong with overgiving the Agent with players[state.player_turn]'''
        action_choice = Decision_for_action(state, players[state.player_turn],Fuse_Token)

        if action_choice == 0:
            players[state.player_turn].play_card(state, eval_play)
        elif action_choice == 1:
            players[state.player_turn].discard_card(state, eval_discard)
        elif action_choice == 2:
            players[state.player_turn].give_hint(state, eval_hint)


    # Change player's turn
    state.player_turn = (state.player_turn + 1) % 3

# player1hand = player_1.get_cards_in_hand()
# print(f"Player 1 = {player1hand}")

"""
player2hand = player_2.get_cards_in_hand()
print(f"Player 2 = {player2hand}")

player3hand = player_3.get_cards_in_hand()
print(f"Player 3 = + {player3hand}")

player_1.set_visible_cards(player_2,player_3)
player1Vis = player_1.get_visible_cards()
print(f"Cards visible to player 1 = '{player1Vis}")
"""

print("Which card would you like to play")
discard_index = int(input())

player_1.play_card(Game_Deck,Play_pile,Discard_pile,discard_index-1,Fuse_Token)
#player_1.discard_card(Game_Deck,Discard_pile,(discard_index-1),Total_hints)
print(f"Player 1 = {player_1.get_cards_in_hand()}")
print(Discard_pile)
print(Play_pile)
