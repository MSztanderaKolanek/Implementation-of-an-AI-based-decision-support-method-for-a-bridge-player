from scripts.Card import Card
import random


CARD_NAMES = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Walet', 'Dama', 'Król', 'As')
CARD_COLORS = ('Trefl', 'Karo', 'Kier', 'Pik')
CARD_VALUES = tuple([i for i in range(1, 53)])


class Deck:

    def __init__(self, names=CARD_NAMES, colors=CARD_COLORS, values=CARD_VALUES):
        self.deck = []
        val = 0
        for nam in names:
            for col in colors:
                self.deck.append(Card(col, values[val], nam))
            val += 1

    def print_deck(self):
        for card in self.deck:
            print(card.get_card())

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def sort_deck(self, card_names, card_colors, card_values):
        # creates new deck instead of sorting previous one
        # possible change - create dictionary with names and their values instead of separate lists
        self.deck = []
        val = 0
        for nam in card_names:
            for col in card_colors:
                self.deck.append(Card(col, card_values[val], nam))
            val += 1

    def get_and_remove_cards_from_deck(self, number_of_cards_to_remove):
        # if deck is shuffled previously, there is no reason in choosing random cards to remove (but ok)
        cards_removed = []
        for _ in range(number_of_cards_to_remove):
            cards_removed.append(self.deck.pop(random.randrange(0, len(self.deck))))
        return cards_removed

    def get_and_remove_specific_cards_from_deck(self, names, color):
        cards_removed = []
        for name in names:
            for i, card in enumerate(self.deck):
                if card.get_name() == name and card.get_color() == color:
                    cards_removed.append(self.deck.pop(i))
        return cards_removed

    def get_deck(self):
        return self.deck
