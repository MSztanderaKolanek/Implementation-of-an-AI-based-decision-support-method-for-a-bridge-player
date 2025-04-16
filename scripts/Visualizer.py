from pandas import *
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np


FILES_TO_VISUALIZE = []
FILES_TO_VISUALIZE.append('contractsWbridge5.csv')
FILES_TO_VISUALIZE.append('contractsBiddingMethod.csv')
FILES_TO_VISUALIZE.append('contractsAlgorithm.csv')

CONTRACTS_DICT_0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
CONTRACTS_DICT_1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
CONTRACTS_DICT_2 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
CONTRACT_DICTS = [CONTRACTS_DICT_0, CONTRACTS_DICT_1, CONTRACTS_DICT_2]
IF_MAX_CONTRACT_CONTRACTS_DICT_0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
IF_MAX_CONTRACT_CONTRACTS_DICT_1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
IF_MAX_CONTRACT_CONTRACTS_DICT_2 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
IF_MAX_CONTRACT_CONTRACTS_DICTS = [IF_MAX_CONTRACT_CONTRACTS_DICT_0,
                                   IF_MAX_CONTRACT_CONTRACTS_DICT_1,
                                   IF_MAX_CONTRACT_CONTRACTS_DICT_2]
IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICT_0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICT_1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICT_2 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICTS = [IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICT_0,
                                              IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICT_1,
                                              IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICT_2]
MAX_CONTRACTS_DICT_0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
MAX_CONTRACTS_DICT_1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
MAX_CONTRACTS_DICT_2 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
MAX_CONTRACTS_DICTS = [MAX_CONTRACTS_DICT_0, MAX_CONTRACTS_DICT_1, MAX_CONTRACTS_DICT_2]
FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICT_0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICT_1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICT_2 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS = [FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICT_0,
                                                    FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICT_1,
                                                    FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICT_2]
COLORS = ['Trefl', 'Karo', 'Kier', 'Pik', 'BA']


for k, file in enumerate(FILES_TO_VISUALIZE):
    contracts_data = read_csv(FILES_TO_VISUALIZE[k])
    CONTRACTS = contracts_data['contract']
    MAX_CONTRACTS = contracts_data['maximum_contracts']

    for i, contract in enumerate(CONTRACTS):
        current_colors = []
        if contract == 'pas':
            CONTRACT_DICTS[k][0] += 1
        else:
            CONTRACT_DICTS[k][int(contract[0])] += 1
        if MAX_CONTRACTS[i] == "-----":
            MAX_CONTRACTS_DICTS[k][0] += 1
            if contract == 'pas':
                IF_MAX_CONTRACT_CONTRACTS_DICTS[k][0] += 1
                IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICTS[k][0] += 1
                FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS[k][0] += 1
            if contract[0] == '1':
                FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS[k][0] += 1
        else:
            current_max_contract = max([int(x) for x in MAX_CONTRACTS[i].replace('-', '0')])
            MAX_CONTRACTS_DICTS[k][current_max_contract] += 1
            if contract != 'pas':
                if int(contract[0]) == current_max_contract:
                    IF_MAX_CONTRACT_CONTRACTS_DICTS[k][current_max_contract] += 1
                    for j, sign in enumerate(list(MAX_CONTRACTS[i])):
                        if sign != '-':
                            if int(sign) == current_max_contract:
                                current_colors.append(COLORS[j])
                    if contract[2:] in current_colors:
                        IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICTS[k][current_max_contract] += 1
                        FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS[k][current_max_contract] += 1
                elif int(contract[0]) + 1 == current_max_contract or int(contract[0]) - 1 == current_max_contract:
                    for j, sign in enumerate(list(MAX_CONTRACTS[i])):
                        if sign != '-':
                            if int(sign) == current_max_contract:
                                current_colors.append(COLORS[j])
                    if contract == 'pas':
                        FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS[k][current_max_contract] += 1
                    elif contract[2:] in current_colors:
                        FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS[k][current_max_contract] += 1


def generate_max_contracts_hist(max_contracts_dict):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje
    # wszystkie maksymalne kontrakty w zbiorze
    # Data
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    current_contracts = [max_contracts_dict[x] for x in range(8)]
    raw_data = {'lightgreyBars': current_contracts}
    df = pd.DataFrame(raw_data)
    orangeBars = [i for i in df['lightgreyBars']]

    # plot
    barWidth = 0.85
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    # Create orange Bars
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)

    plt.bar(r, orangeBars, color='lightgrey', edgecolor='white', width=barWidth)

    # Custom x axis
    plt.xticks(r, names)
    plt.title('Maksymalne kontrakty')
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Show graphic
    plt.show()


