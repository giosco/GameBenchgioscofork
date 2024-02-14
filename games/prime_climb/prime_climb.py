
import ast
from api.classes import Agent, Action, Observation, AvailableActions, Rules
from dataclasses import dataclass, field
from typing import List, Tuple
import random
from prime_climb_card_manager import PrimeClimbCardManager


@dataclass
class PrimeClimbGame:
    rules: Rules = Rules(
        title="Prime Climb",
        summary="Roll the dice and move your two pawns from 1 - 101, knocking your opponents back to start as you go.  "
                "Players use addition, subtraction, multiplication and division to get the center of the board to land "
                "exactly on 101"
                "Players race to be the first to get to the center of the board while avoiding getting knocked back to "
                "the start by other players. "
                "Each player controls two pawns that start at the 0 circle. Players take turns rolling two 10-sided dice and applying the values to their two "
                "pawns using any of the four basic arithmetic operations: addition, subtraction, multiplication, and division. The first to get both"
                "pawns into the 101 circle exactly wins the game! Be careful: if another player lands on you, you get sent back to the start",
        additional_details={
            "Dice Rolling and Movement": "Players have two dice. The two numbers you roll will be used, one at a time, to move your pawns. In the case of doubles, you may use the number you rolled four times instead of twice. The 0 on the dice stands for 10. You must use all your rolls.",
            "Move Phase Operations": "During your Move Phase, you add, subtract, multiply, or divide the number your pawn is on by a number you rolled and send that pawn to the resulting number. You must use both of your rolled numbers, one at a time. If you have Keeper cards, you may choose to play one or more of them before, between, or after applying your dice rolls.",
            "Keeper and Action Cards": "There are two types of cards: Keeper Cards and Action Cards. Keeper Cards: If you draw a Keeper Card, keep that card, face up, for a future turn. You may play any number of Keeper cards during your Move phase. You may not play a Keeper Card the turn you draw it. Action Cards: Any card that does not say Keeper on it is an Action Card. When you draw an Action Card, immediately perform the action the card requires. If the Action Card requires you to move one of your own pawns, you must move the pawn that landed on the red space; if both your pawns moved to red spaces that turn, you may choose the pawn the card applies to.",
            "Board Restrictions": "Pawns may never move to a space not on the board, such as negative numbers, non-whole numbers, or numbers greater than 101.",
            "Bumping Rules": "If you end your Move Phase with either of your pawns on the same space as another pawn, send the pawn you landed on back to Start. Bumping is not optional. Note: You can bump your own pawns. Note: You bump a pawn only when you end your turn on an occupied space, not when you pass through an occupied space.",
            "Prime Cards": "You draw a Prime Card after your Move and Bump Phases are completed if at least one of your pawns is on an entirely red space (i.e., a prime number greater than 10), and that pawn did not begin its turn on that space. You may draw only one card per turn, even if both your pawns end on red spaces. No card trading is allowed!",
            "End of Game": "When your first pawn reaches the 101 circle exactly, remove it from the board. You cannot move to a number past 101, or bounce off 101. After your first pawn reaches 101, you must apply all dice rolls to your remaining pawn. You win immediately when you can apply a dice roll or Keeper card to land your second pawn on 101. You do not have to use both dice rolls on your winning move. Do not draw a Prime Card when you land on 101."
        }

    )
    id: str = "prime_climb"

    def init_game(self, agent1: Agent, agent2: Agent):
        self.states = [{
            "board": [None] * 102,
        }]
        self.agents = [agent1(team_id=0, agent_id=0, **self.agent_1_kwargs),
                       agent2(team_id=1, agent_id=1, **self.agent_2_kwargs)]

        # Initialize pawn positions with structure {team_id: {pawn_id: position, ...}, ...}
        self.pawns = {agent.team_id: {pawn_id: -1 for pawn_id in range(2)} for agent in self.agents}
        self.turn = 0
        self.winner = None
        self.dice = []
        self.cards = []  # Placeholder for Prime and Action cards
        self.game_log = []  # To store the sequence of moves and decisions
        self.card_manager = PrimeClimbCardManager()
        self.reverse_moves = {player: False for player in range(4)}
        self.skip_turns = {player: False for player in range(4)}


    def move_pawn(self, agent_id, pawn_index, new_position):
            # Validate new position is within board limits
            if 0 <= new_position <= 101:
                # Update the pawn's position in the pawns structure
                self.pawns[agent_id][pawn_index] = new_position
                # Check for bumping only if pawn is moved to a position on the board
                if new_position > 0:
                    self.check_bump(agent_id, pawn_index)

    def get_board_string(self):
        board = self.states[-1]["board"]
        row_strings = [", ".join(row) for row in board]
        board_string = "\n".join(row_strings)
        return board_string

    def calculate_available_moves(self, agent_id):
        moves = []
        dice_rolls = self.dice
        for pawn_id, position in self.pawns[agent_id].items():
            for roll in dice_rolls:
                # Add and Subtract
                new_position_add = position + roll
                new_position_sub = position - roll
                if 1 <= new_position_add <= 101:
                    moves.append((pawn_id, 'add', roll))
                if 1 <= new_position_sub <= 101:
                    moves.append((pawn_id, 'sub', roll))

                # Multiply
                new_position_mul = position * roll
                if 1 <= new_position_mul <= 101:
                    moves.append((pawn_id, 'mul', roll))

                # Divide
                if roll != 0 and position % roll == 0:
                    new_position_div = position // roll
                    if 1 <= new_position_div <= 101:
                        moves.append((pawn_id, 'div', roll))
        return moves

    def apply_move(self, player, pawn, operation, roll):
        current_position = self.pawns[player][pawn]
        new_position = current_position

        if operation == "add":
            new_position += roll
        elif operation == "sub":
            new_position -= roll
        elif operation == "mul":
            new_position *= roll
        elif operation == "div" and roll != 0:
            if current_position % roll == 0:
                new_position //= roll
        # Ensure the new position is within board limits
        if 1 <= new_position <= 101:
            # Update pawn position
            self.pawns[player][pawn] = new_position
            # Check for bump only if the move is valid
            self.check_bump(player, pawn)

    def check_bump(self, active_player, active_pawn):
        active_pawn_position = self.pawns[active_player][active_pawn]
        for player, pawns in self.pawns.items():
            if player != active_player:  # Avoid checking the active player's own pawns
                for pawn_id, position in pawns.items():
                    if position == active_pawn_position:  # If another pawn is on the same position
                        self.pawns[player][pawn_id] = -1  # Send the bumped pawn back to the start

    def check_win_condition(self):
        for player, pawns in self.pawns.items():
            if all(pos == 101 for pos in pawns.values()):  # Check if all pawns for the player are at position 101
                self.winner = player
                self.game_is_over = True
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

    def get_observation(self, agent: Agent) -> Tuple[Observation, AvailableActions]:
        self.roll_dice()  # Roll dice at the beginning of each turn
        dice_rolls = f"Dice rolls: {self.dice}"
        board_state = self.get_board_string()  # Custom method to represent the game state as a string

        # Calculate available moves based on the current game state and dice rolls
        available_moves = self.calculate_available_moves(agent.agent_id)

        observation = Observation(text=f"{board_state}\n{dice_rolls}")
        available_actions = AvailableActions(
            instructions="Select a pawn and an operation (add, sub, mul, div) based on your dice rolls.",
            openended={})
        return observation, available_actions

    def update(self, action, available_actions, agent):
        # Parse the action (assuming action.action_id is structured as "(pawn_idx, operation, dice_idx)")
        pawn_idx, operation, dice_idx = ast.literal_eval(action.action_id)

        # Apply the move
        if dice_idx < len(self.dice):
            self.apply_move(agent.agent_id, pawn_idx, operation, self.dice[dice_idx])

        # Check for win condition
        if self.check_win_condition():
            self.game_is_over = True
            self.winning_team = agent.team_id

    def roll_dice(self):
        roll1 = random.randint(0, 9)
        roll2 = random.randint(0, 9)
        self.dice = [10 if x == 0 else x for x in [roll1, roll2]]


