import pygame
import subprocess

# Initialize Pygame
pygame.init()

# Set up window
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Texas Hold'em")

# Load background image
background_image = pygame.image.load("pokerTable.png").convert()
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font1 = pygame.font.Font(None, 60)
font2 = pygame.font.Font(None, 36)

# Dropdown options
options = ['1', '2', '3', '4', '5']
selected_option_index = 0

# Button properties
button_width = 50
button_height = 50
window_center_x = window_width // 2
window_center_y = window_height // 2
button_rect_left = pygame.Rect(window_center_x - 100, window_center_y + 50, button_width, button_height)
button_rect_right = pygame.Rect(window_center_x + 50, window_center_y + 50, button_width, button_height)

# Start button properties
start_button_width = 150
start_button_height = 50
start_button_rect = pygame.Rect(window_center_x - start_button_width // 2, window_center_y + 150, start_button_width, start_button_height)

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect_left.collidepoint(event.pos):
                # If the left arrow is clicked, decrement the selected index
                selected_option_index = (selected_option_index - 1) % len(options)
            elif button_rect_right.collidepoint(event.pos):
                # If the right arrow is clicked, increment the selected index
                selected_option_index = (selected_option_index + 1) % len(options)
            elif start_button_rect.collidepoint(event.pos):
                # If the start button is clicked, open "tableModel.py" using subprocess
                subprocess.Popen(["python", "tableModel.py"])

    # Draw the background image
    window.blit(background_image, (0, 0))

    # Draw the "Title" label centered
    text_surface = font1.render("Texas Hold'em", True, BLACK)
    text_rect = text_surface.get_rect(center=(window_center_x, window_center_y - 50))
    window.blit(text_surface, text_rect)

    # Draw the "players" label centered
    text_surface = font2.render("# of computer players", True, BLACK)
    text_rect = text_surface.get_rect(center=(window_center_x, window_center_y))
    window.blit(text_surface, text_rect)

    # Draw the dropdown button
    dropdown_width = 100
    dropdown_height = 50
    dropdown_rect = pygame.Rect(window_center_x - dropdown_width // 2, window_center_y + 50, dropdown_width, dropdown_height)
    pygame.draw.rect(window, GRAY, dropdown_rect)
    pygame.draw.rect(window, BLACK, dropdown_rect, 2)
    text_surface = font2.render(options[selected_option_index], True, BLACK)
    text_rect = text_surface.get_rect(center=(dropdown_rect.centerx, dropdown_rect.centery))
    window.blit(text_surface, text_rect)

    # Draw the left button
    pygame.draw.rect(window, GRAY, button_rect_left)
    pygame.draw.rect(window, BLACK, button_rect_left, 2)
    text_surface = font2.render("<", True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect_left.center)
    window.blit(text_surface, text_rect)

    # Draw the right button
    pygame.draw.rect(window, GRAY, button_rect_right)
    pygame.draw.rect(window, BLACK, button_rect_right, 2)
    text_surface = font2.render(">", True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect_right.center)
    window.blit(text_surface, text_rect)

    # Draw the start button
    pygame.draw.rect(window, GRAY, start_button_rect)
    pygame.draw.rect(window, BLACK, start_button_rect, 2)
    text_surface = font2.render("Start", True, BLACK)
    text_rect = text_surface.get_rect(center=start_button_rect.center)
    window.blit(text_surface, text_rect)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
