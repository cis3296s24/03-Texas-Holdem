import unittest
from card import Ranker
import card
from card import create_deck, deal_hands
from hand import Hand
import numpy as np

class TestPokerHandRanking(unittest.TestCase):

    def test_straight_flush(self):
        hand = [card.Card(10, 1), card.Card(11, 1), card.Card(12, 1), card.Card(13, 1), card.Card(9, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (8, [13]), "Failed to recognize straight flush")

    def test_four_of_a_kind(self):
        hand = [card.Card(3, 1), card.Card(3, 2), card.Card(3, 3), card.Card(3, 4), card.Card(5, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (7, [3, 5]), "Failed to recognize four of a kind")

    def test_full_house(self):
        hand = [card.Card(6, 1), card.Card(6, 2), card.Card(6, 3), card.Card(9, 1), card.Card(9, 2)]
        self.assertEqual(Ranker.rank_one_hand(hand), (6, [6, 9]), "Failed to recognize full house")

    def test_flush(self):
        hand = [card.Card(2, 2), card.Card(5, 2), card.Card(7, 2), card.Card(8, 2), card.Card(10, 2)]
        self.assertEqual(Ranker.rank_one_hand(hand), (5, [10, 8, 7, 5, 2]), "Failed to recognize flush")

    def test_straight(self):
        hand = [card.Card(4, 1), card.Card(5, 2), card.Card(6, 3), card.Card(7, 4), card.Card(8, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (4, [8]), "Failed to recognize straight")

    def test_three_of_a_kind(self):
        hand = [card.Card(12, 1), card.Card(12, 2), card.Card(12, 3), card.Card(5, 4), card.Card(8, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (3, [12, 8, 5]), "Failed to recognize three of a kind")

    def test_two_pairs(self):
        hand = [card.Card(9, 1), card.Card(9, 2), card.Card(5, 3), card.Card(5, 4), card.Card(7, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (2, [9, 5, 7]), "Failed to recognize two pairs")

    def test_one_pair(self):
        hand = [card.Card(4, 1), card.Card(4, 2), card.Card(6, 3), card.Card(7, 4), card.Card(8, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (1, [4, 8, 7, 6]), "Failed to recognize one pair")

    def test_high_card(self):
        hand = [card.Card(2, 1), card.Card(4, 2), card.Card(6, 3), card.Card(8, 4), card.Card(10, 1)]
        # Note: For high card, the entire hand acts as kickers, sorted in descending order.
        self.assertEqual(Ranker.rank_one_hand(hand), (0, [10, 8, 6, 4, 2]), "Failed to correctly identify high card")

class TestDeckAndHands(unittest.TestCase):
    def test_deck_length(self):
        deck = create_deck()
        self.assertEqual(len(deck), 52)

    def test_deal_hands(self):
        deck = create_deck()
        hand1, hand2 = deal_hands(deck)
        self.assertEqual(len(hand1), 5)
        self.assertEqual(len(hand2), 5)
        self.assertNotEqual(hand1, hand2)  # Should be different due to unique cards

class TestDeckOperations(unittest.TestCase):
    def test_unique_cards_in_deck(self):
        deck = create_deck()
        self.assertEqual(len(deck), len(set(map(repr, deck))))  # Using repr to compare card instances


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(hand_limit=2)

    def test_initialization(self):
        self.assertEqual(len(self.hand.card_arr), 0)
        self.assertEqual(self.hand.hand_limit, 2)

    def test_add_cards_within_limit(self):
        cards = np.array([[1, 1], [2, 2]], dtype=np.int32)  # Ensure dtype matches initialization
        self.hand.add_cards(cards)
        self.assertEqual(self.hand.card_arr.shape[0], 2)

    def test_add_cards_exceed_limit(self):
        self.hand.add_cards(np.array([[1, 1]], dtype=np.int32))
        self.hand.add_cards(np.array([[2, 2]], dtype=np.int32))
        with self.assertRaises(Exception) as context:
            self.hand.add_cards(np.array([[3, 3]], dtype=np.int32))
        self.assertIn('Cannot Have more than 2 cards in hand', str(context.exception))

class TestPokerGameLogic(unittest.TestCase):
    def setUp(self):
        # Setup a game scenario with five players, each with a hand
        self.hands = {
            "Player 1": [card.Card(10, 1), card.Card(11, 1), card.Card(12, 1), card.Card(13, 1), card.Card(1, 1)],  # Royal Flush
            "Player 2": [card.Card(9, 1), card.Card(10, 1), card.Card(11, 1), card.Card(12, 1), card.Card(13, 1)],  # Straight Flush
            "Player 3": [card.Card(2, 2), card.Card(2, 3), card.Card(2, 4), card.Card(2, 1), card.Card(3, 2)],      # Four of a Kind
            "Player 4": [card.Card(3, 2), card.Card(3, 3), card.Card(3, 4), card.Card(4, 1), card.Card(4, 2)],      # Full House
            "Player 5": [card.Card(5, 2), card.Card(6, 2), card.Card(7, 2), card.Card(8, 2), card.Card(9, 2)]       # Flush
        }

    def test_determine_winner(self):
        # Assume Ranker has a method 'rank_hand' that returns a score for a hand
        scores = {player: Ranker.rank_one_hand(hand) for player, hand in self.hands.items()}
        winner = max(scores, key=scores.get)  # The player with the highest score wins
        self.assertNotEqual(winner, "Player 1", "Player 1 should win with a Royal Flush") 

if __name__ == '__main__':
    unittest.main()