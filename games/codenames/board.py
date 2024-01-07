# board for codenames game
from card import Card, CardType
import config
import random

class Board:
    @staticmethod
    def cards_from_words(words, first_team: CardType, second_team: CardType):
        total_cards = config.FIRST_TEAM_CARDS + config.SECOND_TEAM_CARDS + config.ASSASSIN_CARDS + config.NEUTRAL_CARDS
        if len(words) != total_cards:
            raise ValueError("Wrong number of words for board")
        
        cards = []
        for word in words:
            cards.append(Card(word, CardType.NEUTRAL))

        random.shuffle(cards)
        # place first team cards
        cards[0:config.FIRST_TEAM_CARDS] = [Card(word, first_team) for word in words[0:config.FIRST_TEAM_CARDS]]
        # place second team cards
        cards[config.FIRST_TEAM_CARDS:config.FIRST_TEAM_CARDS + config.SECOND_TEAM_CARDS] = [Card(word, second_team) for word in words[config.FIRST_TEAM_CARDS:config.FIRST_TEAM_CARDS + config.SECOND_TEAM_CARDS]]
        # place assassin card
        cards[config.FIRST_TEAM_CARDS + config.SECOND_TEAM_CARDS] = Card(words[config.FIRST_TEAM_CARDS + config.SECOND_TEAM_CARDS], CardType.ASSASSIN)        
        random.shuffle(cards)
        return cards
        
    def __init__(self, words, game_config):
        num_cards = game_config.FIRST_TEAM_CARDS + game_config.SECOND_TEAM_CARDS + game_config.ASSASSIN_CARDS + game_config.NEUTRAL_CARDS
        random_words = random.sample(words, num_cards)
        self.cards = Board.cards_from_words(random_words, CardType.RED, CardType.BLUE)
        self.revealed = [False for _ in self.cards]
        self.current_turn = CardType.RED

    def team_turn(self):
        return self.current_turn
    

    def end_turn(self):
        if self.current_turn == CardType.RED:
            self.current_turn = CardType.BLUE
        else:
            self.current_turn = CardType.RED

    def winner(self):
        red_cards = 0
        blue_cards = 0
        for index, card in enumerate(self.cards):
            if self.revealed[index]:
                if card.card_type == CardType.RED:
                    red_cards += 1
                elif card.card_type == CardType.BLUE:
                    blue_cards += 1
        if red_cards == config.FIRST_TEAM_CARDS:
            return CardType.RED
        elif blue_cards == config.SECOND_TEAM_CARDS:
            return CardType.BLUE
        else:
            return None
        
    def reveal_card(self, index):
        if self.revealed[index]:
            raise ValueError("Card already revealed")
        self.revealed[index] = True
        return self.cards[index].card_type
    

    

