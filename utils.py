import numpy as np
from math import factorial
from itertools import combinations, chain
from scipy.special import comb
from exceptions import *


num_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
suit_dict = {"d": 0, "c": 1, "s": 2, "h": 3}
rev_num_dict = {v: k for k, v in num_dict.items()}
rev_suit_dict = {v: k for k, v in suit_dict.items()}
hand_type_dict = {0: 'High Card', 1: 'One Pair', 2: 'Two Pairs', 3: 'Three of a Kind', 4: 'Straight', 5: 'Flush', 6: 'Full House', 7: 'Four of a Kind', 8: 'Straight Flush'}

def num_combinations(total, selected):
    """
    Calculates the number of ways to choose 'selected' items from 'total' items without replacement.

    Args:
        total (int): Total number of items.
        selected (int): Number of items to select.

    Returns:
        int: The number of combinations.
    """
    return int(factorial(total)/(factorial(selected)*factorial(total-selected)))


def comb_index(n, k):
    """
    Generates all possible combinations of indices for selecting 'k' elements from an array of length 'n'.

    Args:
        n (int): Length of the array from which elements are to be chosen.
        k (int): Number of elements to choose.

    Returns:
        numpy.ndarray: An array of shape (M, k) where M is the number of combinations, and each row represents indices of a combination.
    """
    count = comb(n, k, exact=True)
    index = np.fromiter(chain.from_iterable(combinations(range(n), k)),
                        int, count=count*k)
    return index.reshape(-1, k)

def card_str_to_arr(card_str):
    """
    Converts a list of card strings into a 2D numpy array representing card numbers and suits.

    Args:
        card_str (list[str]): List of card strings, each formatted as 'RankSuit'.

    Returns:
        numpy.ndarray: A 2D array where each row represents a card with columns for rank and suit.
    """
    return np.array([[num_dict[card[0]], suit_dict[card[1]]] for card in card_str])


def card_arr_to_str(card_arr):
    """
    Converts a 2D numpy array representing cards into a list of card strings.

    Args:
        card_arr (numpy.ndarray): A 2D array where each row represents a card with columns for rank and suit.

    Returns:
        list[str]: List of card strings formatted as 'RankSuit'.
    """
    return [rev_num_dict[card[0]] + rev_suit_dict[card[1]] for card in card_arr]


def remove_card(card, card_arr):
    """
    Removes a specified card from a card array.

    Args:
        card (str or numpy.ndarray): The card to remove, specified either as a string or as an array element.
        card_arr (numpy.ndarray): Array from which the card is to be removed.

    Returns:
        numpy.ndarray: Array with the specified card removed.

    Raises:
        DeckException: If the specified card is not found in the array.
    """
    if type(card) == str:
        card_check = (card_arr[:, 0] == card_str_to_arr([card])[0][0]) & (card_arr[:, 1] == card_str_to_arr([card])[0][1])
    else:
        card_check = (card_arr[:, 0] == card[0]) & (card_arr[:, 1] == card[1])
    if not card_check.sum():
        raise DeckException(f"Card {card if type(card) == str else ' '.join(card_arr_to_str([card]))} is not in the Deck")
    return card_arr[~card_check]

def add_card(card, card_arr):
    """
    Adds a specified card to a card array, ensuring no duplicates.

    Args:
        card (str or numpy.ndarray): The card to add, specified either as a string or as an array element.
        card_arr (numpy.ndarray): Array to which the card is to be added.

    Returns:
        numpy.ndarray: Array with the specified card added.

    Raises:
        HandException: If the specified card is already present in the array.
    """
    if len(card_arr) == 0:
        card_arr = card_str_to_arr([card]) if type(card) == str else np.array([card])
    else:
        new_card = card_str_to_arr([card]) if type(card) == str else np.array([card])
        card_check = np.array((card_arr[:, 0] == new_card[0][0]) & (card_arr[:, 1] == new_card[0][1]))

        if card_check.sum():
            raise HandException(f"Card {card if type(card) == str else ' '.join(card_arr_to_str([card]))} is already added")
        card_arr = np.concatenate([
                card_arr,
                new_card
            ], axis=0)
    return card_arr

def format_cards(cards):
    """
    Normalizes different forms of card inputs into a consistent format.

    Args:
        cards (str, list, or numpy.ndarray): Input cards, which could be a single string, a list of integers, or a numpy array.

    Returns:
        list: A normalized list of cards.
    """
    if type(cards) == np.ndarray and cards.ndim == 1:
        return [cards]
    elif type(cards) == list and type(cards[0]) == int:
        return [cards]
    elif type(cards) == str:
        return [cards]
    return cards
