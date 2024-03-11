class Agent:

    @staticmethod
    def get_feature_vector_length():
        return 3

    @staticmethod
    def get_feature_vector(player, bidding_order, is_first, action):
        """
        points_in_current_color
        length_of_current_color
        height_of_bid
        :return: vector of features
        """

        colors = {'Trefl': 0, 'Karo': 0, 'Kier': 0, 'Pik': 0}
        if is_first:
            if bidding_order:
                for i in range(int(len(bidding_order) / 2)):
                    color = bidding_order[2*i+1][2:]
                    colors[color] = 1
        else:
            for i in range(int((len(bidding_order) / 2) + 1)):
                # print(bidding_order[2*i][2:])
                try:
                    color = bidding_order[2*i][2:]
                    colors[color] = 1
                except IndexError:
                    pass

        points, cards_in_colors = player.calculate_points_and_colors()
        points_in_colors = player.calculate_points_in_colors()
        height_of_bid = 0
        if action != 'pas':
            if points >= 22:
                if action[0] == '4':
                    height_of_bid = 50
            if points >= 18:
                if action[0] == '2':
                    height_of_bid = 40
            if points >= 14:
                if action[0] == '2':
                    height_of_bid = 30
            if points >= 10:
                if action[0] == '1':
                    height_of_bid = 20
            if action[2:] != 'BA':
                points_in_current_color = points_in_colors[action[2:]]
                length_of_current_color = cards_in_colors[action[2:]] * 2
            else:
                points_in_current_color = min(points_in_colors['Trefl'], points_in_colors['Karo'],
                                              points_in_colors['Kier'], points_in_colors['Pik']) * 4
                length_of_current_color = min(cards_in_colors['Trefl'], cards_in_colors['Karo'],
                                              cards_in_colors['Kier'], cards_in_colors['Pik']) * 3

        else:
            points_in_current_color = 0
            length_of_current_color = 0
            height_of_bid = 0
        return points_in_current_color, length_of_current_color, height_of_bid
