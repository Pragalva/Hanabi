from enum import Enum
from typing import List
# from state import State


# Correspondence between card color and int value
class Color(Enum):
    NO_COLOR = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    WHITE = 5


class Card:
    # Constructor and print
    def __init__(self, number: int, color: Color):
        self.number: int = number
        self.color: "Color" = color
        self.hinted_number: bool = False
        self.hinted_color: bool = False
        self.hinted_excluded_numbers: List[int] = []
        self.hinted_excluded_colors: List["Color"] = []
        self.probability_matrix: List[List[float]]
    def __repr__(self):
        return f"{self.color} {self.number}"

    # Getters
    def get_number(self) -> int:
        return self.number
    def get_color(self) -> "Color":
        return self.color
    def get_color_hint(self) -> bool:
        return self.hinted_color
    def get_number_hint(self) -> bool:
        return self.hinted_number

    # Setters
    def set_color_hint(self, hint):
        self.hinted_color = hint
    def set_number_hint(self, hint):
        self.hinted_number = hint


    # Calculate and update probability matrix
    def evaluate_probability_matrix(self, state):
        # Virtual copy of deck
        list_of_deck_cards = state.full_deck.copy()

        # List of cards visible from the player who is taking the turn
        visible_cards: List["Card"] = []
        for card in state.board_cards:
            visible_cards.append(card)
        for card in state.discard_pile:
            visible_cards.append(card)
        for index, player in enumerate(state.players):
            if index != state.player_turn:
                for card in player.hand_cards:
                    visible_cards.append(card)

        # Remove possible cards from virtual deck based on hints
        for card in list_of_deck_cards:
            if (card.get_number() in self.hinted_excluded_numbers) or (card.get_color() in self.hinted_excluded_colors):
                list_of_deck_cards.remove(card)
        
        # Remove possible cards from virtual deck based on visible cards ##################
        list_of_deck_cards_copy = list_of_deck_cards.copy()
        for card in list_of_deck_cards:
            for visible_card in visible_cards:
                if card == visible_card:
                    list_of_deck_cards_copy.remove(card)
                    visible_cards.remove(visible_card)
                    break
        list_of_deck_cards = list_of_deck_cards_copy.copy()
        
        # Count the occurences of each card in the virtual deck
        self.probability_matrix = [[0 for i in range(5)] for j in range(5)]
        for card1 in list_of_deck_cards:
            count = 0
            for card2 in list_of_deck_cards:
                if card1 == card2:
                    count += 1
            self.probability_matrix[card1.get_color().value - 1][card1.get_number() - 1] = count / len(list_of_deck_cards)
