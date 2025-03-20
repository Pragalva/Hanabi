from Agent import Agent
from card import card
from typing import List


# Evaluation function to choose which hint to give
def eval_hint(player: "Agent", board_pile, discard_pile, last_played: List[Card], info_tokens: int) -> int:

    ##Function to evaluate which hint to give to the partner.

    highest_prio = -1
    best_hint = -1


    for i, card in enumerate(player.card_in_hand):
        hint_prio = 0

        # Checking the card's playability
        if playable(card, last_played) == 1:
            hint_prio += 5

        # No hint received but useful in future
        if player.hint_color[i] == 0 and player.hint_number[i] == 0:  # No hint received yet
            hint_prio += 3

        # Give hints that require less tokens (if tokens are low)
        if info_tokens > 1:
            hint_prio += 2

      ## protect critical cards like 5
        if card.get_number() == 5 or card in discard_pile:
            hint_prio -= 3

        # partner knows either color/number
        if player.partner_knows[i]:
            hint_prio += 1

        # If the card should be discarded soon, avoid giving hints about it
        if player.discard_prio[i] > 80:
            hint_prio -= 2

        #  hints that provide more value
        if card.get_number() == 1 or card.get_number() == 5:
            hint_prio += 4

        # Compare with highest priority so far and update the best_hint
        if hint_prio > highest_prio:
            highest_prio = hint_prio
            best_hint = i

    return best_hint


def playable(card_to_check: "Card", last_played: List[Card]) -> int:

    ##Function to check if a card is playable based on the last played cards.
    ##A card is playable if it matches the color or the next number in the sequence.

    for i in last_played:
        if i.get_color() == card_to_check.get_color():
            if (i.get_number() + 1) == card_to_check.get_number():  # checking for sequential playability
                return 1
    return 0  # If the card is not playable

