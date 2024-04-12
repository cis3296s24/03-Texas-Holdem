import unittest

import numpy as np


class Card:
    def __init__(self, count: int, color: int):
        self._count = None
        self._color = None
        self.count = count  # Use the setter to check value
        self.color = color  # Use the setter to check value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        if not 1 <= value <= 13:
            raise ValueError("Count must be between 1 and 13.")
        self._count = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not 1 <= value <= 4:
            raise ValueError("Color must be between 1 and 4.")
        self._color = value

    def __repr__(self):
        return f"Card(count={self.count}, color={self.color})"

def set_card():
    return [Card(count, color) for color in range(1, 5) for count in range(1, 14)]


class Ranker:
    @staticmethod
    def rank_all_hands(hand_combos, return_all=False):
        results = []

        for hand in hand_combos:
            rank, tie_breakers = Ranker.rank_one_hand(hand)
            results.append((rank, tie_breakers))

        if return_all:
            return results
        else:
            # Sort the results based on rank and then tie_breakers, return the highest
            highest_hand = max(results, key=lambda x: (x[0], x[1]))
            return highest_hand


    @staticmethod
    def rank_one_hand(hand):

        counts = np.array([card.count for card in hand])
        colors = np.array([card.color for card in hand])

        # Sort the counts to make further operations easier.
        counts.sort()
        suit_arr = Ranker.gen_suit_arr(colors)
        straight_arr = Ranker.gen_straight_arr(counts)

        rank = 0
        tie_breakers = []

        # The checks return a tuple (rank, tie_breakers), we update both based on the check.
        rank, tie_breakers = Ranker.straight_flush_check(counts, rank, straight_arr, suit_arr)
        if rank == 0:  # Continue only if no higher rank was found
            rank, tie_breakers = Ranker.four_of_a_kind_check(counts, rank)
        if rank == 0:
            rank, tie_breakers = Ranker.full_house_check(counts, rank)
        if rank == 0:
            rank, tie_breakers = Ranker.flush_check(rank, suit_arr, counts)
        if rank == 0:
            rank, tie_breakers = Ranker.straight_check(counts, rank, straight_arr)
        if rank == 0:
            rank, tie_breakers = Ranker.three_of_a_kind_check(counts, rank)
        if rank == 0:
            rank, tie_breakers = Ranker.two_pairs_check(counts, rank)
        if rank == 0:
            rank, tie_breakers = Ranker.one_pair_check(counts, rank)
        if rank == 0:
            # High card case, return the sorted counts as tie_breakers.
            tie_breakers = sorted(counts, reverse=True)
            rank = 0  # Explicit for clarity, high card is the default case.

        return rank, tie_breakers


    @staticmethod
    def gen_suit_arr(colors):
        return np.max(colors) == np.min(colors)

    @staticmethod
    def gen_straight_arr(counts):
        straight_check = 0
        for i in range(4):
            if counts[i] + 1 == counts[i + 1]:
                straight_check += 1
        straight_check += ((counts[0] == 2) and (counts[4] == 14))  # Handling Ace as both high and low
        return straight_check == 4

    @staticmethod
    def straight_flush_check(counts, rank, straight_arr, suit_arr):
        if rank == 0 and straight_arr and suit_arr:
            # Handling Ace as both high and low in a straight flush
            if counts[0] == 2 and counts[4] == 14:
                # Ace-low straight flush, make Ace '1'
                return (8, [5])  # Returning 5 as the highest card (Ace is considered low)
            return (8, [counts[-1]])  # Return rank and highest card of straight flush
        return (rank, [])


    @staticmethod
    def four_of_a_kind_check(counts, rank):
        if rank > 0:
            return (rank, [])
        quad_value = np.where(np.bincount(counts)[1:] == 4)[0]
        if quad_value.size > 0:
            quad_value += 1  # Adjusting index to match card value
            kicker = np.max(np.setdiff1d(counts, quad_value))
            return (7, [quad_value[0], kicker])  # Returning rank, quad value, and kicker
        return (rank, [])

    @staticmethod
    def full_house_check(counts, rank):
        if rank > 0:
            return (rank, [])
        count_bin = np.bincount(counts)[1:]
        if 3 in count_bin and 2 in count_bin:
            triplet_value = np.where(count_bin == 3)[0][0] + 1
            pair_value = np.where(count_bin == 2)[0][0] + 1
            return (6, [triplet_value, pair_value])
        return (rank, [])


    @staticmethod
    def flush_check(rank, suit_arr, counts):
        if rank > 0:
            return (rank, [])
        if suit_arr:
            # Return all cards in descending order
            return (5, sorted(counts, reverse=True))
        return (rank, [])


    @staticmethod
    def straight_check(counts, rank, straight_arr):
        if rank > 0:
            return (rank, [])
        if straight_arr:
            if counts[0] == 2 and counts[4] == 14:  # Ace low straight
                return (4, [5])  # Returning 5 as the highest card
            return (4, [counts[-1]])
        return (rank, [])


    @staticmethod
    def three_of_a_kind_check(counts, rank):
        if rank > 0:
            return (rank, [])
        triplet_value = np.where(np.bincount(counts)[1:] == 3)[0]
        if triplet_value.size > 0:
            triplet_value += 1  # Adjust for card value
            kickers = np.sort(np.setdiff1d(counts, triplet_value))[::-1]  # Highest kickers
            return (3, [triplet_value[0]] + list(kickers[:2]))  # Include top 2 kickers
        return (rank, [])

    @staticmethod
    def two_pairs_check(counts, rank):
        if rank > 0:
            return (rank, [])
        pair_values = np.where(np.bincount(counts)[1:] == 2)[0]
        if pair_values.size == 2:
            pair_values += 1  # Adjust for card values
            kicker = np.max(np.setdiff1d(counts, pair_values))  # Highest kicker
            return (2, sorted(pair_values, reverse=True) + [kicker])
        return (rank, [])


    @staticmethod
    def one_pair_check(counts, rank):
        if rank > 0:
            return (rank, [])
        pair_value = np.where(np.bincount(counts)[1:] == 2)[0]
        if pair_value.size > 0:
            pair_value += 1  # Adjust for card value
            kickers = np.sort(np.setdiff1d(counts, pair_value))[::-1]  # Highest kickers
            return (1, [pair_value[0]] + list(kickers[:3]))  # Include top 3 kickers
        return (rank, [])



