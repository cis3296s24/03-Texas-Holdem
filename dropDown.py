import pygame
import random

# Path to the card images
card_images_path = "/Users/vincentschetroma/Desktop/03-Texas-Holdem/PlayingCards/PNG-cards-1.3/"


class dropDownMenu:
    def __init__(self, card_images_path, screen):
        self.scrollbar_rect = pygame.Rect(210, 140, 20, 300)                # scroll bar variables
        self.scrollbar_handle_rect = pygame.Rect(210, 140, 20, 50)
        self.scroll_offset = 0
        self.dragging_scrollbar = False
        self.card_images_path = card_images_path
        self.screen = screen
        self.dropdown_open = False
        self.selected_card = None
        self.card_options =  [
    "2_of_clubs", "3_of_clubs", "4_of_clubs", "5_of_clubs", "6_of_clubs","7_of_clubs", "8_of_clubs", "9_of_clubs", "10_of_clubs", "Jack_of_clubs",
    "Queen_of_clubs", "King_of_clubs", "Ace_of_clubs","2_of_diamonds", "3_of_diamonds", "4_of_diamonds", "5_of_diamonds", "6_of_diamonds",
    "7_of_diamonds", "8_of_diamonds", "9_of_diamonds", "10_of_diamonds", "Jack_of_diamonds","Queen_of_diamonds", "King_of_diamonds", "Ace_of_diamonds",
    "2_of_hearts", "3_of_hearts", "4_of_hearts", "5_of_hearts", "6_of_hearts","7_of_hearts", "8_of_hearts", "9_of_hearts", "10_of_hearts", "Jack_of_hearts",
    "Queen_of_hearts", "King_of_hearts", "Ace_of_hearts","2_of_spades", "3_of_spades", "4_of_spades", "5_of_spades", "6_of_spades",
    "7_of_spades", "8_of_spades", "9_of_spades", "10_of_spades", "Jack_of_spades","Queen_of_spades", "King_of_spades", "Ace_of_spades"]
        self.card_images = {}
        for card in self.card_options:
            self.card_images[card] = pygame.image.load(f"{self.card_images_path}{card.lower()}.png")
            #self.card_images[card] = pygame.transform.scale(f"{self.card_images_path}{card.lower()}.png")
        self.dropdown_button_rect = pygame.Rect(100, 100, 100, 30)
        self.option_rects = []
# Rectangles for dropdown button and options

    def handle_events(self, event):
        """
        Handles mouse events to control the dropdown menu operations like opening the menu, selecting cards, and scrolling.

        Args:
            event (pygame.event.Event): The event to handle, typically mouse events.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.dropdown_button_rect.collidepoint(event.pos):
                    self.dropdown_open = not self.dropdown_open
                elif self.dropdown_open:
                    for i, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(event.pos):
                            self.selected_card = self.card_options[self.scroll_offset + i]
                            self.card_options.remove(self.selected_card)        #remove selected card so it cannot be chosen twice
                            
                            self.dropdown_open = False
                    if self.scrollbar_handle_rect.collidepoint(event.pos):
                        self.dragging_scrollbar = True
                        self.scrollbar_handle_offset = event.pos[1] - self.scrollbar_handle_rect.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            self.scrollbar_handle_rect.y = event.pos[1] - self.scrollbar_handle_offset
            if self.scrollbar_handle_rect.y < self.scrollbar_rect.y:
                self.scrollbar_handle_rect.y = self.scrollbar_rect.y
            elif self.scrollbar_handle_rect.y > self.scrollbar_rect.bottom - self.scrollbar_handle_rect.height:
                self.scrollbar_handle_rect.y = self.scrollbar_rect.bottom - self.scrollbar_handle_rect.height
            total_options = len(self.card_options)
            visible_options = min(total_options, 10)  # Max number of visible options
            scrollable_range = self.scrollbar_rect.height - self.scrollbar_handle_rect.height
            self.scroll_offset = int((total_options - visible_options) * ((self.scrollbar_handle_rect.y - self.scrollbar_rect.y) / scrollable_range))
            if self.scroll_offset < 0:
                self.scroll_offset = 0
            elif self.scroll_offset > total_options - visible_options:
                self.scroll_offset = total_options - visible_options

    # Draw the dropdown button

    def draw(self):
        """
        Draws the dropdown menu components including the button, options, and scrollbar on the specified screen.
        """
        pygame.draw.rect(self.screen, (200, 200, 200), self.dropdown_button_rect)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(120, 115), (130, 115), (125, 125)])
        if self.dropdown_open:
            self.option_rects = []
            for i, card in enumerate(self.card_options[self.scroll_offset:self.scroll_offset + 10]):
                option_rect = pygame.Rect(100, 140 + i * 30, 100, 30)
                self.option_rects.append(option_rect)
                pygame.draw.rect(self.screen, (200, 200, 200), option_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), option_rect, 2)
                font = pygame.font.Font(None, 24)
                text_surface = font.render(card, True, (0, 0, 0))
                self.screen.blit(text_surface, (option_rect.x + 5, option_rect.y + 5))
        # Draw scrollbar
            pygame.draw.rect(self.screen, (200, 200, 200), self.scrollbar_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.scrollbar_rect, 2)
            handle_pos = self.scrollbar_rect.y + (self.scrollbar_rect.height - self.scrollbar_handle_rect.height) * (self.scroll_offset / (len(self.card_options) - 10))
            self.scrollbar_handle_rect.y = handle_pos
            pygame.draw.rect(self.screen, (100, 100, 100), self.scrollbar_handle_rect)

    # Display the selected card (for demonstration purposes)
    def get_selected_card(self):
        """
        Returns the name of the currently selected card.

        Returns:
            str or None: The name of the selected card or None if no card is selected.
        """
        return self.selected_card


    def get_selected_card_image(self):
        """
        Retrieves the Pygame image surface associated with the selected card.

        Returns:
            pygame.Surface or None: The Pygame surface for the selected card image, or None if no card is selected.
        """
        return self.card_images.get(self.selected_card)     #gets image from card_images array

    def get_random_cards(selected_cards, card_options):
        """
        Selects 5 random cards from available options excluding already selected cards.

        Args:
            selected_cards (list[str]): A list of card names that are already selected.
            card_options (list[str]): A list of all possible card names.

        Returns:
            list[str]: A list of 5 randomly selected card names.
        """
        # Filter out selected cards from the card options
        available_cards = [card for card in card_options if card not in selected_cards]
        # Select 5 random cards from the available cards
        random_cards = random.sample(available_cards, 5)
        return random_cards