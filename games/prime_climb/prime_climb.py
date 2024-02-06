# Since we are in the PCI and cannot actually interface with a real API,
# we will simulate the API interface with a random decision-making function.
# The `api_interface_example` function below is designed to simulate receiving
# decisions from an external source (e.g., an API).
from api.classes import Agent, Action, Observation, AvailableActions, Rules
from dataclasses import dataclass, field
from typing import List, Tuple
import random
from prime_climb_card_manager import PrimeClimbCardManager


class PrimeClimbGame:
    rules: Rules = Rules(
        title="Prime Climb",
        summary="Roll the dice and move your two pawns from 1 - 101, knocking your opponents back to start as you go.  "
                "Players use addition, subtraction, multiplication and division to get the center of the board to land "
                "exactly on 101",
        additional_details=[
            "Prime Climb is a new board game that uses arithmetic to open a beautiful world of possibility. ",
            "Players race to be the first to get to the center of the board while avoiding getting knocked back to ",
            "the start by other players. Highlighting the power of the prime numbers, Prime Climb is mathematical, deep, creative, and fun.",
            "Each player controls two pawns that start at the 0 circle. Players take turns rolling two 10-sided dice and applying the values to their two ",
            "pawns using any of the four basic arithmetic operations: addition, subtraction, multiplication, and division. The first to get both",
            "pawns into the 101 circle exactly wins the game! Be careful: if another player lands on you, you get sent back to the start",
            "Roll the dice. The two numbers you roll will be used, one at a time, to move your pawns. In other words, if you roll a 3 and a 5, you have a ",
            "3 and a 5 to use on your turn; you do not get to use an 8, a 15, or a 35.",
            "In the case of doubles, you may use the number you rolled four times instead of twice. The 0 on the dice stands for 10. You must use all your rolls.",
            "During your Move Phase, you add, subtract, multiply, or divide the number your pawn is on by a number you rolled and send that pawn to the resulting number.",
            "You must use both of your rolled numbers, one at a time. If you have Keeper cards, you may choose to play one or more of them before, between, or after applying your dice ",
            "rolls. Your pawns may land on any space on the board, including occupied spaces.",
            "Pawns may never move to a space not on the board, such as negative numbers, non-whole numbers, or numbers greater than 101.",
            "If you end your Move Phase with either of your pawns on the same space as another pawn, send the pawn you landed on back to Start. Bumping is not optional.",
            "Note: You can bump your own pawns.",
            "Note: You bump a pawn only when you end your turn on an occupied space, not when you pass through an occupied space.",
            "You bump the pawn on 37 back to Start. You do not bump the pawn on 33 back to Start, since you did not end your Move Phase on 33.",
            "You draw a Prime Card after your Move and Bump Phases are completed if:",
            "At least one of your pawns is on an entirely red space (i.e., a prime number greater than 10), and",
            "That pawn did not begin its turn on that space.",
            "You may draw only one card per turn, even if both your pawns end on red spaces. No card trading is allowed!",
            " There are two types of cards: Keeper Cards and Action Cards. Keeper Cards",
            "If you draw a Keeper Card, keep that card, face up, for a future turn. You may play any number of Keeper ",
            "cards during your Move phase. You may not play a Keeper Card the turn you draw it.",
            "Action Cards Any card that does not say Keeper on it is an Action Card. When you draw an Action Card, ",
            "immediately perform the action the card requires.",
            "If the Action Card requires you to move one of own pawns, you must move the pawn that landed on the red ",
            "space; if both your pawns moved to red spaces that turn, you may choose the pawn the card applies to.",
            "If an Action Card takes your pawn to an occupied space on the board, bump the pawn you land on back to ",
            "Start. If an Action Card takes your pawn to a new red space, do not draw another Prime Card. In some",
            " positions, Action Cards may have no effect."
            "After you play a card, discard it. If you run out of cards, shuffle the discard pile and continue drawing",
            " as necessaryEnd of the Game When your first pawn reaches the 101 circle exactly, remove it from the board.",
            " You cannot move to a number past 101, or bounce off 101.",
            "After your first pawn reaches 101, you must apply all dice rolls to your remaining pawn. You win ",
            "immediately when you can apply a dice roll or Keeper card to land your second pawn on 101. You do not have ",
            "to use both dice rolls on your winning move.",
            "Do not draw a Prime Card when you land on 101."
            ]
    )
    def init_game(self, agent1 : Agent, agent2 : Agent):
        self.states = [{
            "board" : [None]*102,
        }]
        self.agents = [agent1(team_id = 0, agent_id = 0), agent2(team_id = 1, agent_id = 1)]

        ## added to make sure both players are given a turn before checking for winning or losing
        self.turncount_player0 = 0
        self.turncount_player1 = 0

        self.orbcount_player0 = 0
        self.orbcount_player1 = 0

        ## Replaced X with red and O with green
        ## Replaced marker with orb
        self.winning_team = None
        if self.show_state:
            print(f"Agent {self.agents[0].agent_type_id} is red and agent {self.agents[1].agent_type_id} is green")

        self.pawns = {agent.id: [0, 0] for agent in agents}  # Track pawn positions
        # Initialize board positions for pawns
        for agent_id, positions in self.pawns.items():
            for pawn_pos in positions:
                self.board[pawn_pos] = agent_id  # Mark the agent's pawns on the board
        self.card_manager = PrimeClimbCardManager()

    def move_pawn(self, agent_id, pawn_index, new_position):
        # Move a pawn and update the board representation
        old_position = self.pawns[agent_id][pawn_index]
        self.board[old_position] = None  # Remove pawn from old position
        self.pawns[agent_id][pawn_index] = new_position
        self.board[new_position] = agent_id  # Place pawn in new position
        current_position = self.pawns[player][pawn]
        new_position = current_position
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





    def get_board_string(self):
        board = self.states[-1]["board"]
        row_strings = [", ".join(row) for row in board]
        board_string = "\n".join(row_strings)
        return board_string

    def get_observation(self, agent : Agent) -> Tuple[Observation, AvailableActions]:
        board_string = self.get_board_string()
        observation = Observation(text=board_string)

        pawn = self.agent_data[agent.agent_id]["pawn"]
        available_actions = AvailableActions(
            instructions = f"Return your actions as tuples indicating coordinates of your pawns. The board starts with 0. Your pawns is  {pawn}.",
            predefined = {
                f"({row},{col})" : None for row in range(11) for col in range(6)
                    if self.states[-1]["board"][row][col] == '-'
                },
            openended = {}
        )
        return observation, available_actions
    def __init__(self, agents):
        self.agents = agents
        self.board = [None] * 102  # A list of length 102, representing spaces 0 to 101
        self.pawns = {agent.id: [0, 0] for agent in agents}  # Track pawn positions
        # Initialize board positions for pawns
        for agent_id, positions in self.pawns.items():
            for pawn_pos in positions:
                self.board[pawn_pos] = agent_id  # Mark the agent's pawns on the board
        self.card_manager = PrimeClimbCardManager()
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
