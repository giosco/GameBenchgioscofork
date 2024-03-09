
import ast
from api.classes import Agent, Action, Observation, AvailableActions, Rules, Game
from dataclasses import dataclass, field
from typing import List, Tuple, Any
import random
from games.prime_climb.prime_climb_card_manager import PrimeClimbCardManager

len_board=20
@dataclass
class PrimeClimbGame(Game):
    rules: Rules = field(default_factory=lambda: Rules(
        title="Prime Climb",
        summary="Roll the dice and move your two pawns from 1 to {len_board}, knocking your opponents back to start as you go.  "
                "Players use addition, subtraction, multiplication and division to get the center of the board to land "
                "exactly on len_board"
                "Players race to be the first to get to the center of the board while avoiding getting knocked back to "
                "the start by other players. "
                "Each player controls two pawns that start at the 1 circle. Players take turns rolling two 10-sided dice and applying the values to their two "
                "pawns using any of the four basic arithmetic operations: addition, subtraction, multiplication, and division. The first to get both"
                "pawns into the 101 circle exactly wins the game! Be careful: if another player lands on you, you get sent back to the start",
        additional_details={
            "Dice Rolling and Movement": "Players have two dice. The two numbers you roll will be used, one at a time, to move your pawns. In the case of doubles, you may use the number you rolled four times instead of twice. The 0 on the dice stands for 10. You must use all your rolls.",
            "Move Phase Operations": "During your Move Phase, you add, subtract, multiply, or divide the number your pawn is on by a number you rolled and send that pawn to the resulting number. You must use both of your rolled numbers, one at a time. If you have Keeper cards, you may choose to play one or more of them before, between, or after applying your dice rolls.",
            "Action Cards": "Action Cards: Any card that does not say Keeper on it is an Action Card. When you draw an Action Card, immediately perform the action the card requires. The Action card requires you to move one of your own pawns by 5 positions on the board, you must move the pawn that has the lower position on the board",
            "Board Restrictions": "Pawns may never move to a space not on the board, such as negative numbers, non-whole numbers, or numbers greater than 101.",
            "Bumping Rules": "If you end your Move Phase with either of your pawns on the same space as another pawn, send the pawn you landed on back to Start. Bumping is not optional. Note: You can bump your own pawns. Note: You bump a pawn only when you end your turn on an occupied space, not when you pass through an occupied space.",
            "Prime Cards": "You draw a Prime Card after your Move and Bump Phases are completed if at least one of your pawns is on a prime number greater than 10, and that pawn did not begin its turn on that space. Move your pawn to the next board values that is a prime number. You may draw only one card per turn. No card trading is allowed!",
            "End of Game": "When your first pawn reaches the 101 circle exactly, remove it from the board. You cannot move to a number past 101, or bounce off 101. After your first pawn reaches 101, you must apply all dice rolls to your remaining pawn. You win immediately when you can apply a dice roll or Keeper card to land your second pawn on 101. You do not have to use both dice rolls on your winning move. Do not draw a Prime Card when you land on 101."
        }

    )
                         )
    id: str = "prime_climb"
    def init_game(self, agent1_class: Agent, agent2_class: Agent):
        self.states = [{
            "board": ["-"] * len_board,
        }]
        agent1 = agent1_class(**self.agent_1_kwargs)
        agent2 = agent2_class(**self.agent_2_kwargs)
        agent1.team_id = 1
        agent1.agent_id = 1
        agent2.team_id = 2
        agent2.agent_id = 2
        self.agents = [agent1, agent2]
        # Initialize pawn positions with structure {team_id: {pawn_id: position, ...}, ...}
        self.pawns = {
            agent.team_id: {f"{agent.agent_id}_{pawn_id}":1 for pawn_id in range(2)}
            for agent in self.agents
        }
        self.turn = 0
        self.winner = None
        self.dice = []
        self.cards = []  # Placeholder for Prime and Action cards
        self.game_log = []  # To store the sequence of moves and decisions
        self.card_manager = PrimeClimbCardManager(self)
        self.reverse_moves = {player: False for player in range(4)}
        self.skip_turns = {player: False for player in range(4)}
        # Initialize the board with pawns
        for team_id, pawn_data in self.pawns.items():
            for pawn_id, _ in pawn_data.items():  # We only need the pawn_id
                self.states[0]["board"][team_id] = pawn_id

    #def get_board_string(self):
        #board = self.states[-1]["board"]
        #row_strings = [", ".join(row) for row in board]
        #board_string = "-".join(row_strings)
        #return board_string

    def calculate_available_moves(self, agent_id):
        #print("agent_id is", agent_id)
        moves = []
        dice_rolls = self.dice
        my_pawns = self.pawns[agent_id]
        #print(my_pawns)

        for pawn_id, position in my_pawns.items():
            #print("pawn_id is", pawn_id)
            #print("position is ", position)
           # print("self.pawns[agent_id].items()", self.pawns[agent_id].items())

            for roll in dice_rolls:
                # Add and Subtract
                new_position_add = position + roll
                new_position_sub = position - roll
                if 1 <= new_position_add <= len_board:
                    moves.append((pawn_id, position, 'adding', roll))
                if 1 <= new_position_sub <= len_board:
                    moves.append((pawn_id, position, 'subtracting', roll))
                # Multiply
                new_position_mul = position * roll
                if 1 <= new_position_mul <= len_board:
                    moves.append((pawn_id, position, 'multiplying', roll))
                # Divide
                if roll != 0 and position % roll == 0:
                    new_position_div = position // roll
                    if 1 <= new_position_div <= len_board:
                        moves.append((pawn_id, position, 'dividing', roll))
        return moves

    def apply_move(self, agent_id, pawn_id, operation, roll):
        current_position = self.pawns[agent_id][pawn_id]
        if operation == "adding" or operation == 'prime_card' or operation == 'double_card':
            new_position = current_position + roll  # Directly add
        elif operation == "subtracting" or operation == 'reverse_card':
            new_position = current_position - roll  # Directly subtract
        elif operation == "multiplying":
            # Consider how multiplication should work for your game
            new_position = current_position * roll
        elif operation == "dividing" and roll != 0:
            if current_position != 0:
                # Consider how division should work for your game
                new_position = current_position // roll
            else:
                new_position = current_position
        else:
            new_position = current_position
        if 1 <= new_position <= len_board:
            print("BEFORE update:", self.states[-1]["board"])  # Print the board before
            # Update pawn position
            self.pawns[agent_id][pawn_id] = new_position
            # Mark the new position with the pawn's identifier
            self.states[-1]["board"][current_position-1] = "-"
            self.states[-1]["board"][new_position-1] = str(pawn_id)
            #print("AFTER update:", self.states[-1]["board"])  # Print the board after
        else:
            new_position = 2
            self.pawns[agent_id][pawn_id] = new_position
            self.states[-1]["board"][current_position-1] = "-"
            self.states[-1]["board"][new_position-1] = str(pawn_id)
            # Check for bump only if the move is valid
            self.check_bump(agent_id, pawn_id)

    def check_bump(self, active_player, active_pawn):
        print('BUMP function')
        active_pawn_position = self.pawns[active_player][active_pawn] -1
        for player, pawns in self.pawns.items():
            if player != active_player:  # Avoid checking the active player's own pawns
                for pawn_id, position in pawns.items():
                    if position -1 == active_pawn_position:  # If another pawn is on the same position
                        self.pawns[player][pawn_id] = 1  # Send the bumped pawn back to the start

    def check_win_condition(self):
        for player, pawns in self.pawns.items():
            if any(pos == len_board for pos in pawns.items()):  # Check if all pawns for the player are at position 101
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
        for pawn_idx, position, operation, dice_idx in move_decisions:
            if dice_idx < len(self.dice):
                self.apply_move(player, pawn_idx, operation, self.dice[dice_idx])
                self.game_log.append((player, position, pawn_idx, operation, self.dice[dice_idx]))
                if self.check_win_condition():
                    break
                # Draw and apply a card effect after the pawn moves
                card = self.card_manager.draw_card()
                if card:
                    print("pawn_idx in card handling:", pawn_idx)
                    self.card_manager.apply_card_effect(card, player, pawn_idx, self.dice[dice_idx])
                    self.card_manager.discard_card(card)  # Discard the card after using it
    def get_observation(self, agent: Agent) -> tuple[Observation, AvailableActions]:
        self.roll_dice()  # Roll dice at the beginning of each turn
        # Calculate available moves based on the current game state and dice rolls
        available_moves = self.calculate_available_moves(agent.agent_id)
        observation = Observation(text=f"{self.states[-1]['board']}")
        available_actions = AvailableActions(
            instructions="Select a pawn and an action (addition, subtraction, multiplication, division) based on your dice rolls.",
            predefined={
            },
           # openended={},
            #openended={"open": "use the rules to figure out a strategy to play"},

            openended={
                "draw_prime_card"  : "Draw a Prime Card if a pawn ends on a prime number space that was not occupied at the start of the turn.",
             #   "draw_action_card" : "Draw an Action Card and applies its effect immediately. Effects can range from moving pawns to affecting opponents.",
             #   "play_prime_card"  : "Plays an Action Card, modifying the game state as per the card's rules. Cannot be played in the turn it is drawn.",
                #"roll_the_dice": "Rolls two 10-sided dice. If doubles are rolled, the number can be used four times. The 0 represents 10.",
                # "move_pawn_add"     : "Move a pawn by adding the dice value to its current position. Each dice roll must be used separately.",
                # "move_pawn_subtract": "Move a pawn by subtracting the dice value from its current position. Each dice roll must be used separately.",
                # "move_pawn_multiply": "Move a pawn by multiplying its current position by the dice value. Each dice roll must be used separately.",
                # "move_pawn_divide"  : "Move a pawn by dividing its current position by the dice value. Only valid if the result is a whole number. Each dice roll must be used separately.",
              #  "check_bump": "Check if a pawn's new position results in bumping another pawn back to the start. Bumping is mandatory.",
              #  "check_win_condition": "Check if any player has won by getting both pawns to 101 exactly.",
            }
        )
        # Add the available moves to the available_actions object
        for move in available_moves:
            pawn_id, position, operation, roll = move
            if operation in ['adding', 'subtracting']:
                action_key = move
                action_description = f"Move your {pawn_id} pawn by {operation} the dice value {roll} to its current position ({position} on the board). Each dice roll must be used separately."
                available_actions.predefined[action_key] = action_description
            else:
                action_key = move
                action_description = f"Move a pawn by {operation} its current position ({position} on the board) with the dice value {roll}. Each dice roll must be used separately."
                available_actions.predefined[action_key] = action_description

        return observation, available_actions

    def update(self, action, available_actions, agent):
        for key_tuple in available_actions.predefined.keys():
            #print("available_actions.predefined keys are:", key_tuple)
            try:
                pawn_idx, position, operation, dice_idx = key_tuple
            except ValueError as e:
                print("Error parsing action_id:", e)
        # Apply the move
            if dice_idx < len(self.dice):
               # print("dice_idx:", dice_idx)
                #print("pawn_idx:", pawn_idx)
                move_decisions = [(pawn_idx, position, operation, dice_idx)]
                self.play_turn(agent.agent_id, move_decisions)
        # Check for win condition
        if self.check_win_condition():
            self.game_is_over = True
            self.winning_team = agent.team_id

    def roll_dice(self):
        roll1 = random.randint(0, 9)
        roll2 = random.randint(0, 9)
        self.dice = [10 if x == 0 else x for x in [roll1, roll2]]

    def play(self):
        player_1 = self.agents[0]
        player_2 = self.agents[1]

        self.game_is_over = False  # Ensure game state is properly initialized

        while not self.game_is_over:
            # Iterate through each player for their turn
            for player in (player_1, player_2):
                # Get the current state and available actions for the player
                observation, available_actions = self.get_observation(player)

                # Let the player take action based on the current state and available actions
                action = player.take_action(self.rules, observation, available_actions, show_state=self.show_state)

                if action.action_id not in available_actions.predefined and action.action_id not in available_actions.openended:
                    action = Action(action_id=random.choice(list(available_actions.predefined.keys())))
                self.update(action, available_actions, player)
                # Update the game state based on the action taken
                # Check if the game is over after the action is applied
                if self.game_is_over:
                    # Determine the outcome based on the winning team
                    # If there's no winning team, it's a draw (0.5, 0.5)
                    # If there is a winning team, set the score to (1, 0) or (0, 1) accordingly
                    outcome = (0.5, 0.5) if self.winning_team is None else \
                        (float(self.winning_team == player_1.team_id), float(self.winning_team == player_2.team_id))
                    return outcome
        # If the loop exits without finding a winner, return a draw (this should not happen with proper win condition checks)
        return (0.5, 0.5)
