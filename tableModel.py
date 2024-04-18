import pygame
from dropDown import dropDownMenu
from pygame.locals import *
import random

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("Texas Hold em Odds Calculator")

card_images_path = "/Users/vincentschetroma/Desktop/03-Texas-Holdem/PlayingCards/PNG-cards-1.3/"
# Load the image
pokertable_image = pygame.image.load("pokertable.png")

# Resize the image to fit the screen
pokertable_image = pygame.transform.scale(pokertable_image, (1280, 720))

dropdown_menu = dropDownMenu(card_images_path, screen)
selected_cards = []  # List to hold selected cards and their positions

random_cards = []  # List to hold random cards

# Generate and store 5 random cards
if len(selected_cards) == 10:
    random_cards = dropDownMenu.get_random_cards([card[1] for card in selected_cards], dropdown_menu.card_options)

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

        # Reset the selected card in the drop-down menu
        dropdown_menu.selected_card = None

    # Display selected cards on the screen
    for i, (card_image, card_name) in enumerate(selected_cards):
        positionValues = ((300,150), (350,150), (675,150), (725,150), (840,320), (890,320), (725,490), (675,490), (350,490), (300,490))        #positions for cards
        card_position = positionValues[i]  

        resized_card_image = pygame.transform.scale(card_image, (50, 80))
        screen.blit(resized_card_image, card_position)

    # Check if all cards are selected
    if len(selected_cards) == 10 and not random_cards:
        # Generate and display 5 random cards in the middle of the table
        random_cards = dropDownMenu.get_random_cards([card[1] for card in selected_cards], dropdown_menu.card_options)
        for i, card_name in enumerate(random_cards):
            card_image = dropdown_menu.card_images[card_name]
            card_position = (540 - 125 + i * 50, 320)  # Adjusted position for 5 cards
            resized_card_image = pygame.transform.scale(card_image, (50, 80))
            screen.blit(resized_card_image, card_position)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

