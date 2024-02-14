import random

class PrimeClimbCardManager:
    def __init__(self):
        self.deck = self.initialize_deck()
        self.discard_pile = []

    def initialize_deck(self):
        # Initialize a new deck of cards for the game
        cards = [
            {"name": "Double Move", "type": "keeper"},
            {"name": "Prime Move", "type": "action"},
            {"name": "Reverse", "type": "action"},
            {"name": "Skip", "type": "action"}
        ]
        random.shuffle(cards)
        return cards

    def draw_card(self):
        # If the deck is empty, reshuffle the discard pile into the deck
        if not self.deck:
            self.deck, self.discard_pile = self.discard_pile, []
            random.shuffle(self.deck)
        # Now that we've ensured the deck is not empty, safely draw a card
        if self.deck:  # Check if the deck is still not empty after reshuffling
            return self.deck.pop()
        else:
            # Handle the case when both the deck and discard pile are empty
            print("No more cards to draw.")
            return None  # Or return a special value that indicates no card could be drawn

    def apply_card_effect(self, card, game_state, player):
        # Apply the effect of the drawn card to the game state
        print(f"Player {player} drew a {card['type']} card: {card['name']}")
        if card["name"] == "Double Move":
            # The player can choose the first die roll to use twice for a single pawn move
            # Let's assume the player chooses the first dice roll for simplicity
            dice_roll_index = 0  # or 1 for the second dice roll
            if dice_roll_index < len(game_state.dice):
                dice_roll = game_state.dice[dice_roll_index]
                # Apply the dice roll twice to a chosen pawn
                chosen_pawn = 0  # Assuming the player chooses the first pawn
                game_state.apply_move(player, chosen_pawn, 'add', dice_roll)
                game_state.apply_move(player, chosen_pawn, 'add', dice_roll)
                print(f"Player {player} uses Double Move with a roll of {dice_roll}.")
            else:
                print(f"No dice roll available for Double Move for player {player}.")
        elif card["name"] == "Prime Move":
            # Moves a pawn to the next prime number on the board
            print(f"Player: {player}, Pawns: {game_state.pawns[player]}")
            for pawn_id, pawn_position in game_state.pawns[player].items():
                print(f"Before Prime Move - Player {player}'s Pawn {pawn_id} at position {pawn_position}")
                next_prime = self.find_next_prime(pawn_position)
                game_state.pawns[player][pawn_id] = next_prime
                print(f"After Prime Move - Player {player}'s Pawn {pawn_id} moves to next prime number {next_prime}")
        elif card["name"] == "Reverse":
            # Reverses the direction of the next player's pawn move
            next_player = (player + 1) % len(game_state.pawns)
            game_state.reverse_moves[next_player] = True
            print(f"Player {player} plays Reverse on player {next_player}.")
        elif card["name"] == "Skip":
            # Skips the next player's turn
            next_player = (player + 1) % len(game_state.pawns)
            game_state.skip_turns[next_player] = True
            print(f"Player {player} skips player {next_player}'s turn.")

    def find_next_prime(self, current_position, max_limit=101):
        # This is a helper function to find the next prime number on the board
        def is_prime(num):
            if num < 2:
                return False
            for n in range(2, int(num ** 0.5) + 1):
                if num % n == 0:
                    return False
            return True
        next_position = current_position + 1
        while next_position <= max_limit:
            if is_prime(next_position):
                return next_position
            next_position += 1
            print(f"Checking next position: {next_position}")  # Debugging statement

        print("No next prime found within the board limit.")  # Debugging statement
        return current_position  # Return the current position if no prime is found

    def discard_card(self, card):
        # Add the used card to the discard pile
        self.discard_pile.append(card)
