from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyautogui
import pyperclip
import time
import os
import csv
from Deck import Deck
from Player import Player


def character_converter(card_name):
    if len(card_name) == 1:
        return card_name
    elif card_name == '10':
        return 'T'
    elif card_name == 'Dama':
        return 'Q'
    elif card_name == 'Walet':
        return 'J'
    else:
        return card_name[0]


def lin_file_creator(players):
    deck = Deck()
    deck.shuffle_deck()
    result = ""
    spades = "S"
    hearts = "H"
    diamonds = "D"
    clubs = "C"
    for player in players:
        player.add_cards_to_hand(deck.get_and_remove_cards_from_deck(13))
        for card in player.get_hand():
            if card.get_color() == "Pik":
                spades += character_converter(card.get_name())
            elif card.get_color() == "Kier":
                hearts += character_converter(card.get_name())
            elif card.get_color() == "Karo":
                diamonds += character_converter(card.get_name())
            elif card.get_color() == "Trefl":
                clubs += character_converter(card.get_name())
        result += spades + hearts + diamonds + clubs + ','
        spades = "S"
        hearts = "H"
        diamonds = "D"
        clubs = "C"
    return 'qx|o2|md|4' + result[:-1] + '|rh||ah||sv|n|pg||'


for i in range(1):
    playerS = Player('S')
    playerW = Player('W')
    playerN = Player('N')
    # playerE = Player('E')
    # players = [playerS, playerW, playerN, playerE]
    players = [playerS, playerW, playerN]
    result = lin_file_creator(players)
    with open('current_deal.lin', 'w') as file:
        file.write(result)
    result = result[10:63]

    DRIVER_PATH = 'https://mirgo2.co.uk/bridgesolver/upload.htm'
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(DRIVER_PATH)
    driver.maximize_window()
    driver.find_element(By.ID, "fileToUpload").send_keys(os.getcwd()+"/current_deal.lin")
    time.sleep(5)

    pyautogui.moveTo(160, 570)
    pyautogui.click()
    pyautogui.moveTo(565, 470)
    pyautogui.dragTo(780, 470, 1, button='left')
    pyautogui.hotkey('ctrl', 'c')

    analised_contracts = str(pyperclip.paste())
    analised_contracts = analised_contracts.strip()
    analised_contracts = analised_contracts.replace('\t', '')
    if analised_contracts[0] == 'N':
        analised_contracts = analised_contracts[1:]
    if len(analised_contracts) > 5 or analised_contracts == "*****" or len(analised_contracts) < 5:
        continue

    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # field = ["deal", "maximum_contracts"]
        # writer.writerow(field)
        writer.writerow([result, analised_contracts])
