import unittest
import numpy as np
import card
from ranker import Ranker

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

if __name__ == '__main__':
    unittest.main()