def generate_contracts_hist(contracts_dict):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje
    # wszystkie maksymalne kontrakty w zbiorze
    # Data
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    current_contracts = [contracts_dict[x] for x in range(8)]
    raw_data = {'lightgreyBars': current_contracts}
    df = pd.DataFrame(raw_data)
    orangeBars = [i for i in df['lightgreyBars']]

    # plot
    barWidth = 0.85
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    # Create orange Bars
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)

    plt.bar(r, orangeBars, color='lightgrey', edgecolor='white', width=barWidth)

    # Custom x axis
    plt.xticks(r, names)
    plt.title('Wylicytowane kontrakty')
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))
    # Show graphic
    plt.show()


def generate_divided_hist(max_contracts_dict, if_max_contract_contracts_dict):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje,
    # ile kontraktów o każdej wysokości zostało optymalnie wylicytowanych.
    # Słupki wyłącznie pomarańczowe - 0 optymalnych kontraktów.
    # Słupki wyłąćznie zielone - 100% optymalnych kontraktów.
    # Data
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    correct_contracts = [max_contracts_dict[x] - if_max_contract_contracts_dict[x] for x in range(8)]
    incorrect_contracts = [if_max_contract_contracts_dict[x] for x in range(8)]

    # raw_data = {'greenBars': [20, 1.5, 7, 10, 5, 4, 2, 5], 'orangeBars': [5, 15, 5, 10, 15, 2, 6, 3]}
    raw_data = {'greenBars': incorrect_contracts, 'orangeBars': correct_contracts}
    df = pd.DataFrame(raw_data)
    # From raw value to percentage
    # totals = [i + j for i, j in zip(df['greenBars'], df['orangeBars'])]
    # greenBars = [i / j * 100 for i, j in zip(df['greenBars'], totals)]
    # orangeBars = [i / j * 100 for i, j in zip(df['orangeBars'], totals)]
    greenBars = [i for i in df['greenBars']]
    orangeBars = [i for i in df['orangeBars']]

    # plot
    barWidth = 0.85
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)
    # Create green Bars
    plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth)
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)

    # Custom x axis
    plt.xticks(r, names)
    plt.legend(["Wylicytowane kontrakty", "Maksymalne kontrakty"])
    plt.title("Stosunek kontraktów o poprawnej wysokości do maksymalnych")
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Show graphic
    plt.show()


def generate_divided_hist_max(max_contracts_dict, if_max_contract_and_color_contracts_dict):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje,
    # ile kontraktów o każdej wysokości zostało optymalnie wylicytowanych - biorąc pod uwagę też kolory.
    # Słupki wyłącznie pomarańczowe - 0 optymalnych kontraktów.
    # Słupki wyłąćznie zielone - 100% optymalnych kontraktów.
    # Data
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    correct_contracts = [max_contracts_dict[x] - if_max_contract_and_color_contracts_dict[x] for x in range(8)]
    incorrect_contracts = [if_max_contract_and_color_contracts_dict[x] for x in range(8)]

    raw_data = {'greenBars': incorrect_contracts, 'orangeBars': correct_contracts}
    df = pd.DataFrame(raw_data)

    greenBars = [i for i in df['greenBars']]
    orangeBars = [i for i in df['orangeBars']]

    # plot
    barWidth = 0.85
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)
    # Create green Bars
    plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth)
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)

    # Custom x axis
    plt.xticks(r, names)
    plt.legend(["Wylicytowane kontrakty", "Maksymalne kontrakty"])
    plt.title("Stosunek kontraktów o poprawnej wysokości i kolorze do maksymalnych")
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Show graphic
    plt.show()


def generate_mistakes_forgiving_hist(max_contracts_dict, forgiving_max_contract_and_color_contracts_dict):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje,
    # ile kontraktów o każdej wysokości zostało optymalnie wylicytowanych - biorąc pod uwagę też kolory.
    # Słupki wyłącznie pomarańczowe - 0 optymalnych kontraktów.
    # Słupki wyłąćznie zielone - 100% optymalnych kontraktów.
    # UWAGA - w tym przypadku jeżeli nastąpiła pomyłka o 1 (1 karo było optymalne, zalicytowano 2 karo lub pas)
    # tez zalicza się jako optymalne
    # Data
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    correct_contracts = [max_contracts_dict[x] - forgiving_max_contract_and_color_contracts_dict[x] for x in range(8)]
    incorrect_contracts = [forgiving_max_contract_and_color_contracts_dict[x] for x in range(8)]

    raw_data = {'greenBars': incorrect_contracts, 'orangeBars': correct_contracts}
    df = pd.DataFrame(raw_data)

    greenBars = [i for i in df['greenBars']]
    orangeBars = [i for i in df['orangeBars']]

    # plot
    barWidth = 0.85
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)
    # Create green Bars
    plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth)
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)

    # Custom x axis
    plt.xticks(r, names)
    plt.legend(["Wylicytowane kontrakty", "Maksymalne kontrakty"])
    plt.title("Stosunek kontraktów do maksymalnych z możliwością pomyłki")
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Show graphic
    plt.show()


