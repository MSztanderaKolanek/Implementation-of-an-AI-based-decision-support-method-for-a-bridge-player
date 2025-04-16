from Deck import Deck
import random
from pandas import read_csv
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import numpy as np
from Agent import Agent
import pickle


colorama_init(autoreset=True)
TEXT_COLORS = dict(Fore.__dict__.items())

BIDS = ['1 Trefl', '1 Karo', '1 Kier', '1 Pik', '1 BA',
        '2 Trefl', '2 Karo', '2 Kier', '2 Pik', '2 BA',
        '3 Trefl', '3 Karo', '3 Kier', '3 Pik', '3 BA',
        '4 Trefl', '4 Karo', '4 Kier', '4 Pik', '4 BA',
        '5 Trefl', '5 Karo', '5 Kier', '5 Pik', '5 BA',
        '6 Trefl', '6 Karo', '6 Kier', '6 Pik', '6 BA',
        '7 Trefl', '7 Karo', '7 Kier', '7 Pik', '7 BA', 'pas']


class Bidding:

    def __init__(self, players, human_players=2, show_suggestions=False, show_max_bids=False, passEW=True):
        self.human_players = human_players
        self.playerN = players[0]
        self.playerE = players[1]
        self.playerS = players[2]
        self.playerW = players[3]
        self.show_suggestions = show_suggestions
        self.show_max_bids = show_max_bids
        self.passEW = passEW

    def terminal_information_printer(self, information_to_display, color=""):
        if not color:
            print(information_to_display)
        else:
            print(f"{TEXT_COLORS[color]}{information_to_display}{Style.RESET_ALL}")

    def terminal_answer_getter(self, information_to_display, choice_from, color=""):
        if not color:
            print(information_to_display)
        else:
            print(f"{TEXT_COLORS[color]}{information_to_display}{Style.RESET_ALL}")
        choice = input()
        choice = choice.lower().strip()
        if len(choice) == 4:
            choice = choice[:1] + ' ' + choice[2:4].upper()
        if len(choice) > 2:
            if choice != 'pas':
                choice = choice[:1] + ' ' + choice[2].upper() + choice[3:]
        while choice not in choice_from:
            if not color:
                print("Taki wybór nie jest dostępny. Spróbuj ponownie!")
            else:
                print(f"{TEXT_COLORS[color]}Taki wybór nie jest dostępny. Spróbuj ponownie!{Style.RESET_ALL}")
            choice = input()
        return choice

    def bidding_method(self, bidding_course, player, available_bids):
        points = player.calculate_points_and_colors()[0]
        # print(bidding_course)
        # print(points)
        colors = player.calculate_points_and_colors()[1]
        main_color = ''
        # jeżeli partner spasował lub alborytm zaczyna licytacje - mowisz swoje
        if not bidding_course or bidding_course[0] == 'pas':
            for color in list(colors.keys()):
                if colors[color] >= 6:
                    if points >= 16:
                        main_color = color
                        if f"1 {color}" in available_bids:
                            return f"2 {color}"
            for color in list(colors.keys()):
                if colors[color] >= 5:
                    if points >= 11:
                        main_color = color
                        if f"1 {color}" in available_bids:
                            return f"1 {color}"
            return "pas"
        else:
            # jeżeli partner nie spasował w pierwszym - algorytm potwierdza jeżeli może, jeśli nie mówi swoje
            # uwaga - bidding course ma tylko odzywki twoje i partnera
            if bidding_course:
                if bidding_course[0] != 'pas' and len(bidding_course) == 1:
                    # potwierdzenie koloru partnera z przeskokiem
                    if colors[bidding_course[0][2:]] == 4:
                        if points >= 12:
                            return f"{str(int(bidding_course[0][0]) + 2)} {bidding_course[0][2:]}"
                    # potwierdzenie koloru partnera bez przeskoku
                    if colors[bidding_course[0][2:]] == 3:
                        if points >= 8:
                            return f"{str(int(bidding_course[0][0]) + 1)} {bidding_course[0][2:]}"
            if not bidding_course or len(bidding_course) == 1:
                # licytowanie głownego koloru z przeskokiem
                main_color = 0
                for color in list(colors.keys()):
                    if colors[color] >= 6:
                        if points >= 16:
                            if main_color == 0:
                                main_color = color
                            else:
                                second_color = color
                            main_color = color
                            for i in range(7):
                                if f"{int(bidding_course[0][0]) + i} {color}" in available_bids:
                                    return f"{int(bidding_course[0][0]) + i + 1} {color}"
                # licytowanie głownego koloru bez przeskoku
                for color in list(colors.keys()):
                    if colors[color] >= 5:
                        if points >= 11:
                            main_color = color
                            for i in range(7):
                                if f"{int(bidding_course[0][0]) + i} {color}" in available_bids:
                                    return f"{int(bidding_course[0][0]) + i} {color}"
            return "pas"

    def lin_format_cards_add_handler(self, coded_cards, deck):
        coded_cards = coded_cards.replace('S', '')
        cards_to_add = []
        current_names = []
        current_color = ['Pik', 'Kier', 'Karo', 'Trefl']
        for char in coded_cards:
            # print(char)
            if char not in ['D', 'H', 'C']:
                if char == 'A':
                    char = "As"
                elif char == 'K':
                    char = "Król"
                elif char == 'Q':
                    char = "Dama"
                elif char == 'J':
                    char = "Walet"
                elif char == 'T':
                    char = "10"
                current_names.append(char)
            else:
                cards_to_add.extend(deck.get_and_remove_specific_cards_from_deck(current_names, current_color[0]))
                current_color.pop(0)
                current_names = []
        cards_to_add.extend(deck.get_and_remove_specific_cards_from_deck(current_names, current_color[0]))
        return cards_to_add

    def get_current_legal_actions(self, current_bids_order):
        current_bids = ['1 Trefl', '1 Karo', '1 Kier', '1 Pik', '1 BA']
        colors = ['Trefl', 'Karo', 'Kier', 'Pik', 'BA']
        if not current_bids_order:
            current_bids.append('pas')
            return current_bids
        else:
            color_index = colors.index(current_bids_order[-1][2:])
            for j in range(len(current_bids)):
                current_bids[j] = current_bids_order[-1][0] + current_bids[j][1:]
            for i in range(color_index + 1):
                current_bids[i] = str(int(current_bids_order[-1][0]) + 1) + current_bids[i][1:]

        for z in range(5):
            if current_bids[z][0] == '8':
                current_bids[z] = 'pas'
        current_bids.append('pas')
        return current_bids

    def bidding(self):
        # UWAGA bidding_course zawiera tylko odzywki licytujacego i partnera

        agent = Agent()
        with open(f"../model2", 'rb') as f:
            weights, episode = pickle.load(f)
        # rozdanie kart
        deck = Deck()
        if self.show_max_bids:
            data = read_csv("../data.csv")
            random_deal = random.randint(1, 5000)
            current_coded_hands = data['deal'][random_deal].split(',')
            current_max_bids = data['maximum_contracts'][random_deal]

            self.playerS.add_cards_to_hand(self.lin_format_cards_add_handler(current_coded_hands[0], deck))
            self.playerW.add_cards_to_hand(self.lin_format_cards_add_handler(current_coded_hands[1], deck))
            self.playerN.add_cards_to_hand(self.lin_format_cards_add_handler(current_coded_hands[2], deck))
            self.playerE.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))
        else:
            deck.shuffle_deck()
            self.playerN.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))
            self.playerE.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))
            self.playerS.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))
            self.playerW.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))

        players = [self.playerN, self.playerE, self.playerS, self.playerW]
        available_bids = BIDS.copy()
        counter = 0
        passes = 0
        bid = ''
        someone_did_bid = False
        bids_order = []
        bidding_state = "Nikt nie zalicytował"
        current_color = ""

        if self.human_players == 2:
            self.playerN.change_to_human()
            self.playerS.change_to_human()
        elif self.human_players == 1:
            self.playerN.change_to_human()
            self.playerS.change_to_computer('algorithm')
        self.terminal_information_printer("Rozpoczyna się licytacja", color="BLUE")
        self.terminal_information_printer("-"*30, color="BLUE")
        while True:
            current_player = players[counter]
            if current_player == self.playerE or current_player == self.playerW:
                current_text_color = 'BLUE'
            elif not current_player.get_is_computer():
                current_text_color = 'GREEN'
            else:
                current_text_color = 'RED'
            self.terminal_information_printer(f"Obecny stan licytacji: {bidding_state}", current_text_color)
            self.terminal_information_printer(f"Licytuje gracz: {current_player.get_name()}", current_text_color)
            if self.passEW:
                if current_player == self.playerE or current_player == self.playerW:
                    self.terminal_information_printer("Co licytujesz? (1-7 Trefl,Karo,Kier,Pik,BA / pas)", current_text_color)
                    self.terminal_information_printer("pas", current_text_color)
                    bid = 'pas'
                else:
                    if not current_player.get_is_computer():
                        self.terminal_information_printer("-" * 30, current_text_color)
                        self.terminal_information_printer("Karty na ręce:", current_text_color)
                        current_player.show_hand(current_text_color)
                        self.terminal_information_printer("-" * 30, current_text_color)

                        # TODO random bid
                        if self.show_suggestions:
                            q_values = [np.dot(weights.T, agent.get_feature_vector(
                                current_player, bids_order, False, bid))
                                        for bid in self.get_current_legal_actions(bids_order)]
                            bid_index = np.argmax(q_values)
                            suggest_bid = self.get_current_legal_actions(bids_order)[bid_index]
                            self.terminal_information_printer(f"Sugestia systemu: licytuj {suggest_bid}", current_text_color)

                        bid = self.terminal_answer_getter(
                            "Co licytujesz? (1-7 Trefl,Karo,Kier,Pik,BA / pas)", available_bids, current_text_color)
                    else:
                        if current_player.get_computer_type() == 'random':
                            self.terminal_information_printer("Co licytujesz? (1-7 Trefl,Karo,Kier,Pik,BA / pas)", current_text_color)
                            bid = random.choice(available_bids)
                            self.terminal_information_printer(f"{bid}", current_text_color)
                        elif current_player.get_computer_type() == 'bidding_method':
                            self.terminal_information_printer("Co licytujesz? (1-7 Trefl,Karo,Kier,Pik,BA / pas)", current_text_color)
                            bid = self.bidding_method(bids_order, current_player, available_bids)
                            self.terminal_information_printer(f"{bid}", current_text_color)
                        elif current_player.get_computer_type() == 'algorithm':
                            q_values = [np.dot(weights.T, agent.get_feature_vector(
                                current_player, bids_order, False, bid))
                                        for bid in self.get_current_legal_actions(bids_order)]
                            bid_index = np.argmax(q_values)
                            bid = self.get_current_legal_actions(bids_order)[bid_index]
                            self.terminal_information_printer("Co licytujesz? (1-7 Trefl,Karo,Kier,Pik,BA / pas)",
                                                              current_text_color)
                            self.terminal_information_printer(f"{bid}", current_text_color)
                if bid == "pas":
                    passes += 1
                else:
                    someone_did_bid = True
                    passes = 0
                    bids_order.append(bid)
                    bidding_state = f"{current_player.get_name()} zalicytował {bid}"
                    for _ in range(available_bids.index(bid) + 1):
                        available_bids.pop(0)
            print()
            if someone_did_bid:
                if passes == 3:
                    break
            else:
                if passes == 4:
                    break
            counter += 1
            if counter > 3:
                counter = 0
        if bidding_state == "Nikt nie zalicytował":
            self.terminal_information_printer(f"Licytacja zakończona: {bidding_state}", 'BLUE')
        else:
            self.terminal_information_printer(f"Licytacja zakończona: {bidding_state}, a pozostali gracze spasowali", 'BLUE')
        self.terminal_information_printer("-"*30, 'BLUE')
        self.terminal_information_printer("Ręce wszystkich graczy: ", 'BLUE')
        for player in players:
            if player == self.playerE or player == self.playerW:
                self.terminal_information_printer(f"Gracz {player.get_name()}: ", 'BLUE')
                player.show_hand('BLUE')
            elif player.get_is_computer():
                self.terminal_information_printer(f"Gracz {player.get_name()}: ", 'RED')
                player.show_hand('RED')
            else:
                self.terminal_information_printer(f"Gracz {player.get_name()}: ", 'GREEN')
                player.show_hand('GREEN')

        if self.show_max_bids:
            self.terminal_information_printer("-" * 30, 'BLUE')
            for i, color in enumerate(['treflu', 'karo', 'kierze', 'piku', 'bez atu']):
                self.terminal_information_printer(
                    f"Maksymalny możliwy do wygrania kontrakt w {color}: {current_max_bids[i]}", 'BLUE')
            if bidding_state == "Nikt nie zalicytował":
                self.terminal_information_printer(f"Wylicytowany kontrakt to -", 'BLUE')
            elif bidding_state.split('zalicytował')[1][3:] == 'BA':
                self.terminal_information_printer(
                    f"Wylicytowany kontrakt to{bidding_state.split('zalicytował')[1][:2]} bez atu", 'BLUE')
            else:
                self.terminal_information_printer(f"Wylicytowany kontrakt to{bidding_state.split('zalicytował')[1]}", 'BLUE')
