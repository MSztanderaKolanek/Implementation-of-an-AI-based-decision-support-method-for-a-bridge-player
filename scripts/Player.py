from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init(autoreset=True)
TEXT_COLORS = dict(Fore.__dict__.items())


class Player:

    def __init__(self, name, is_computer=False, computer_type=None):
        self.name = name
        self.is_computer = is_computer
        self.hand = []
        self.taken_cards = []
        self.computer_type = computer_type
        self.next_player = None

    def order_hand(self):
        order_hand = []
        card_names = ('As', 'Król', 'Dama', 'Walet', '10', '9', '8', '7', '6', '5', '4', '3', '2')
        # TODO tutaj dokonano zmiany - kolory były od trefla do pika (na odwrót)
        card_colors = ('Pik', 'Kier', 'Karo', 'Trefl')
        for col in card_colors:
            for nam in card_names:
                for card in self.hand:
                    if card.get_name() == nam and card.get_color() == col:
                        order_hand.append(card)
        self.hand = order_hand

    def add_cards_to_hand(self, cards):
        for card in cards:
            self.hand.append(card)
        self.order_hand()

    def add_taken_cards(self, cards):
        for card in cards:
            self.taken_cards.append(card)

    def remove_and_get_card_by_index(self, card_index):
        card = self.hand.pop(card_index)
        return card

    def calculate_points_in_colors(self):
        # caclulating how many points there are in each color
        colors_and_points = {'Trefl': 0, 'Karo': 0, 'Kier': 0, 'Pik': 0}
        for card in self.hand:
            for color in colors_and_points.keys():
                if card.get_color() == color:
                    if card.name == 'As':
                        colors_and_points[color] += 4
                    elif card.get_name() == 'Król':
                        colors_and_points[color] += 3
                    elif card.get_name() == 'Dama':
                        colors_and_points[color] += 2
                    elif card.get_name() == 'Walet':
                        colors_and_points[color] += 1
        return colors_and_points

    def calculate_points_and_colors(self):
        points = 0
        clubs = 0
        diamonds = 0
        hearts = 0
        spades = 0
        for card in self.hand:
            if card.name == 'As':
                points += 4
            elif card.get_name() == 'Król':
                points += 3
            elif card.get_name() == 'Dama':
                points += 2
            elif card.get_name() == 'Walet':
                points += 1
            if card.get_color() == 'Trefl':
                clubs += 1
            elif card.get_color() == 'Karo':
                diamonds += 1
            elif card.get_color() == 'Kier':
                hearts += 1
            elif card.get_color() == 'Pik':
                spades += 1
        if clubs < 3:
            if clubs == 2:
                points += 1
                for card in self.hand:
                    if card.get_color() == "Trefl":
                        if card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif clubs == 1:
                points += 2
                for card in self.hand:
                    if card.get_color() == "Trefl":
                        if card.get_name() == 'Król':
                            points -= 3
                        elif card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif clubs == 0:
                points += 3
        if diamonds < 3:
            if diamonds == 2:
                points += 1
                for card in self.hand:
                    if card.get_color() == "Karo":
                        if card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif diamonds == 1:
                points += 2
                for card in self.hand:
                    if card.get_color() == "Karo":
                        if card.get_name() == 'Król':
                            points -= 3
                        elif card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif diamonds == 0:
                points += 3
        if hearts < 3:
            if hearts == 2:
                points += 1
                for card in self.hand:
                    if card.get_color() == "Kier":
                        if card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif hearts == 1:
                points += 2
                for card in self.hand:
                    if card.get_color() == "Kier":
                        if card.get_name() == 'Król':
                            points -= 3
                        elif card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif hearts == 0:
                points += 3
        if spades < 3:
            if spades == 2:
                points += 1
                for card in self.hand:
                    if card.get_color() == "Pik":
                        if card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif spades == 1:
                points += 2
                for card in self.hand:
                    if card.get_color() == "Pik":
                        if card.get_name() == 'Król':
                            points -= 3
                        elif card.get_name() == 'Dama':
                            points -= 2
                        elif card.get_name() == 'Walet':
                            points -= 1
            elif spades == 0:
                points += 3
        return points, {'Trefl': clubs, 'Karo': diamonds, 'Kier': hearts, 'Pik': spades}

    def change_to_human(self):
        self.is_computer = False

    def change_to_computer(self, comp_type):
        self.is_computer = True
        self.computer_type = comp_type

    def get_hand(self):
        return self.hand

    def add_next_player(self, player):
        self.next_player = player

    def get_next_player(self):
        return self.next_player

    def get_name(self):
        return self.name

    def get_taken_cards(self):
        return self.taken_cards

    def get_is_computer(self):
        return self.is_computer

    def get_computer_type(self):
        return self.computer_type

    def empty_hand(self):
        self.hand = []

    def show_hand(self, color):
        card_colors = ('Trefl', 'Karo', 'Kier', 'Pik')
        card_colors_with_spaces = ('Trefl', 'Karo ', 'Kier ', 'Pik  ')
        current_color = []
        for col in card_colors:
            for card in self.hand:
                if card.get_color() == col:
                    current_color.append(card)
            if len(col) == 4:
                col += ' '
            elif len(col) == 3:
                col += '  '
            print(f"{TEXT_COLORS[color]}{col}: {[card.get_name() for card in current_color]}{Style.RESET_ALL}")
            current_color = []
