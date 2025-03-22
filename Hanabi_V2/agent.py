from card import Card
from card import Color
from typing import List
from state import State, update_all_probability_matrices
from evaluation import choose_action, evaluate_play_move, evaluate_discard_move, evaluate_hint_move


class Agent:
    def __init__(self, player_name: str, player_index: int):
        self.player_name: str = player_name
        self.player_index: int = player_index
        self.hand_cards: List["Card"] = []
    
    # Getters
    def get_hand_cards(self) -> str:
        full_hand = ""
        for card in self.hand_cards:
            full_hand += card.__repr__() + " "
        return full_hand

    # Actions
    def draw_card(self, state: "State"):
        if(len(state.deck) != 0 and len(self.hand_cards) <= 5):
            self.hand_cards.append(state.deck.pop(0))
            print(f"{self.player_name} has drawn a card\n")


    def discard_card(self, state: "State", discard_index: int):
        discarded_card = self.hand_cards.pop(discard_index)

        state.discard_pile.append(discarded_card)

        print(f"{self.player_name} has discarded a {discarded_card.__repr__()}\n")

        # Refill the hint tokens
        if(state.hint_tokens < 8):
            state.hint_tokens += 1

        self.draw_card(state)

        update_all_probability_matrices(state)


    def play_card(self, state: "State", play_index: int):
        played_card = self.hand_cards.pop(play_index)

        print(f"{self.player_name} has played a {played_card.__repr__()}\n")

        # print(played_card)
        # print(state.playable_cards)

        if played_card in state.playable_cards:
            print(f"The {played_card.__repr__()} has been played succesfully\n")

            state.board_cards.append(played_card)
            state.playable_cards.remove(played_card)
            state.playable_cards.append(Card(played_card.get_number() + 1, played_card.get_color()))
        else:
            print(f"The {played_card.__repr__()} couldn't be played succesfully\n")

            state.fuse_tokens -= 1
            state.discard_pile.append(played_card)

        # for card in state.playable_cards:
        #     # Look for the card with the right color
        #     if played_card.get_color() == card.get_color():
        #         # Look for the card with the right number
        #         if played_card.get_number() == (card.get_number() + 1):
        #             print(f"The {played_card.__repr__()} has been played succesfully\n")

        #             state.board_cards.append(played_card)
        #             state.playable_cards.remove(card)
        #             state.playable_cards.append(played_card)
        #         else:
        #             print(f"The {played_card.__repr__()} couldn't be played succesfully\n")

        #             state.fuse_tokens -= 1
        #             state.discard_pile.append(played_card)

        self.draw_card(state)

        update_all_probability_matrices(state)


    def give_color_hint(self, state: "State", player_hint_index: int, color: "Color"):
        # Give hint
        print(f"{self.player_name} has given a color hint to {state.players[player_hint_index].player_name}\n")

        for card_index, card in enumerate(state.players[player_hint_index].hand_cards):
            if card.get_color() == color:
                card.set_color_hint(True)
                card.hinted_excluded_colors.extend(c for c in Color if (c != color or c != Color.NO_COLOR))
                print(f"{state.players[player_hint_index].player_name} has a {color} card in the position {card_index + 1}")
            else:
                card.hinted_excluded_colors.append(color)       
        # Spend the hint token
        state.hint_tokens -= 1

        update_all_probability_matrices(state)


    def give_number_hint(self, state: "State", player_hint_index: int, number: int):
        # Give hint
        for card_index, card in enumerate(state.players[player_hint_index].hand_cards):
            if card.get_number() == number:
                card.set_number_hint(True)
                card.hinted_excluded_numbers.extend(n for n in [1, 2, 3, 4, 5] if n != number)
                print(f"{state.players[player_hint_index].player_name} has a {number} card in the position {card_index + 1}")
            else:
                card.hinted_excluded_numbers.append(number)
        
        # Spend the hint token
        state.hint_tokens -= 1

        update_all_probability_matrices(state)


    def do_player_action(self, state: "State"):
        # Show other players' hands
        print(f"Hand of {state.players[1].player_name}:", state.players[1].get_hand_cards(), "\n")
        print(f"Hand of {state.players[2].player_name}:", state.players[2].get_hand_cards(), "\n")
        print("Current Board: ", state.board_cards,"\n")
        print("Number of hints left: ", state.hint_tokens, ", Number of lives left: ", state.fuse_tokens, "\n")

        # Player's action
        print(f"{state.players[state.player_turn].player_name}, what's your move? Type 'p' to play a card, 'd' to discard or 'h' to give a hint\n")

        # Check the player's action
        valid_key_action = False
        while not valid_key_action:
            action_choice = input(">>> ")
            
            # Check valid action
            if action_choice not in ('p', 'd', 'h'):
                print("Invalid action! Please try again\n")
                continue
            valid_key_action = True

            # Resolve play action
            if action_choice == 'p':
                print(f"What card do you want to play? Type a number from 1 to 5\n")
                play_card_index = (int(input(">>> ")) - 1) % 5

                state.players[state.player_turn].play_card(state, play_card_index)

            # Resolve discard action
            elif action_choice == 'd':
                print(f"What card do you want to discard? Type a number from '1' to '5'\n")
                discard_card_index = (int(input(">>> ")) - 1) % 5

                state.players[state.player_turn].discard_card(state, discard_card_index)

            # Resolve hint action
            elif action_choice == 'h':
                if state.hint_tokens <= 0:
                    print("You have no more hint tokens left! Choose another action!\n")
                    continue

                print(f"What type of hint do you want to give? Type 'n' or 'c'\n")

                valid_hint_type = False
                while not valid_hint_type:
                    hint_type_choice = input(">>> ")
                    
                    # Check valid hint choice
                    if hint_type_choice not in ('n', 'c'):
                        print("Invalid action! Please try again\n")
                        continue
                    valid_hint_type = True
                
                    # Choosing player target for hint
                    print("Which player should be target for the hint? Type '1' or '2'\n")
                    player_hint_index = ((int(input(">>> ")) - 1) % 2) + 1

                    if hint_type_choice == 'n':
                        print("What number should be hinted? Type a number from '1' to '5'\n")
                        hinted_number = (int(input(">>> "))) % 5

                        state.players[state.player_turn].give_number_hint(state, player_hint_index, hinted_number)
                    
                    elif hint_type_choice == 'c':
                        print("What color should be hinted? Type 'r', 'b', 'g', 'y' or 'w'\n")

                        valid_color_hint = False
                        while not valid_color_hint:
                            hinted_color = input(">>> ")

                            # Check valid hint choice
                            if hinted_color not in ('r', 'b', 'g', 'y', 'w'):
                                print("Invalid action! Please try again\n")
                                continue
                            valid_hint_type = True

                            if hinted_color == 'r':
                                hinted_color = Color.RED
                            elif hinted_color == 'b':
                                hinted_color = Color.BLUE
                            elif hinted_color == 'g':
                                hinted_color = Color.GREEN
                            elif hinted_color == 'y':
                                hinted_color = Color.YELLOW
                            elif hinted_color == 'w':
                                hinted_color = Color.WHITE

                            state.players[state.player_turn].give_color_hint(state, player_hint_index, hinted_color)


    def do_ai_action(self, state: "State"):
        action = choose_action(state)

        # Play move
        if action == 0:
            play_card_index, _ = evaluate_play_move(state)
            self.play_card(state, play_card_index)
        # Hint move
        elif action == 1:
            hint_type_choice, player_hint_index, hinted_value, _ = evaluate_hint_move(state)
            if hint_type_choice == "n":
                self.give_number_hint(state, player_hint_index, hinted_value)
            elif hint_type_choice == "c":
                if hinted_value == 1:
                    hinted_value = Color.RED
                elif hinted_value == 2:
                    hinted_value = Color.BLUE
                elif hinted_value == 3:
                    hinted_value = Color.GREEN
                elif hinted_value == 4:
                    hinted_value = Color.YELLOW
                elif hinted_value == 5:
                    hinted_value = Color.WHITE
                self.give_color_hint(state, player_hint_index, hinted_value)
        # Discard move
        elif action == 2:
            discard_card_index, _ = evaluate_discard_move(state)
            self.discard_card(state, discard_card_index)