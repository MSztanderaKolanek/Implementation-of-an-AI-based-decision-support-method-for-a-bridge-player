from scripts.Learning import Learning
from scripts.Player import Player
from scripts.Deck import Deck

BIDS = ['1 Trefl', '1 Karo', '1 Kier', '1 Pik', '1 BA',
        '2 Trefl', '2 Karo', '2 Kier', '2 Pik', '2 BA',
        '3 Trefl', '3 Karo', '3 Kier', '3 Pik', '3 BA',
        '4 Trefl', '4 Karo', '4 Kier', '4 Pik', '4 BA',
        '5 Trefl', '5 Karo', '5 Kier', '5 Pik', '5 BA',
        '6 Trefl', '6 Karo', '6 Kier', '6 Pik', '6 BA',
        '7 Trefl', '7 Karo', '7 Kier', '7 Pik', '7 BA', 'pas']


def test_bidding_method():
    p1 = Player("Bob")
    p2 = Player("Alice")
    p3 = Player("Michael")
    p4 = Player("Emil")
    d = Deck()
    players = [p1, p2, p3, p4]
    learning = Learning(players)
    p1.add_cards_to_hand(d.get_and_remove_cards_from_deck(13))
    bid = learning.bidding_method([], p1, BIDS)
    assert bid in BIDS
