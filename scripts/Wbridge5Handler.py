import pyautogui
import time
import csv
from pandas import *


make_deal = False
coded_deals_and_max_bids = read_csv("../test.csv")
coded_deals = coded_deals_and_max_bids['deal']
max_contracts = coded_deals_and_max_bids['maximum_contracts']
if make_deal:
    for k in range(0):
        with open('../current_Wbridge5_deal.lin', 'w') as file:
            current_lin = 'qx|o2|md|4' + coded_deals_and_max_bids['deal'][k] + '|rh||ah||nv|n|pg||'
            file.write(current_lin)

        pyautogui.moveTo(580, 275)
        pyautogui.click()
        pyautogui.moveTo(580, 365)
        pyautogui.click()
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(0.5)
        pyautogui.hotkey('enter')
        pyautogui.moveTo(580, 275)
        pyautogui.click()
        pyautogui.moveTo(580, 435)
        pyautogui.click()
        pyautogui.hotkey('enter')
        pyautogui.moveTo(1315, 295)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.hotkey('enter')
        for i in range(10):
            time.sleep(2)
            pyautogui.moveTo(1090, 518)
            pyautogui.click()
            pyautogui.moveTo(1330, 735)
            pyautogui.click()
            time.sleep(2)
        # input("waiting for bidding")
        pyautogui.moveTo(580, 275)
        pyautogui.click()
        pyautogui.moveTo(580, 340)
        pyautogui.click()
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(1)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        time.sleep(2)

        with open('../wbr5-sort.txt', 'r') as f:
            content = f.readlines()

        potential_contracts = [content[-3][22:25], content[-3][36:39], content[-2][22:25], content[-2][36:39]]
        real_potentials = []
        numbers_of_real_potentials = []
        for potential in potential_contracts:
            if potential:
                if potential[0] in ['1', '2', '3', '4', '5', '6', '7']:
                    real_potentials.append(potential)
                    numbers_of_real_potentials.append(int(potential[0]))

        for i, number in enumerate(numbers_of_real_potentials):
            if number != max(numbers_of_real_potentials):
                real_potentials[i] = ""
        real_real_potentials = [real[1] for real in real_potentials if real != ""]
        coded_colors = ['C', 'D', 'H', 'S', 'N']
        if 'N' in real_real_potentials:
            bid = str(max(numbers_of_real_potentials)) + " " + 'BA'
        elif 'S' in real_real_potentials:
            bid = str(max(numbers_of_real_potentials)) + " " + 'Pik'
        elif 'H' in real_real_potentials:
            bid = str(max(numbers_of_real_potentials)) + " " + 'Kier'
        elif 'D' in real_real_potentials:
            bid = str(max(numbers_of_real_potentials)) + " " + 'Karo'
        elif 'C' in real_real_potentials:
            bid = str(max(numbers_of_real_potentials)) + " " + 'Trefl'
        else:
            bid = 'pas'
        # print(bid)
        with open('../contractsWbridge5.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([bid, max_contracts[k]])
            # print("Added")
