from Player import Player
from Bidding import Bidding
from colorama import init as colorama_init


colorama_init(autoreset=True)

Player_1 = Player("N")
Player_2 = Player("E")
Player_3 = Player("S", is_computer=True, computer_type='algorithm')
Player_4 = Player("W")

with open('../configuration.txt', 'r', encoding='utf-8') as file:
    current_configuration = file.readlines()
    human_players, suggestions, max_bids = [conf.strip().lower().split(' - ')[1] for conf in current_configuration]
    if human_players not in ['1', '2'] or suggestions not in ['tak', 'nie'] or max_bids not in ['tak', 'nie']:
        print("Niepoprawna konfiguracja. Sprawdź plik konfiguracyjny!")
        exit()
    else:
        if suggestions == 'tak':
            suggestions = True
        else:
            suggestions = False
        if max_bids == 'tak':
            max_bids = True
        else:
            max_bids = False
        human_players = int(human_players)
bidding = Bidding([Player_1, Player_2, Player_3, Player_4],
                  human_players=human_players,
                  show_suggestions=suggestions,
                  show_max_bids=max_bids)
bidding.bidding()
