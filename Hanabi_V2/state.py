from utils import generate_deck, initialize_playable_cards
from card import Card
from typing import List

class State:
    def __init__(self, players):
        self.deck: List["Card"] = generate_deck()
        self.full_deck: List["Card"] = self.deck.copy()
        self.discard_pile: List["Card"] = []
        self.playable_cards: List["Card"] = initialize_playable_cards()
        self.board_cards: List["Card"] = []
        self.max_hint_tokens: int = 8
        self.max_fuse_tokens: int = 3
        self.hint_tokens: int = self.max_hint_tokens
        self.fuse_tokens: int = self.max_fuse_tokens

        self.player_turn = 0
        self.rounds_until_game_ends = 3

        self.players = players


def update_all_probability_matrices(state):
    for player in state.players:
        for card in player.hand_cards:
            card.evaluate_probability_matrix(state)
