import pygame
from dropDown import dropDownMenu
from pygame.locals import *


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("Texas Hold em Odds Calculator")

card_images_path = "/Users/vincentschetroma/Desktop/03-Texas-Holdem/PlayingCards/PNG-cards-1.3/"
# Load the image
pokertable_image = pygame.image.load("pokertable.png")

# Resize the image to fit the screen
pokertable_image = pygame.transform.scale(pokertable_image, (1280, 720))

dropdown_menu = dropDownMenu(card_images_path, screen)

while running:
    # Poll for events
    # pygame.QUIT event means the user clicked X to close your window

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("yes")
            running = False
        else:
            dropdown_menu.handle_events(event)

    # Display the loaded image
    screen.blit(pokertable_image, (0, 0))
    dropdown_menu.draw()

    # Flip() the display to put your work on screen

    selected_card = dropdown_menu.get_selected_card()
    selected_card_image = dropdown_menu.get_selected_card_image()

    if selected_card:
        positionValues = ((500,150), (550,150))
        cordX = 500
        cordY = 150
        font = pygame.font.Font(None,36)
        #text_surface = font.render(f"Selected Card: {selected_card}", True, (0,0,0))
        #screen.blit(text_surface, (300,200))
        resized_card_image = pygame.transform.scale(selected_card_image, (60, 90))  # Resize the image
        screen.blit(resized_card_image, (cordX, cordY))  # Blit the resized image to the screen
        #screen.blit(selected_card, selected_card.get_rect())

    pygame.display.flip()
    clock.tick(60)  # Limits FPS to 60

pygame.quit()




