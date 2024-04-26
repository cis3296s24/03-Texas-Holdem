import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game Instructions")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Instructions text
instructions_text = [
    "Game Instructions:",
    "This is NOT a traditional poker game simulator.",
    "This is a learning tool to calculate favorable outcomes.",
    "User can:",
    "- Customize different hands of computer player(s)",
    "- Reset game, run flop, or generate winning rates",

]
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen
    window.fill(WHITE)

    # Render instructions text
    y_offset = 100
    for line in instructions_text:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(window_width // 2, y_offset))
        window.blit(text_surface, text_rect)
        y_offset += 50

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
