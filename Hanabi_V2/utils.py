import random
from typing import List
from card import Card, Color
#from state import State


# Generate a shuffled deck of cards
def generate_deck() -> List["Card"]:
    # Defining the number of cards that we will have for our game
    card_copies_for_color = [1,1,1,2,2,3,3,4,4,5]

    # Assemble the deck
    deck: List["Card"] = []
    for color in Color:
        if color == Color.NO_COLOR:
            continue
        for number in card_copies_for_color:
            card = Card(number, color)
            deck.append(card)
    
    # Shuffle the deck
    random.shuffle(deck)
    return deck


# Initialize the playable cards on the board
def initialize_playable_cards() -> List["Card"]:
    playable_cards: List[Card] = []
    
    for color in Color:
        if color == Color.NO_COLOR:
            continue
        card = Card(0, color)
        playable_cards.append(card)
    
    return playable_cards


# Check if the game is over
def termination_test(state) -> bool:
    terminate = False
    if (len(state.deck) == 0):
        state.rounds_until_game_ends -= 1
    if len(state.board_cards) == 25 or (state.fuse_tokens == 0) or (state.rounds_until_game_ends == 0):
        terminate = True

    return terminate