def generate_multiple_contracts_hist(contracts_dicts):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje
    # wszystkie maksymalne kontrakty w zbiorze
    # Data
    contracts_0 = []
    contracts_1 = []
    contracts_2 = []
    contracts = [contracts_0, contracts_1, contracts_2]
    for z, contracts_dict in enumerate(contracts_dicts):
        contracts[z] = [contracts_dict[x] for x in range(8)]

    # current_contracts = [contracts_dict[x] for x in range(8)]
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    r = np.arange(len(names))
    raw_data = {'blueBars': contracts[2], 'orangeBars': contracts[1], 'greenBars': contracts[0]}
    df = pd.DataFrame(raw_data)

    greenBars = [i for i in contracts[0]]
    orangeBars = [i for i in contracts[1]]
    blueBars = [i for i in contracts[2]]

    # plot
    barWidth = 0.85

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)
    # Create green Bars
    plt.bar(r + 0.3, greenBars, color='green', edgecolor='white', width=barWidth / 3)
    # Create orange Bars
    plt.bar(r - 0.3, orangeBars, color='orange', edgecolor='white', width=barWidth / 3)
    # Create blue Bars
    plt.bar(r, blueBars, color='blue', edgecolor='white', width=barWidth / 3)

    # Custom x axis
    plt.xticks(r, names)
    plt.legend(["Wbridge5", "Metoda dla początkujących", "Uczenie ze wzmocnieniem"])
    plt.title("Kontrakty wszystkich metod")
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Show graphic
    plt.show()


def generate_multiple_contracts_hist_max(max_contract_dicts):
    # wykres pokazuje 8 słupków - każdy odpowiada wysokości kontraktu. Wykres pokazuje
    # wszystkie maksymalne kontrakty w zbiorze
    # Data

    contracts_0 = []
    contracts_1 = []
    contracts_2 = []
    contracts = [contracts_0, contracts_1, contracts_2]
    for z, contracts_dict in enumerate(max_contract_dicts):
        contracts[z] = [contracts_dict[x] for x in range(8)]

    # current_contracts = [contracts_dict[x] for x in range(8)]
    names = ('0', '1', '2', '3', '4', '5', '6', '7')
    r = np.arange(len(names))
    raw_data = {'blueBars': contracts[2], 'orangeBars': contracts[1], 'greenBars': contracts[0]}
    df = pd.DataFrame(raw_data)

    greenBars = [i for i in contracts[0]]
    orangeBars = [i for i in contracts[1]]
    blueBars = [i for i in contracts[2]]

    # plot
    barWidth = 0.85

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_axisbelow(True)
    # Create green Bars
    plt.bar(r, greenBars, color='green', edgecolor='white', width=barWidth / 3)
    # Create orange Bars
    plt.bar(r - 0.3, orangeBars, color='orange', edgecolor='white', width=barWidth / 3)
    # Create blue Bars
    plt.bar(r + 0.3, blueBars, color='blue', edgecolor='white', width=barWidth / 3)

    # Custom x axis
    plt.xticks(r, names)
    plt.legend(["Wbridge5", "Metoda dla początkujących", "Uczenie ze wzmocnieniem"])
    plt.title("Maksymalne kontrakty wszystkich metod")
    plt.ylabel("Liczba kontraktów")
    plt.xlabel("Poziom kontraktu")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Show graphic
    plt.show()


generate_max_contracts_hist(MAX_CONTRACTS_DICTS[0])
generate_contracts_hist(CONTRACT_DICTS[0])
generate_divided_hist(MAX_CONTRACTS_DICTS[0], IF_MAX_CONTRACT_CONTRACTS_DICTS[0])
generate_divided_hist_max(MAX_CONTRACTS_DICTS[0], IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICTS[0])
generate_mistakes_forgiving_hist(MAX_CONTRACTS_DICTS[0], FORGIVING_MAX_CONTRACT_AND_COLOR_CONTRACTS_DICTS[0])
generate_multiple_contracts_hist(CONTRACT_DICTS)
generate_multiple_contracts_hist_max(IF_MAX_CONTRACT_AND_COLORS_CONTRACTS_DICTS)
