
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
convert = False
num_players = int(sys.argv[1])
runFlop= False
current_flop_cards=None
win_rates= None
winner_message=None



pygame.display.set_caption("Texas Hold em Odds Calculator")

card_images_path = "PlayingCards/PNG-cards-1.3/"
# Load the image
pokertable_image = pygame.image.load("pokerTableLight.png")

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


run_flop_button_width = 150
run_flop_button_height = 50
run_flop_button_rect = pygame.Rect(250, 650, run_flop_button_width, run_flop_button_height)  # Positioned next to the reset button

calculation_button_width = 150
calculation_button_height = 50
calculation_button_rect = pygame.Rect(450, 650, calculation_button_width, calculation_button_height)  # Positioned next to the Run Flop button


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif run_flop_button_rect.collidepoint(event.pos):
                random_cards = dropDownMenu.get_random_cards([card[1] for card in selected_cards], dropdown_menu.card_options)
                current_flop_cards = [(dropdown_menu.card_images[card_name], card_name) for card_name in random_cards]
                s_cards = [card_name for _, card_name in selected_cards]  # Extract card names
                cards = convert_strings_to_cards(s_cards)
                # Constructing each player's hand combined with the community cards
                player_hands = [cards[i * 2:(i + 1) * 2] for i in range(num_players)]
                community_cards = [convert_to_card(card_name) for _, card_name in current_flop_cards]
                hands_with_community = [hand + community_cards for hand in player_hands]
                # Rank all hands and find the highest ranking hand
                player_results = [card.Ranker.rank_all_hands([hand], return_all=False) for hand in hands_with_community]
                highest_rank = max(player_results, key=lambda x: (x[0],x[1]))  # Find the highest rank
                winner_index = player_results.index(highest_rank)  # Get the index of the winning hand
                winner_message = f"Player {winner_index + 1} is the winner with the highest rank!"
            elif calculation_button_rect.collidepoint(event.pos):
                s_cards = [card_name for _, card_name in selected_cards]  # Extract card names
                cards = convert_strings_to_cards(s_cards)
                win_rates = card.simulate_poker_games(cards, num_players)
                convert = False
            else:
                dropdown_menu.handle_events(event)
        elif event.type == pygame.MOUSEMOTION:
            # Move the buttons slightly down if the mouse hovers over them
            if reset_button_rect.collidepoint(event.pos):
                reset_button_rect.y = 655
            else:
                reset_button_rect.y = 650  # Reset to original position

            if run_flop_button_rect.collidepoint(event.pos):
                run_flop_button_rect.y = 655
            else:
                run_flop_button_rect.y = 650  # Reset to original position

            if calculation_button_rect.collidepoint(event.pos):
                calculation_button_rect.y = 655
            else:
                calculation_button_rect.y = 650  # Reset to original position

        else:
            dropdown_menu.handle_events(event)

    screen.blit(pokertable_image, (-100, 0))
    dropdown_menu.draw()

    pygame.draw.rect(screen, (255, 0, 0), reset_button_rect, border_radius=10)  # Draw a red reset button
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Reset", True, (255, 255, 255))
    screen.blit(text_surface, (reset_button_rect.x + 20, reset_button_rect.y + 10))

    pygame.draw.rect(screen, (0, 255, 0), run_flop_button_rect, border_radius=10)  # Draw a green Run Flop button
    text_surface = font.render("Run Flop", True, (255, 255, 255))
    screen.blit(text_surface, (run_flop_button_rect.x + 20, run_flop_button_rect.y + 10))

    pygame.draw.rect(screen, (0, 0, 255), calculation_button_rect, border_radius=10)  # Draw a blue Calculation button
    text_surface = font.render("Calculate", True, (255, 255, 255))
    screen.blit(text_surface, (calculation_button_rect.x + 20, calculation_button_rect.y + 10))

    if winner_message:  # Check if there's a winner message to display
        font = pygame.font.Font(None, 36)
        text_surface = font.render(winner_message, True, (0, 0, 0))  # Black text
        # Position the text at the top center of the screen
        # Calculate the position so that the text is centered
        text_rect = text_surface.get_rect(center=(screen.get_width()/2, 90))
        screen.blit(text_surface, text_rect)


    # Check if a card is selected
    selected_card = dropdown_menu.get_selected_card()
    selected_card_image = dropdown_menu.get_selected_card_image()

    if selected_card:
        if len(selected_cards) < num_players * 2:
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
            screen.blit(win_rate_text, (785, 490))

        if i == 9:
            win_rate_text = font.render("Win Rate", True, (255, 255, 255))  # White text
            screen.blit(win_rate_text, (410, 490))

        if ((i % 2) != 0 and (i != 7) and (i != 9)):  # Display win rate text next to the hand
            #winRatePosition = ((card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]), (card_position[0] + 50, card_position[1]))
            win_rate_text = font.render("Win Rate", True, (255, 255, 255)) # White text
            screen.blit(win_rate_text, (card_position[0] + 60, card_position[1]))

    if len(selected_cards) == (num_players*2) and convert == True:
        cards = convert_strings_to_cards(s_cards)
        win_rates = card.simulate_poker_games(cards,num_players)
    # Check if all cards are selected



    # if len(selected_cards) == num_players*2:
    #     winRatePositions = ((400, 165), (775, 165), (940, 335), (775, 505), (400, 505))
    #     # Ensure you do not exceed the length of winRatePositions or win_rates
    #     num_players = min(len(winRatePositions), len(win_rates))
    #
    #     for i in range(num_players):  # Loop through each player
    #         player_hand_index = i * 2 + 1  # The index of the second card of each player
    #         card_position = positionValues[player_hand_index]
    #
    #         if win_rates:  # Ensure win_rates have been calculated
    #             win_rate_text = font.render(f"{win_rates[i] * 100:.2f}%", True, (255, 255, 255))  # White text
    #         else:
    #             win_rate_text = font.render("Calculating...", True, (255, 255, 255))  # Before win rates are calculated
    #
    #         # Set the win rate position based on predefined positions
    #         win_rate_position = winRatePositions[i]
    #
    #         # Display the win rate text at the specified position on the screen
    #         screen.blit(win_rate_text, win_rate_position)
    if win_rates:
        winRatePositions = ((420, 175), (795, 175), (960, 345), (795, 515), (420, 515))# Only attempt to display win rates if they've been calculated
        num_players = min(len(winRatePositions), len(win_rates))
        for i in range(num_players):
            player_hand_index = i * 2 + 1
            card_position = positionValues[player_hand_index]
            win_rate_text = font.render(f"{win_rates[i] * 100:.2f}%", True, (255, 255, 255))
            win_rate_position = winRatePositions[i]
            screen.blit(win_rate_text, win_rate_position)




    if current_flop_cards:
        for i, (card_image, card_name) in enumerate(current_flop_cards):
            card_position = (540 - 125 + i * 50, 320)  # Adjusted position for 5 cards
            resized_card_image = pygame.transform.scale(card_image, (50, 80))
            screen.blit(resized_card_image, card_position)




    pygame.display.flip()
    clock.tick(60)

pygame.quit()

