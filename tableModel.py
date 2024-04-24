
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
num_players = int(sys.argv[1])
runFlop= True

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
        'Clubs': 1, 'Diamonds': 2, 'Hearts': 3, 'Spades': 4
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





# Generate and store 5 random cards
if len(selected_cards) == 10:
    random_cards = dropDownMenu.get_random_cards([card[1] for card in selected_cards], dropdown_menu.card_options)

font = pygame.font.Font(None, 24)  # Font for the text

# Reset button properties
reset_button_width = 150
reset_button_height = 50
reset_button_rect = pygame.Rect(50, 650, reset_button_width, reset_button_height)  # Positioned at the bottom left


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button_rect.collidepoint(event.pos):
                # Terminate Pygame and current script
                pygame.quit()
                sys.exit()  # Ensure the current script stops
            else:
                # Handle other mouse button events, such as those for the dropdown menu
                dropdown_menu.handle_events(event)
        else:
            # Handle non-mouse button events
            dropdown_menu.handle_events(event)

    screen.blit(pokertable_image, (-100, 0))
    dropdown_menu.draw()

    pygame.draw.rect(screen, (255, 0, 0), reset_button_rect)  # Draw a red reset button
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Reset", True, (255, 255, 255))
    screen.blit(text_surface, (reset_button_rect.x + 20, reset_button_rect.y + 10))

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

        if i == 7:
            win_rate_text = font.render("Win Rate", True, (255, 255, 255))  # White text
            screen.blit(win_rate_text, (775, 490))

        if i == 9:
            win_rate_text = font.render("Win Rate", True, (255, 255, 255))  # White text
            screen.blit(win_rate_text, (400, 490))

        if ((i % 2) != 0 and (i != 7) and (i != 9)):  # Display win rate text next to the hand
            #winRatePosition = ((card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]))
            win_rate_text = font.render("Win Rate", True, (255, 255, 255)) # White text
            screen.blit(win_rate_text, (card_position[0] + 50, card_position[1]))

    if len(selected_cards) == (num_players*2) and convert == True:
        cards = convert_strings_to_cards(s_cards)
        win_rates = card.simulate_poker_games(cards,num_players)
    # Check if all cards are selected



    if len(selected_cards) == num_players*2:
        winRatePositions = ((400, 165), (775, 165), (940, 335), (775, 505), (400, 505))
        # Ensure you do not exceed the length of winRatePositions or win_rates
        num_players = min(len(winRatePositions), len(win_rates))

        for i in range(num_players):  # Loop through each player
            player_hand_index = i * 2 + 1  # The index of the second card of each player
            card_position = positionValues[player_hand_index]

            if win_rates:  # Ensure win_rates have been calculated
                win_rate_text = font.render(f"{win_rates[i] * 100:.2f}%", True, (255, 255, 255))  # White text
            else:
                win_rate_text = font.render("Calculating...", True, (255, 255, 255))  # Before win rates are calculated

            # Set the win rate position based on predefined positions
            win_rate_position = winRatePositions[i]

            # Display the win rate text at the specified position on the screen
            screen.blit(win_rate_text, win_rate_position)




    if len(selected_cards) == num_players*2 and runFlop == True:
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