import random


# TO DO: add invalid input catching
def inputcard(player, card_num):
    count = int(input(f"Enter count for Player {player}'s card {card_num} (1-13, where 10-13 are J, Q, K, A): "))
    suit = int(input(f"Enter suit for Player {player}'s card {card_num} (1-4): "))
    return Card(count, suit)

def simulate_poker_games(num_simulations=10000):
    player1_wins = 0
    player2_wins = 0
    ties = 0

    player1_hand = [inputcard(1, 1), inputcard(1, 2)]
    player2_hand = [inputcard(2, 1), inputcard(2, 2)]
    players_hands = player1_hand + player2_hand
    for i in range(num_simulations):
        deck = create_deck()
        deck = [card for card in deck if card not in players_hands]
        random.shuffle(deck)
        community_cards = deck[:5]
        player1_best_hand = Ranker.rank_all_hands([player1_hand + community_cards], return_all=False)
        player2_best_hand = Ranker.rank_all_hands([player2_hand + community_cards], return_all=False)


    for _ in range(num_simulations):
        deck = create_deck()
        player1_hand = [Card(10, 1), Card(10, 2)]
        player2_hand = [Card(13, 2), Card(12, 3)]
        players_hands = player1_hand + player2_hand
        # Remove the specific cards for Player 1 and Player 2 from the deck
        deck = [card for card in deck if card not in players_hands]

        # Shuffle the remaining deck
        random.shuffle(deck)

        # Assign specific hands to Player 1 and Player 2


        # Assuming the next five cards are community cards
        community_cards = deck[:5]

        # Evaluate hands (assuming Ranker.rank_all_hands and related evaluation logic is properly defined)
        player1_best_hand = Ranker.rank_all_hands([player1_hand + community_cards], return_all=False)
        player2_best_hand = Ranker.rank_all_hands([player2_hand + community_cards], return_all=False)

        # Compare and record results
        if player1_best_hand > player2_best_hand:
            player1_wins += 1
        elif player2_best_hand > player1_best_hand:
            player2_wins += 1
        else:
            ties += 1



    # Calculate and return win rates and tie rate
    player1_win_rate = player1_wins / num_simulations
    player2_win_rate = player2_wins / num_simulations
    tie_rate = ties / num_simulations

    return player1_win_rate, player2_win_rate, tie_rate



