import pygame
import sys
from dropDown import dropDownMenu
import random
import card

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
running = True
convert = True

pygame.display.set_caption("Texas Hold em Odds Calculator")

card_images_path = "PlayingCards/PNG-cards-1.3/"
# Load the image
pokertable_image = pygame.image.load("pokertable.png")

# Resize the image to fit the screen
pokertable_image = pygame.transform.scale(pokertable_image, (1280, 720))

dropdown_menu = dropDownMenu(card_images_path, screen)
selected_cards = []  # List to hold selected cards and their positions
s_cards = []

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
        'clubs': 1, 'diamonds': 2, 'hearts': 3, 'spades': 4
    }

    # Convert rank and suit to count and color, checking if they exist in the dictionary
    try:
        count = rank_to_count[rank]
        color = suit_to_color[suit.capitalize()]  # Capitalize to match key names
    except KeyError:
        raise ValueError(f"Unknown rank or suit in card: '{card_string}'.")

    # Create a new Card instance
    return card.Card(count, color)

def convert_strings_to_cards(card_strings):
    return [convert_to_card(card_string) for card_string in card_strings]

if __name__ == "__main__":
    num_players = int(sys.argv[1])
    print(f"num_players tablemodel: {num_players}")

# Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                dropdown_menu.handle_events(event)

        screen.blit(pokertable_image, (-100, 0))
        dropdown_menu.draw()

        # Check if a card is selected
        selected_card = dropdown_menu.get_selected_card()
        selected_card_image = dropdown_menu.get_selected_card_image()

        if selected_card:
            # Add the selected card and its position to the list
            selected_cards.append((selected_card_image, selected_card))
            s_cards.append(selected_card)
            # Reset the selected card in the drop-down menu
            dropdown_menu.selected_card = None

        # Display selected cards on the screen
        for i, (card_image, card_name) in enumerate(selected_cards):
            positionValues = ((300,150), (350,150), (675,150), (725,150), (840,320), (890,320), (725,490), (675,490), (350,490), (300,490))        #positions for cards
            card_position = positionValues[i]

            resized_card_image = pygame.transform.scale(card_image, (50, 80))
            screen.blit(resized_card_image, card_position)

        if len(selected_cards) == 10 and convert == True:
            cards = convert_strings_to_cards(s_cards)
            for card in cards:
                print(f"Card: Count = {card.count}, Color = {card.color}")
            convert = False

        # Check if all cards are selected
        runFlop = True
        # if len(selected_cards) == 10 and runFlop == True:
        if len(selected_cards) == 2 * num_players and runFlop:

            # Generate and display 5 random cards in the middle of the table
            random_cards = dropDownMenu.get_random_cards([card[1] for card in selected_cards], dropdown_menu.card_options)
            for i, card_name in enumerate(random_cards):
                card_image = dropdown_menu.card_images[card_name]
                card_position = (540 - 125 + i * 50, 320)  # Adjusted position for 5 cards
                resized_card_image = pygame.transform.scale(card_image, (50, 80))
                screen.blit(resized_card_image, card_position)
            runFlop = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
