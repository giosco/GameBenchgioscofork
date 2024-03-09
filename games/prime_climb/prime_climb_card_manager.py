import random

class PrimeClimbCardManager:
    def __init__(self, game_state):
        self.deck = self.initialize_deck()
        self.discard_pile = []
        self.game_state = game_state

    def initialize_deck(self):
        # Initialize a new deck of cards for the game
        cards = [
            {"name": "Double Move", "type": "action"},
            {"name": "Prime Move", "type": "action"},
            {"name": "Reverse", "type": "action"},
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

    def apply_card_effect(self,card, player, pawn_idx, dice_roll):
        # Apply the effect of the drawn card to the game state
        print(f"Player {player} drew a {card['type']} card: {card['name']}")
        if card["name"] == "double_card":
            for _ in range(2):  # Repeat twice
                self.game_state.apply_move(player, pawn_idx, 'adding', dice_roll)
            print(f"Player {player} uses Double Move with a roll of {dice_roll}.")
        elif card["name"] == "prime_card":
                next_prime = self.find_next_prime(self.pawns[player][pawn_idx])
                self.game_state.apply_move(player, pawn_idx, 'prime_card', next_prime)
                print(f"After Prime Move - Player {player}'s Pawn {pawn_idx} moves to next prime number {next_prime}")
        elif card["name"] == "reverse_card":
            current_team = player // 2  # Assuming teams of two, find the player's team
            other_team = (current_team + 1) % 2  # Find the other team (with modulo 2)
            next_player = other_team * 2 + (player + 1) % 2  # Get the opposing player within the other team
            self.game_state.apply_move(next_player, pawn_idx, 'prime_card', dice_roll)
            print(f"Player {player} plays Reverse on player {next_player}.")

    def find_next_prime(self, current_position, max_limit=101):
        # This is a helper function to find the next prime number on the board
        def is_prime(num):
            if num < 2:
                return False
            for n in range(2, int(num ** 0.5) + 1):
                if num % n == 0:
                    return False
            return True
        print('current position for prime function',current_position)
        next_position = current_position + 1
        while next_position <= max_limit:
            if is_prime(next_position):
                return next_position
            next_position += 1
        print("No next prime found within the board limit.")  # Debugging statement
        return current_position  # Return the current position if no prime is found

    def discard_card(self, card):
        # Add the used card to the discard pile
        self.discard_pile.append(card)
