import pygame

# Initialize Pygame
pygame.init()

# Set up window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Texas Hold'em")

# Load background image
background_image = pygame.image.load("Green_Table.png").convert()
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 36)

# Dropdown options
options = ['1', '2', '3', '4', '5']
selected_option_index = 0

# Dropdown properties
dropdown_width = 100
dropdown_height = 50
dropdown_rect = pygame.Rect(300, 200, dropdown_width, dropdown_height)
dropdown_open = False

# Button properties
button_width = 50
button_height = 50
button_rect_left = pygame.Rect(250, 200, button_width, button_height)
button_rect_right = pygame.Rect(400, 200, button_width, button_height)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect_left.collidepoint(event.pos):
                selected_option_index = max(0, selected_option_index - 1)
            elif button_rect_right.collidepoint(event.pos):
                selected_option_index = min(len(options) - 1, selected_option_index + 1)

    # Draw the background image
    window.blit(background_image, (0, 0))

    # Draw the "Title" label
    text_surface = font.render("Texas Hold'em", True, BLACK)
    window.blit(text_surface, (250, 100))

    # Draw the "Left" label
    text_surface = font.render("# of computer players", True, BLACK)
    window.blit(text_surface, (250, 150))

    # Draw the left button
    pygame.draw.rect(window, GRAY, button_rect_left)
    pygame.draw.rect(window, BLACK, button_rect_left, 2)
    text_surface = font.render("<", True, BLACK)
    window.blit(text_surface, text_surface.get_rect(center=button_rect_left.center))

    # Draw the right button
    pygame.draw.rect(window, GRAY, button_rect_right)
    pygame.draw.rect(window, BLACK, button_rect_right, 2)
    text_surface = font.render(">", True, BLACK)
    window.blit(text_surface, text_surface.get_rect(center=button_rect_right.center))

    # Draw the dropdown button
    pygame.draw.rect(window, GRAY, dropdown_rect)
    pygame.draw.rect(window, BLACK, dropdown_rect, 2)
    text_surface = font.render(options[selected_option_index], True, BLACK)
    window.blit(text_surface, text_surface.get_rect(center=(dropdown_rect.centerx, dropdown_rect.centery - 10)))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
