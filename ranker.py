
import numpy as np
from card import Card

class Ranker:
    @staticmethod
    def rank_all_hands(hand_combos, return_all=False):
        """
        Evaluates all combinations of hands provided and ranks them. Can return all rankings or only the highest one.

        Args:
            hand_combos (list[list[Card]]): A list containing lists of Card objects, each list representing a hand.
            return_all (bool): If True, returns a list of all rankings. If False, returns only the highest ranked hand.

        Returns:
            list or tuple: Depending on 'return_all', a list of all rankings or a tuple for the highest ranked hand.
        """
        rank_res_arr = np.zeros(shape=(len(hand_combos), len(hand_combos[0])))
        for i, hand in enumerate(hand_combos):
            for j, card_combo in enumerate(hand):
                rank_res_arr[i, j] = Ranker.rank_one_hand(card_combo)
        results = []

        for hand in hand_combos:
            rank, tie_breakers = Ranker.rank_one_hand(hand)
            results.append((rank, tie_breakers))

        if return_all:
            return results
        else:
            highest_hand = max(results, key=lambda x: (x[0], x[1]))
            return highest_hand

    @staticmethod
    def rank_one_hand(hand):
        """
        Ranks a single poker hand.

        Args:
            hand (list[Card]): A list of Card objects.

        Returns:
            tuple: A tuple containing the rank of the hand and list of tie breakers.
        """
        counts = np.array([card.count for card in hand])
        colors = np.array([card.color for card in hand])
        counts.sort()
        suit_arr = Ranker.gen_suit_arr(colors)
        straight_arr = Ranker.gen_straight_arr(counts)

        rank = 0
        tie_breakers = []

        rank, tie_breakers = Ranker.straight_flush_check(counts, rank, straight_arr, suit_arr)
        if rank == 0:
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
            tie_breakers = sorted(counts, reverse=True)
            rank = 0

        return rank, tie_breakers

    @staticmethod
    def gen_suit_arr(colors):
        """
        Checks if all cards in the hand have the same suit.

        Args:
            colors (numpy.ndarray): Array of card color codes.

        Returns:
            bool: True if all cards have the same suit, otherwise False.
        """
        return np.max(colors) == np.min(colors)

    @staticmethod
    def gen_straight_arr(counts):
        """
        Determines if the hand is a straight.

        Args:
            counts (numpy.ndarray): Sorted array of card counts.

        Returns:
            bool: True if the cards form a straight, otherwise False.
        """
        straight_check = 0
        for i in range(4):
            if counts[i] + 1 == counts[i + 1]:
                straight_check += 1
        straight_check += ((counts[0] == 2) and (counts[4] == 14))
        return straight_check == 4

    @staticmethod
    def straight_flush_check(counts, rank, straight_arr, suit_arr):
        """
        Evaluates whether the hand is a straight flush.

        Args:
            counts (numpy.ndarray): Array of card values sorted in ascending order.
            rank (int): Current rank of the hand.
            straight_arr (bool): Indicates if the hand is a straight.
            suit_arr (bool): Indicates if all cards are of the same suit.

        Returns:
            int: The updated rank of the hand if a straight flush is found; otherwise, the original rank.
        """
        if rank == 0 and straight_arr and suit_arr:
            if counts[0] == 2 and counts[4] == 14:
                counts[:] = np.roll(counts, -1)
            return 8
        return rank

    @staticmethod
    def four_of_a_kind_check(counts, rank):
        """
        Checks if the hand contains four of a kind.

        Args:
            counts (numpy.ndarray): Array of card values.
            rank (int): Current rank of the hand.

        Returns:
            int: Returns 7 (rank for four of a kind) if found, otherwise returns the current rank.
        """
        if rank > 0:
            return rank
        if np.any(np.bincount(counts)[1:] == 4):
            for i in range(3):
                if counts[i] == counts[i+1]:
                    if counts[0] != counts[i]:
                        counts[:] = np.roll(counts, 4-i-1)
                        break
            return 7
        return rank

    @staticmethod
    def full_house_check(counts, rank):
        """
        Checks if the hand is a full house.

        Args:
            counts (numpy.ndarray): Array of card values.
            rank (int): Current rank of the hand.

        Returns:
            int: Returns 6 (rank for full house) if a full house is detected, otherwise returns the current rank.
        """
        if rank > 0:
            return rank
        count_bin = np.bincount(counts)[1:]
        if 3 in count_bin and 2 in count_bin:
            return 6
        return rank

    @staticmethod
    def flush_check(rank, suit_arr, counts):
        """
        Evaluates if the hand is a flush.

        Args:
            rank (int): Current rank of the hand.
            suit_arr (bool): Indicates if all cards are of the same suit.
            counts (numpy.ndarray): Array of card values.

        Returns:
            int: Returns 5 (rank for flush) if a flush is found, otherwise returns the current rank.
        """
        if rank > 0:
            return rank
        return 5 if suit_arr else rank

    @staticmethod
    def straight_check(counts, rank, straight_arr):
        """
        Checks if the hand is a straight.

        Args:
            counts (numpy.ndarray): Array of card values sorted in ascending order.
            rank (int): Current rank of the hand.
            straight_arr (bool): Indicates if the hand is a straight.

        Returns:
            int: Returns 4 (rank for straight) if a straight is found, otherwise returns the current rank.
        """
        if rank > 0:
            return rank
        if straight_arr:
            if counts[0] == 2 and counts[4] == 14:
                counts[:] = np.roll(counts, -1)
            return 4
        return rank

