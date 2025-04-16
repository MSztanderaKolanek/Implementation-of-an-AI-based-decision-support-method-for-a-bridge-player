from scripts.Player import Player
from scripts.Deck import Deck
from scripts.Agent import Agent
import numpy as np
import pickle
import os
from pandas import *
import random


BIDS = ['1 Trefl', '1 Karo', '1 Kier', '1 Pik', '1 BA',
        '2 Trefl', '2 Karo', '2 Kier', '2 Pik', '2 BA',
        '3 Trefl', '3 Karo', '3 Kier', '3 Pik', '3 BA',
        '4 Trefl', '4 Karo', '4 Kier', '4 Pik', '4 BA',
        '5 Trefl', '5 Karo', '5 Kier', '5 Pik', '5 BA',
        '6 Trefl', '6 Karo', '6 Kier', '6 Pik', '6 BA',
        '7 Trefl', '7 Karo', '7 Kier', '7 Pik', '7 BA', 'pas']

BASIC_BIDS = ['Trefl', 'Karo', 'Kier', 'Pik', 'BA', 'pas']


class Learning:

    def __init__(self, players, human_players=2, passEW=True):
        self.human_players = human_players
        self.playerN = players[0]
        self.playerE = players[1]
        self.playerS = players[2]
        self.playerW = players[3]
        self.passEW = passEW

    def terminal_information_printer(self, information_to_display):
        print(information_to_display)

    def terminal_answer_getter(self, information_to_display, choice_from):
        print(information_to_display)
        choice = input()
        while choice not in choice_from:
            print("Taki wybór nie jest dostępny. Spróbuj ponownie!")
            choice = input()
        return choice

    def lin_format_cards_add_handler(self, coded_cards, deck):
        coded_cards = coded_cards.replace('S', '')
        cards_to_add = []
        current_names = []
        current_color = ['Pik', 'Kier', 'Karo', 'Trefl']
        for char in coded_cards:
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

    def bidding_method(self, bidding_course, player, available_bids):
        points = 0
        colors = {}
        points = player.calculate_points_and_colors()[0]
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
            if bidding_course:
                if bidding_course[-1][2:] == 'BA':
                    return 'pas'
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

    def check_reward(self, episode_number, current_bid, max_bids, bidding_order):
        reward = 0
        colors = ['Trefl', 'Karo', 'Kier', 'Pik', 'BA']
        current_colors = []
        if current_bid == 'pas':
            reward = -1 * (20 - len(bidding_order))
            return reward
        else:
            max_bids = list(max_bids.replace('-', '0'))
            if int(current_bid[0]) <= int(max(max_bids)):
                for i, max_bid in enumerate(range(len(max_bids))):
                    if max_bid == max(max_bids):
                        current_colors.append(colors[i])
                if current_bid[2:] in current_colors:
                    reward = 10
                    return reward
                else:
                    reward = 0
                    return reward
            else:
                reward = -1*(int(current_bid[0]) - int(max(max_bids)))
                return reward

    def learning_bidding(self, episodes, gamma, testing, learning_rate, save, learn):
        agent1 = Agent()
        agent2 = Agent()

        if testing:
            pass
        for i in range(2):   # 2 - tyle jest graczy komputerowych, uczących się
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if learn:
                if i == 0:
                    weights1 = np.array([np.random.uniform(-0.1, 0.1)
                                         for _ in range(agent1.get_feature_vector_length())])
                else:
                    weights2 = np.array([np.random.uniform(-0.1, 0.1)
                                         for _ in range(agent2.get_feature_vector_length())])

            elif os.path.isfile(os.path.join(base_dir, f"model{i + 1}")):
                with open(os.path.join(base_dir, f"model{i + 1}"), 'rb') as f:
                    if i == 0:
                        weights1, episode1 = pickle.load(f)
                    else:
                        weights2, episode2 = pickle.load(f)
            else:
                print("Error - no models!")
                exit()

        for i, episode in enumerate(range(episodes)):
            data = read_csv("../test.csv")
            current_coded_hands = data['deal'][i].split(',')
            current_max_bids = data['maximum_contracts'][i]
            deck = Deck()
            self.playerS.add_cards_to_hand(self.lin_format_cards_add_handler(current_coded_hands[0], deck))
            self.playerW.add_cards_to_hand(self.lin_format_cards_add_handler(current_coded_hands[1], deck))
            self.playerN.add_cards_to_hand(self.lin_format_cards_add_handler(current_coded_hands[2], deck))
            self.playerE.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))
            players = [self.playerN, self.playerE, self.playerS, self.playerW]

            agents = [agent1, agent2]
            weights = [weights1, weights2]

            available_bids = BIDS.copy()
            model_bids = BASIC_BIDS.copy()
            counter = 0
            passes = 0
            bid = ''
            someone_did_bid = False
            bids_order = []
            bidding_state = "Nikt nie zalicytował"
            game_end = False

            while not game_end:
                current_player = players[counter]
                current_agent = agents[int(counter/2)]
                current_weights = weights[int(counter/2)]
                is_player_first = True
                if counter > 1:
                    is_player_first = False
                if self.passEW:
                    if current_player == self.playerE or current_player == self.playerW:
                        bid = 'pas'
                    else:
                        if current_player.get_computer_type() == "bidding_method":
                            bid = self.bidding_method(bids_order, current_player, available_bids)
                        else:
                            q_values = [np.dot(current_weights.T, current_agent.get_feature_vector(current_player, bids_order, is_player_first, bid)) for bid in available_bids]
                            print()
                            print(f"wartośći q: {q_values}")
                            print(f"wartośći w: {current_weights}")
                            bid_index = np.argmax(q_values)
                            bid = available_bids[bid_index]

                            feature_vector = current_agent.get_feature_vector(current_player, bids_order, is_player_first, bid)
                            reward = self.check_reward(i, bid, current_max_bids, bids_order)

                            q_value = np.dot(current_weights.T, feature_vector)
                            if game_end:
                                target_q = reward
                            else:
                                max_q = max([np.dot(current_weights.T, feature_vector) for _ in self.get_current_legal_actions(bids_order)])
                                target_q = reward + gamma * max_q

                            error = target_q - q_value
                            # Update weights
                            for j in range(len(current_weights)):
                                current_weights[j] += learning_rate * error * feature_vector[j]
                if bid == "pas":
                    passes += 1
                else:
                    someone_did_bid = True
                    passes = 0
                    bids_order.append(bid)
                    bidding_state = f"{current_player.get_name()} zalicytował {bid}"
                    for _ in range(available_bids.index(bid) + 1):
                        available_bids.pop(0)

                if someone_did_bid:
                    if passes == 3:
                        game_end = True
                        break
                else:
                    if passes == 4:
                        game_end = True
                        break
                counter += 1
                if counter > 3:
                    counter = 0

            for player in players:
                player.empty_hand()
            if bidding_state == "Nikt nie zalicytował":
                self.terminal_information_printer(f"Licytacja zakończona: {bidding_state}")
            else:
                self.terminal_information_printer(f"Licytacja zakończona: {bidding_state}, a pozostali gracze spasowali")

            print(f"Episode: {episode}, Bids history: {bids_order}")
            print(f"Episode: {episode}, Weights: {current_weights}")
            for i in range(2):   # computer players = 2
                if save:
                    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    with open(os.path.join(base_dir, f"model{i + 1}"), "wb") as f:
                        data = (weights[i], episode)
                        pickle.dump(data, f)
            if testing:
                pass
        return 0


Player_1 = Player("N")
Player_2 = Player("E")
Player_3 = Player("S")
Player_4 = Player("W")
learning1 = Learning([Player_1, Player_2, Player_3, Player_4])
# learn -> czy wagi losowe czy wczytane
learning1.learning_bidding(episodes=500, gamma=0.5,
                           testing=True, learning_rate=0.0005,
                           save=False, learn=False)
