import numpy as np


class Ranker:
    @staticmethod
    def rank_all_hands(hand_combos, return_all=False):
        rank_res_arr = np.zeros(shape=(len(hand_combos), len(hand_combos[0])))
        for i, hand in enumerate(hand_combos):
            for j, card_combo in enumerate(hand):
                rank_res_arr[i, j] = Ranker.rank_one_hand(card_combo)

        if return_all:
            return rank_res_arr
        else:
            return np.max(rank_res_arr, axis=0)

    @staticmethod
    def rank_one_hand(hand):

        print("Debug: Hand size is", len(hand))
        if len(hand) != 2:
            raise ValueError("Invalid hand size. Hand must contain exactly 5 cards.")

        counts = np.array([card.count for card in hand])
        colors = np.array([card.color for card in hand])

        counts.sort()
        suit_arr = Ranker.gen_suit_arr(colors)
        straight_arr = Ranker.gen_straight_arr(counts)

        rank = 0
        rank = Ranker.straight_flush_check(counts, rank, straight_arr, suit_arr)
        rank = Ranker.four_of_a_kind_check(counts, rank)
        rank = Ranker.full_house_check(counts, rank)
        rank = Ranker.flush_check(rank, suit_arr)
        rank = Ranker.straight_check(counts, rank, straight_arr)
        rank = Ranker.three_of_a_kind_check(counts, rank)
        rank = Ranker.two_pairs_check(counts, rank)
        rank = Ranker.one_pair_check(counts, rank)

        return rank

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

    def straight_flush_check(counts, rank, straight_arr, suit_arr):
        if rank == 0 and straight_arr and suit_arr:
            # Rearrange order of 2345A to A2345 if straight flush starts from 2
            if counts[0] == 2 and counts[4] == 14:
                counts[:] = np.roll(counts, -1)
            return 8
        return rank


    @staticmethod
    def four_of_a_kind_check(counts, rank):
        if rank > 0:
            return rank
        if np.any(np.bincount(counts)[1:] == 4):  # Adjusted to avoid counting zeros
            # Move the 4 of a kind to the back
            for i in range(3):  # Only need to check first 3 cards
                if counts[i] == counts[i+1]:
                    if counts[0] != counts[i]:  # If the four of a kind is not at the start
                        counts[:] = np.roll(counts, 4-i-1)
                        break
            return 7
        return rank

    @staticmethod
    def full_house_check(counts, rank):
        if rank > 0:
            return rank
        count_bin = np.bincount(counts)[1:]  # Adjusted to avoid counting zeros
        if 3 in count_bin and 2 in count_bin:
            return 6
        return rank

    @staticmethod
    def flush_check(rank, suit_arr):
        if rank > 0:
            return rank
        return 5 if suit_arr else rank

    @staticmethod
    def straight_check(counts, rank, straight_arr):
        if rank > 0:
            return rank
        if straight_arr:
            # Rearrange order of 2345A to A2345 if straight starts from 2
            if counts[0] == 2 and counts[4] == 14:
                counts[:] = np.roll(counts, -1)
            return 4
        return rank

    @staticmethod
    def three_of_a_kind_check(counts, rank):
        if rank > 0:
            return rank
        if np.any(np.bincount(counts)[1:] == 3):  # Adjusted to avoid counting zeros
            return 3
        return rank
    @staticmethod
    def two_pairs_check(counts, rank):
        if rank > 0:
            return rank
        pair_counts = np.bincount(counts)[1:]  # Adjusted to avoid counting zeros
        if len(pair_counts[pair_counts == 2]) == 2:
            return 2
        return rank

    @staticmethod
    def one_pair_check(counts, rank):
        if rank > 0:
            return rank
        if np.any(np.bincount(counts)[1:] == 2):  # Adjusted to avoid counting zeros
            return 1
        return rank
