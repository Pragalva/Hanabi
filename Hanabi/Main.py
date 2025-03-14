from Card import Card
from Agent import Agent

#Setting the Deck and discard Pile
Game_Deck = Card.generate_deck()
Discard_pile = []

# Initilizing the Agents
player_1 = Agent('Player_1',1)
player_2 = Agent('Player_2',2)
player_3 = Agent('Player_3',3)

#Players draw thier intial hand
for x in range(5):
    player_1.draw_card(Game_Deck)
    player_2.draw_card(Game_Deck)
    player_3.draw_card(Game_Deck)

player1hand = player_1.get_cards_in_hand()
print(f"Player 1 = {player1hand}")

"""
player2hand = player_2.get_cards_in_hand()
print(f"Player 2 = {player2hand}")

player3hand = player_3.get_cards_in_hand()
print(f"Player 3 = + {player3hand}")

player_1.set_visible_cards(player_2,player_3)
player1Vis = player_1.get_visible_cards()
print(f"Cards visible to player 1 = '{player1Vis}")
"""

print("Which card would you like to discard")
discard_index = int(input())

player_1.discard_card(Game_Deck,Discard_pile,(discard_index-1))
print(f"Player 1 = {player_1.get_cards_in_hand()}")
print(Discard_pile)
