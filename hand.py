from utils import *
from exceptions import *
from ranker import *



class Hand:
    """
    A class to represent a poker hand, managing the cards in the hand and evaluating its strength within the context of given community cards.

    Attributes:
        hand_limit (int): The maximum number of cards that can be held in the hand.
        card_arr (numpy.ndarray): An array to store card data using integer representations.

    Methods:
        add_cards(cards): Adds cards to the hand and checks for the hand limit.
        remove_cards(cards): Removes specified cards from the hand.
        hand_evaluation(community_arr): Evaluates the hand strength based on the community cards.
        hand_value(community_arr): Calculates the value of the hand with possible combinations.
    """

    def __init__(self, hand_limit=2):
        """
        Initializes a Hand object with a specified limit for the number of cards.

        Args:
            hand_limit (int, optional): The maximum number of cards the hand can hold. Defaults to 2.
        """
        self.hand_limit = hand_limit
        self.card_arr = np.zeros(shape=(0, hand_limit), dtype=np.int32)

    def add_cards(self, cards):
        """
        Adds a list of cards to the hand, formatted as integers. Raises an exception if the limit is exceeded.

        Args:
            cards (list[int]): A list of cards to add to the hand.

        Raises:
            HandException: If adding the cards would exceed the hand limit.
        """
        cards = format_cards(cards)

        for card in cards:
            self.card_arr = add_card(card, self.card_arr)

        if len(self.card_arr) > self.hand_limit:
            raise HandException(f"Cannot Have more than {self.hand_limit} cards in hand")

    def remove_cards(self, cards):
        """
        Removes a list of cards from the hand.

        Args:
            cards (list[int]): A list of cards to remove from the hand.
        """
        cards = format_cards(cards)

        for card in cards:
            self.card_arr = remove_card(card, self.card_arr)

    def hand_evaluation(self, community_arr):
        """
        Evaluates and returns the strongest hand type that can be made with the current hand and community cards.

        Args:
            community_arr (numpy.ndarray): An array of community cards.

        Returns:
            str: The description of the best hand possible with the hand and community cards.
        """
        all_combos, res_arr = self.hand_value(community_arr)
        return hand_type_dict[np.max(res_arr) // 16 ** 5] + ' ' + ' '.join(
            card_arr_to_str(all_combos[0, np.argmax(res_arr), :, :]))

    def hand_value(self, community_arr):
        """
        Calculates the value of all possible hand combinations with the community cards.

        Args:
            community_arr (numpy.ndarray): An array of community cards.

        Returns:
            tuple: A tuple containing arrays of all combinations and their respective evaluations.

        Raises:
            HandException: If not enough community cards are provided to form a valid hand.
        """
        if len(community_arr) < 3:
            raise HandException("No valid hand has formed.")
        if self.hand_limit == 2:
            player_valid_hand = np.concatenate([self.card_arr, community_arr], axis=0)
            all_combos = np.expand_dims(player_valid_hand, axis=0)[:, comb_index(len(player_valid_hand), 5), :]
        else:
            community_combos = np.expand_dims(community_arr, axis=0)[:, comb_index(len(community_arr), 3), :]
            hand_combos = np.expand_dims(self.card_arr, axis=0)[:, comb_index(4, 2), :]
            all_combos = np.concatenate(
                [np.repeat(hand_combos, repeats=num_combinations(len(community_arr), 3), axis=1),
                 np.concatenate(6 * [community_combos], axis=1)], axis=2)
        res_arr = Ranker.rank_all_hands(all_combos, return_all=True)
        return all_combos, res_arr

    def __str__(self):
        """
        Returns a string representation of the cards in the hand.

        Returns:
            str: A string of card names in the hand.
        """
        return " ".join(card_arr_to_str(self.card_arr))