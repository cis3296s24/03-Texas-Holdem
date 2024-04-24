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

def input_card():
    rank = int(input("Enter card rank (1-13 where 1=two, 13=Ace): "))
    suit = int(input("Enter card suit (1=Hearts, 2=Clubs, 3=Diamonds, 4=Spades): "))
    return Card(rank, suit)

def simulate_poker_games(card_objects,num_player):
    #num_players = int(input("Enter the number of players (1-5): "))
    #num_players = min(max(num_players, 1), 5)
    num_players=num_player
    player_wins = [0] * num_players
    players_hands = [card_objects[i*2:(i+1)*2] for i in range(num_players)]
    #for i in range(num_players):
        #print(f"Define Player {i+1}'s hand:")
        #players_hands.append([input_card() for _ in range(2)])


    for _ in range(10000):
        deck = [Card(count, color) for color in range(1, 5) for count in range(1, 14)]
        flat_player_hands = [card for sublist in players_hands for card in sublist]
        # Remove the specific cards for Player 1 and Player 2 from the deck
        deck = [card for card in deck if card not in card_objects]

        # Shuffle the remaining deck
        random.shuffle(deck)

        # Assign specific hands to Player 1 and Player 2
        # Assuming the next five cards are community cards
        community_cards = deck[:5]
        # Evaluate hands (assuming Ranker.rank_all_hands and related evaluation logic is properly defined)

        player_hands_with_community = [hand + community_cards for hand in players_hands]
        player_best_hands = [Ranker.rank_all_hands([hand], return_all=False) for hand in player_hands_with_community]

        # Compare and record results
        best_hand_score = max(player_best_hands)
        winners = [score == best_hand_score for score in player_best_hands]
        for i in range(num_players):
            if winners[i]:
                player_wins[i] += 1
    # Calculate and return win rates and tie rate
    win_rates = [wins / 10000 for wins in player_wins]
    return win_rates

def create_deck():
        return [Card(count, color) for color in range(1, 5) for count in range(1, 14)]

# Deal hands to two players
def deal_hands(deck, num_cards=5):
    return deck[:num_cards], deck[num_cards:num_cards*2]




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


    def convert_to_card(card_string):
        # Split the input string assuming the format "Rank of Suit" with spaces
        parts = card_string.split('_of_')
        if len(parts) != 2:
            raise ValueError(f"Invalid card format: '{card_string}'. Expected format is 'Rank of Suit'.")

        rank, suit = parts  # Unpack the parts directly into rank and suit

        # Define mappings for count and color
        rank_to_count = {
            '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9,
            'Jack': 10, 'Queen': 11, 'King': 12, 'Ace': 13
        }
        suit_to_color = {
            'Clubs': 1, 'Diamonds': 2, 'Hearts': 3, 'Spades': 4
        }

        # Convert rank and suit to count and color, checking if they exist in the dictionary
        try:
            count = rank_to_count[rank]
            color = suit_to_color[suit.capitalize()]  # Capitalize to match key names
        except KeyError:
            raise ValueError(f"Unknown rank or suit in card: '{card_string}'.")

        # Create a new Card instance
        return Card(count, color)
    def convert_strings_to_cards(card_strings):
        return [convert_to_card(card_string) for card_string in card_strings]


    cards = convert_strings_to_cards([
        "Ace_of_Spades", "Ace_of_Hearts",
        "King_of_Spades", "King_of_Hearts",
        "Queen_of_Spades", "Queen_of_Hearts",
        "Jack_of_Spades", "Jack_of_Hearts",
        "10_of_Spades", "10_of_Hearts"
    ])

    win_rates = simulate_poker_games(cards)
    for i, rate in enumerate(win_rates):
        print(f"Player {i+1} Win Rate: {rate*100:.2f}%")

