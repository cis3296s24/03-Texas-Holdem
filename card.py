import unittest

import numpy as np


class Card:
    """
    Represents a playing card with a number and a suit color.
    
    Attributes:
        count (int): The number on the card, which should be between 1 (Ace) and 13 (King).
        color (int): The suit color of the card, represented as an integer from 1 to 4.
    """
    def __init__(self, count: int, color: int):
        """
        Initialize a new Card instance with the specified count and color.
        
        Args:
            count (int): The number of the card.
            color (int): The suit color of the card.
        
        Raises:
            ValueError: If the count is not between 1 and 13, or if the color is not between 1 and 4.
        """
        self._count = None
        self._color = None
        self.count = count  # Use the setter to check value
        self.color = color  # Use the setter to check value

    @property
    def count(self):
        """
        Returns the number on the card.
        
        Returns:
            int: The number on the card.
        """
        return self._count

    @count.setter
    def count(self, value):
        """
        Sets the number on the card, ensuring it is within the valid range.
        
        Args:
            value (int): The number to set on the card.
        
        Raises:
            ValueError: If the value is not between 1 and 13.
        """
        if not 1 <= value <= 13:
            raise ValueError("Count must be between 1 and 13.")
        self._count = value

    @property
    def color(self):
        """
        Returns the suit color of the card.
        
        Returns:
            int: The suit color of the card.
        """
        return self._color

    @color.setter
    def color(self, value):
        """
        Sets the suit color of the card, ensuring it is within the valid range.
        
        Args:
            value (int): The suit color to set on the card.
        
        Raises:
            ValueError: If the value is not between 1 and 4.
        """
        if not 1 <= value <= 4:
            raise ValueError("Color must be between 1 and 4.")
        self._color = value


    def __repr__(self):
        """
        Returns a string representation of the card.
        
        Returns:
            str: A string representation showing both count and color of the card.
        """
        return f"Card(count={self.count}, color={self.color})"

def set_card():
    """
    Generates a list of Card instances representing a full set of cards.
    
    Returns:
        list[Card]: A list containing one of each card combination from Ace to King in four colors.
    """
    return [Card(count, color) for color in range(1, 5) for count in range(1, 14)]


class Ranker:
    """
    Provides static methods to rank poker hands based on traditional poker hand rankings.
    """
    @staticmethod
    def rank_all_hands(hand_combos, return_all=False):
        """
        Ranks all provided hands of cards and optionally returns all rankings or just the highest one.
        
        Args:
            hand_combos (list[list[Card]]): A list of lists, where each inner list represents a hand of cards.
            return_all (bool): If True, returns a list of all ranked hands. If False, returns only the highest ranked hand.
        
        Returns:
            list or tuple: Depending on `return_all`, returns a list of all hand rankings or a tuple for the highest ranked hand.
        """
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
        """
        Ranks a single poker hand and returns the rank and tie breakers.

        Args:
            hand (list[Card]): A list of Card instances representing a single poker hand.

        Returns:
            tuple: A tuple containing the rank of the hand and a list of tie breakers.
         """
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
        """
        Checks if all cards in a hand are of the same suit.

        Args:
        colors (list[int]): A list of integers representing the colors (suits) of the cards.

        Returns:
        bool: True if all cards are of the same suit, otherwise False.
        """
        return np.max(colors) == np.min(colors)

    @staticmethod
    def gen_straight_arr(counts):
        """
        Determines if the hand forms a straight.

        Args:
            counts (list[int]): A list of integers representing the counts (values) of the cards, sorted in ascending order.

        Returns:
            bool: True if the cards form a straight, otherwise False.
        """
        straight_check = 0
        for i in range(4):
            if counts[i] + 1 == counts[i + 1]:
                straight_check += 1
        straight_check += ((counts[0] == 2) and (counts[4] == 14))  # Handling Ace as both high and low
        return straight_check == 4

    @staticmethod
    def straight_flush_check(counts, rank, straight_arr, suit_arr):
        """
        Checks for a straight flush in a poker hand.

        Args:
            counts (np.array): An array of card counts.
            rank (int): Current rank of the hand.
            straight_arr (bool): Whether the hand is a straight.
            suit_arr (bool): Whether all cards are of the same suit.

        Returns:
            tuple: Updated rank and tie breakers if a straight flush is found.
        """
        if rank == 0 and straight_arr and suit_arr:
            # Handling Ace as both high and low in a straight flush
            if counts[0] == 2 and counts[4] == 14:
                # Ace-low straight flush, make Ace '1'
                return (8, [5])  # Returning 5 as the highest card (Ace is considered low)
            return (8, [counts[-1]])  # Return rank and highest card of straight flush
        return (rank, [])


    @staticmethod
    def four_of_a_kind_check(counts, rank):
        """
        Checks for four of a kind in a poker hand.

        Args:
            counts (np.array): An array of card counts.
            rank (int): Current rank of the hand.

        Returns:
            tuple: Updated rank and tie breakers if four of a kind is found.
        """
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
        """
        Checks for a full house in a poker hand.

        Args:
            counts (np.array): An array of card counts.
            rank (int): Current rank of the hand.

        Returns:
            tuple: Updated rank and tie breakers if a full house is found.
        """
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
        """
        Determines if the hand is a flush and returns the appropriate rank and tie breakers.

        Args:
            rank (int): The current rank of the hand.
            suit_arr (bool): Boolean indicating whether all cards have the same suit.
            counts (np.array): Array of card values sorted in ascending order.

        Returns:
            tuple: Rank of the hand and tie breakers if the hand is a flush; otherwise, current rank and empty list.
        """
        if rank > 0:
            return (rank, [])
        if suit_arr:
            # Return all cards in descending order
            return (5, sorted(counts, reverse=True))
        return (rank, [])


    @staticmethod
    def straight_check(counts, rank, straight_arr):
        """
        Checks if the hand contains a straight and returns the updated rank and tie breakers.

        Args:
            counts (np.array): An array of card values sorted in ascending order.
            rank (int): The current rank of the hand.
            straight_arr (bool): Boolean indicating whether the hand forms a straight.

        Returns:
            tuple: Updated rank and tie breakers if the hand is a straight.
        """
        if rank > 0:
            return (rank, [])
        if straight_arr:
            if counts[0] == 2 and counts[4] == 14:  # Ace low straight
                return (4, [5])  # Returning 5 as the highest card
            return (4, [counts[-1]])
        return (rank, [])


    @staticmethod
    def three_of_a_kind_check(counts, rank):
        """
        Checks for three of a kind in the hand and updates the rank and tie breakers accordingly.

        Args:
            counts (np.array): An array of card values.
            rank (int): The current rank of the hand.

        Returns:
            tuple: Updated rank and tie breakers if three of a kind is found.
        """
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
        """
        Checks for two pairs in the hand and updates the rank and tie breakers accordingly.

        Args:
            counts (np.array): An array of card values.
            rank (int): The current rank of the hand.

        Returns:
            tuple: Updated rank and tie breakers if two pairs are found.
        """
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
        """
        Checks for a single pair in the hand and updates the rank and tie breakers accordingly.

        Args:
            counts (np.array): An array of card values.
            rank (int): The current rank of the hand.

        Returns:
            tuple: Updated rank and tie breakers if one pair is found.
        """
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
    """
    Prompts the user to input the rank and suit of a card and returns a Card object.

    Returns:
        Card: A new Card object based on user input.
    """
    rank = int(input("Enter card rank (1-13 where 1=two, 13=Ace): "))
    suit = int(input("Enter card suit (1=Hearts, 2=Clubs, 3=Diamonds, 4=Spades): "))
    return Card(rank, suit)

