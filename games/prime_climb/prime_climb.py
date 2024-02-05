# Since we are in the PCI and cannot actually interface with a real API,
# we will simulate the API interface with a random decision-making function.
# The `api_interface_example` function below is designed to simulate receiving
# decisions from an external source (e.g., an API).
from api.classes import Agent, Action, Observation, AvailableActions, Rules
from dataclasses import dataclass, field
from typing import List, Tuple
import random
from prime_climb_card_manager import PrimeClimbCardManager


# Simulated API interface function
def api_interface_example(player):
    # In a real scenario, this would make an API call to get the decisions from an external agent
    # Here, we simulate it with random decisions
    operations = ["add", "sub", "mul", "div"]
    dice_indices = [0, 1]
    move_decisions = [(pawn, random.choice(operations), random.choice(dice_indices)) for pawn in range(2)]
    return move_decisions


# Now, let's proceed to test the simulation with this simulated API interface function.
# We will uncomment the function calls and execute the game.

class PrimeClimbGame:
    def __init__(self):
        self.pawns = {player: [0, 0] for player in range(4)}  # Assuming a 4-player game
        self.turn = 0
        self.winner = None
        self.dice = []
        self.cards = []  # Placeholder for Prime and Action cards
        self.game_log = []  # To store the sequence of moves and decisions
        self.card_manager = PrimeClimbCardManager()
        self.reverse_moves = {player: False for player in range(4)}
        self.skip_turns = {player: False for player in range(4)}
    def roll_dice(self):
        roll1 = random.randint(0, 9)
        roll2 = random.randint(0, 9)
        self.dice = [10 if x == 0 else x for x in [roll1, roll2]]

    def apply_move(self, player, pawn, operation, roll):
        current_position = self.pawns[player][pawn]
        new_position = current_position
        if self.reverse_moves[player]:
            new_position = current_position - roll  # Reverse the move
            self.reverse_moves[player] = False  # Clear the reverse effect after applying
        if operation == "add":
            new_position += roll
        elif operation == "sub":
            new_position -= roll
        elif operation == "mul":
            new_position *= roll
        elif operation == "div" and roll != 0:
            if current_position % roll == 0:
                new_position //= roll

        if 0 <= new_position <= 101:
            self.pawns[player][pawn] = new_position
            self.check_bump(player, pawn)

    def check_bump(self, player, pawn):
        position = self.pawns[player][pawn]
        for opponent, pawns in self.pawns.items():
            if opponent != player:
                for idx, opp_position in enumerate(pawns):
                    if opp_position == position:
                        self.pawns[opponent][idx] = 0

    def check_win_condition(self):
        for player, positions in self.pawns.items():
            if all(pos == 101 for pos in positions):
                self.winner = player
                return True
        return False

    def play_turn(self, player, move_decisions):
        global card
        if self.skip_turns[player]:
            print(f"Player {player}'s turn is skipped.")
            self.skip_turns[player] = False  # Clear the skip effect after applying
            return False  # Skip the turn
        self.roll_dice()
        for pawn_idx, operation, dice_idx in move_decisions:
            if dice_idx < len(self.dice):
                self.apply_move(player, pawn_idx, operation, self.dice[dice_idx])
                self.game_log.append((player, pawn_idx, operation, self.dice[dice_idx]))
                if self.check_win_condition():
                    break
                # Draw and apply a card effect after the pawn moves
                card = self.card_manager.draw_card()
                if card:
                    self.card_manager.apply_card_effect(card, self, player)
                    self.card_manager.discard_card(card)  # Discard the card after using it
        self.card_manager.apply_card_effect(card, self, player)
    def play_game(self, api_interface):
        while self.winner is None:
            current_player = self.turn % len(self.pawns)
            move_decisions = api_interface(current_player)
            self.play_turn(current_player, move_decisions)
            self.turn += 1



# Initialize and play the game
game = PrimeClimbGame()
game.play_game(api_interface_example)

# Return the results of the simulation
game_winner, game_log = game.winner, game.game_log
game_winner, game_log
