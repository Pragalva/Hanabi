from agent import Agent
from state import State, update_all_probability_matrices
from utils import termination_test


# Initilizing the Players
player_0 = Agent("Player 0", 0) # AI player
player_1 = Agent("Player 1", 1) # AI player
player_2 = Agent("Player 2", 2) # AI player
players = [player_0, player_1, player_2]

# Set initial state
state = State(players)

# Start game
for player in state.players:
    for card in range(5):
        player.draw_card(state)
print("Game set up!\n")

# Game loop
turn = 0
print("GAME START!\n")

update_all_probability_matrices(state)

while not termination_test(state):
    # Start of turn
    turn += 1
    print(f"TURN {turn}\n")
    print(f"{state.players[state.player_turn].player_name} is playing\n")

    # Print
    # print(state.playable_cards)
    state.players[state.player_turn].do_ai_action(state)

    # Change player's turn
    state.player_turn = (state.player_turn + 1) % 3

    print("Deck: ", len(state.deck), "\n Number of hints : ", state.hint_tokens)

print("GAME END!\n")