def simulate_poker_games(card_objects,num_player):
    """
    Simulates a series of poker games to determine win rates for players based on their initial hands.

    Args:
        card_objects (list[Card]): List of Card objects representing the players' initial hands.
        num_players (int): Number of players in the game.

    Returns:
        list[float]: List of win rates for each player.
    """
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


def simulate_poker_game_with_community_card(card_objects, num_players, community_cards):
    """
        Simulates poker games with predefined community cards.

        Args:
            card_objects (list[Card]): List of Card objects representing the hands of the players.
            num_players (int): Number of players in the game.
            community_cards (list[Card]): List of community cards used in the game.

        Returns:
            list[float]: List of win rates for each player.
    """
    player_wins = [0] * num_players
    players_hands = [card_objects[i*2:(i+1)*2] for i in range(num_players)]

    for _ in range(10000):
        # Create a full deck
        deck = [Card(count, color) for color in range(1, 5) for count in range(1, 14)]
        # Remove cards that are already in use (player hands + community cards)
        flat_player_hands = [card for sublist in players_hands for card in sublist]
        used_cards = flat_player_hands + community_cards
        deck = [card for card in deck if card not in used_cards]

        # Shuffle the remaining deck
        random.shuffle(deck)

        # The community cards are predefined, no need to draw them from the deck
        player_hands_with_community = [hand + community_cards for hand in players_hands]
        player_best_hands = [Ranker.rank_all_hands([hand], return_all=False) for hand in player_hands_with_community]

        # Compare and record results
        best_hand_score = max(player_best_hands)
        winners = [score == best_hand_score for score in player_best_hands]
        for i in range(num_players):
            if winners[i]:
                player_wins[i] += 1

    # Calculate and return win rates
    win_rates = [wins / 10000 for wins in player_wins]
    return win_rates


def create_deck():
    """
        Creates a deck of 52 playing cards.

        Returns:
            list[Card]: A list of Card instances representing a standard deck.
    """
    return [Card(count, color) for color in range(1, 5) for count in range(1, 14)]






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
        """
        Deals hands from a deck to two players.

        Args:
            deck (list[Card]): A list of Card instances representing a deck.
            num_cards (int): Number of cards to deal to each player.

        Returns:
            tuple: Two lists of Card instances representing the hands dealt to each player.
        """
        return deck[:num_cards], deck[num_cards:num_cards*2]


    def convert_to_card(card_string):
        """
        Converts a card string in a specific format to a Card object.

        Args:
            card_string (str): The string representing a card, formatted as 'Rank_of_Suit'.

        Returns:
            Card: A Card object initialized with the appropriate rank and suit.

        Raises:
            ValueError: If the input string does not match the expected format or contains invalid values.
        """
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
        """
        Converts a list of card strings to a list of Card objects.

        Args:
            card_strings (list[str]): A list of strings each representing a card in the format 'Rank_of_Suit'.

        Returns:
            list[Card]: A list of Card objects corresponding to the input card strings.
        """
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