if __name__ == '__main__':
    # Function to create a deck of 52 cards
    def create_deck():
        return [Card(count, color) for color in range(1, 5) for count in range(1, 14)]

    # Shuffle the deck
    def shuffle_deck(deck):
        random.shuffle(deck)
        return deck

    # Deal hands to two players
    def deal_hands(deck, num_cards=5):
        return deck[:num_cards], deck[num_cards:num_cards*2]


    player1_win_rate, player2_win_rate, tie_rate = simulate_poker_games()

    print(f"Player 1 Win Rate: {player1_win_rate*100:.2f}%")
    print(f"Player 2 Win Rate: {player2_win_rate*100:.2f}%")
    print(f"Tie Rate: {tie_rate*100:.2f}%")


import unittest
import numpy as np

# Ensure the Card and Ranker classes are imported or defined here

class TestPokerHandRanking(unittest.TestCase):


    def test_card_suit_limits(self):
        # Test the boundaries for card color
        with self.assertRaises(ValueError):
            Card(10, -1)  # Negative color
        with self.assertRaises(ValueError):
            Card(10, 6)  # Color exceeding upper limit

    def test_card_inequality(self):
        # Test inequality of two different cards
        card1 = Card(9, 3)
        card2 = Card(9, 4)
        self.assertNotEqual(card1, card2, "Different cards are considered equal")

    def test_print_card(self):
        # Test the print representation of a card which will be used for the UI
        card = Card(12, 4)
        self.assertEqual(repr(card), 'Card(count=12, color=4)', "Print representation of card is incorrect")

    def test_card_creation_success(self):
        # Test successful creation of a card within valid boundaries
        card = Card(1, 1)
        self.assertIsInstance(card, Card, "Card is not instantiated correctly")

    def test_straight_flush(self):
        hand = [Card(10, 1), Card(11, 1), Card(12, 1), Card(13, 1), Card(9, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (8, [13]), "Failed to recognize straight flush")

    def test_four_of_a_kind(self):
        hand = [Card(3, 1), Card(3, 2), Card(3, 3), Card(3, 4), Card(5, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (7, [3, 5]), "Failed to recognize four of a kind")

    def test_full_house(self):
        hand = [Card(6, 1), Card(6, 2), Card(6, 3), Card(9, 1), Card(9, 2)]
        self.assertEqual(Ranker.rank_one_hand(hand), (6, [6, 9]), "Failed to recognize full house")

    def test_flush(self):
        hand = [Card(2, 2), Card(5, 2), Card(7, 2), Card(8, 2), Card(10, 2)]
        self.assertEqual(Ranker.rank_one_hand(hand), (5, [10, 8, 7, 5, 2]), "Failed to recognize flush")

    def test_straight(self):
        hand = [Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 4), Card(8, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (4, [8]), "Failed to recognize straight")

    def test_three_of_a_kind(self):
        hand = [Card(12, 1), Card(12, 2), Card(12, 3), Card(5, 4), Card(8, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (3, [12, 8, 5]), "Failed to recognize three of a kind")

    def test_two_pairs(self):
        hand = [Card(9, 1), Card(9, 2), Card(5, 3), Card(5, 4), Card(7, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (2, [9, 5, 7]), "Failed to recognize two pairs")

    def test_one_pair(self):
        hand = [Card(4, 1), Card(4, 2), Card(6, 3), Card(7, 4), Card(8, 1)]
        self.assertEqual(Ranker.rank_one_hand(hand), (1, [4, 8, 7, 6]), "Failed to recognize one pair")

    def test_high_card(self):
        hand = [Card(2, 1), Card(4, 2), Card(6, 3), Card(8, 4), Card(10, 1)]
        # Note: For high card, the entire hand acts as kickers, sorted in descending order.
        self.assertEqual(Ranker.rank_one_hand(hand), (0, [10, 8, 6, 4, 2]), "Failed to correctly identify high card")
    
    #  Confirms that the string representation of the Card class is as expected.
    def test_card_representation(self):
        card = Card(11, 3)
        self.assertEqual(repr(card), 'Card(count=11, color=3)', "Card representation does not match")

    def test_invalid_card_color(self):
        with self.assertRaises(ValueError):
            Card(5, 0)  # Below valid range
        with self.assertRaises(ValueError):
            Card(5, 5)  # Above valid range

    def test_invalid_card_count(self):
        with self.assertRaises(ValueError):
            Card(0, 1)  # Below valid range
        with self.assertRaises(ValueError):
            Card(14, 1)  # Above valid range

if __name__ == '__main__':
    unittest.main()

