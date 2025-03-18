from Agent import Agent
from Card import Card
from typing import List

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

def playable(Card_to_check:"Card",Last_played: List[Card])->int:
     for i in Last_played:
            if i.get_color() == Card_to_check.get_color() : #Loop through to find the right color
                if (i.get_number()+1) == Card_to_check.get_number(): #Check if the card if playable
                    return 1
                else:
                    return 0