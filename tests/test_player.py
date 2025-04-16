from scripts.Player import Player
from scripts.Deck import Deck


def test_player_add_cards_adds_to_hand():
    p = Player("Alice")
    d = Deck()
    p.add_cards_to_hand(d.get_and_remove_cards_from_deck(13))
    assert len(p.hand) == 13


def test_player_add_cards_removes_from_deck():
    p = Player("Bob")
    d = Deck()
    p.add_cards_to_hand(d.get_and_remove_cards_from_deck(13))
    assert len(d.deck) == 39
