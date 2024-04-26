import pygame
import subprocess

# Initialize Pygame
pygame.init()

# Set up window
window_width = 1080
window_height = 720
window = pygame.display.set_mode((window_width, window_height))

# Load caption image
title_image = pygame.image.load("holdem.png")

# Set up window caption
pygame.display.set_icon(title_image)

# Colors for light mode
LIGHT_MODE = {
    "background": (255, 255, 255),
    "text": (0, 0, 0),
    "button": (255, 255, 255),
    "button_border": (0, 0, 0),
}

# Colors for dark mode
DARK_MODE = {
    "background": (30, 30, 30),
    "text": (255, 255, 255),
    "button": (50, 50, 50),
    "button_border": (255, 255, 255),
}

# Fonts
font1 = pygame.font.Font(None, 60)
font2 = pygame.font.Font(None, 36)

# Dropdown options
options = ['1', '2', '3', '4', '5']
selected_option_index = 0

# Calculate the center of the window
window_center_x = window_width // 2
window_center_y = window_height // 2

# Dropdown properties
dropdown_width = 100
dropdown_height = 50
dropdown_rect = pygame.Rect(window_center_x - dropdown_width // 2, window_center_y * 1.3 - dropdown_height // 2, dropdown_width, dropdown_height)
dropdown_open = False

# Button properties
button_width = 50
button_height = 50
button_rect_left = pygame.Rect(window_center_x - 150, window_center_y * 1.3 - button_height // 2, button_width, button_height)
button_rect_right = pygame.Rect(window_center_x + 100, window_center_y * 1.3- button_height // 2, button_width, button_height)

# Start button properties
start_button_width = 150
start_button_height = 50
start_button_rect = pygame.Rect(window_center_x - start_button_width // 2, window_center_y + 100 * 1.5, start_button_width, start_button_height)
button_radius = 10  # Define the radius for rounded corners

# Variable to store number of players
num_players = 1

# Dark mode toggle
dark_mode = False

# Load background image based on initial mode
if dark_mode:
    background_image = pygame.image.load("pokerTableDark.png").convert()
else:
    background_image = pygame.image.load("pokerTableLight.png").convert()

background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Function to toggle dark mode
def toggle_dark_mode():
    global dark_mode, background_image
    dark_mode = not dark_mode
    if dark_mode:
        # Set colors to dark mode
        window.fill(DARK_MODE["background"])
        background_image = pygame.image.load("pokerTableDark.png").convert()
    else:
        # Set colors to light mode
        window.fill(LIGHT_MODE["background"])
        background_image = pygame.image.load("pokerTableLight.png").convert()
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

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
                # If the start button is clicked, store the number of players and open "tableModel.py" using subprocess
                num_players = int(options[selected_option_index])
                print("Number of players homepage:", num_players)
                subprocess.Popen(["python", "tableModel.py", str(num_players)], stdin=subprocess.PIPE)
            elif dark_mode_toggle_rect.collidepoint(event.pos):
                # If the dark mode toggle is clicked, toggle dark mode
                toggle_dark_mode()

    # Draw the background image
    window.blit(background_image, (0, 0))

    # Draw the title image centered
    title_rect = title_image.get_rect(center=(window_width // 2, window_height // 2.7))
    window.blit(title_image, title_rect)

    # Draw the "players" label centered
    text_surface = font2.render("Number of computer players", True, LIGHT_MODE["text"] if not dark_mode else DARK_MODE["text"])
    text_rect = text_surface.get_rect(center=(window_center_x, window_height // 1.75))
    window.blit(text_surface, text_rect)

    # Draw the dropdown button
    pygame.draw.rect(window, LIGHT_MODE["button"] if not dark_mode else DARK_MODE["button"], dropdown_rect)
    pygame.draw.rect(window, LIGHT_MODE["button_border"] if not dark_mode else DARK_MODE["button_border"], dropdown_rect, 2)
    text_surface = font2.render(options[selected_option_index], True, LIGHT_MODE["text"] if not dark_mode else DARK_MODE["text"])
    text_rect = text_surface.get_rect(center=(dropdown_rect.centerx, dropdown_rect.centery))
    window.blit(text_surface, text_rect)

    # Draw the left button
    pygame.draw.rect(window, LIGHT_MODE["button"] if not dark_mode else DARK_MODE["button"], button_rect_left)
    pygame.draw.rect(window, LIGHT_MODE["button_border"] if not dark_mode else DARK_MODE["button_border"], button_rect_left, 2)
    text_surface = font2.render("<", True, LIGHT_MODE["text"] if not dark_mode else DARK_MODE["text"])
    text_rect = text_surface.get_rect(center=button_rect_left.center)
    window.blit(text_surface, text_rect)

    # Draw the right button
    pygame.draw.rect(window, LIGHT_MODE["button"] if not dark_mode else DARK_MODE["button"], button_rect_right)
    pygame.draw.rect(window, LIGHT_MODE["button_border"] if not dark_mode else DARK_MODE["button_border"], button_rect_right, 2)
    text_surface = font2.render(">", True, LIGHT_MODE["text"] if not dark_mode else DARK_MODE["text"])
    text_rect = text_surface.get_rect(center=button_rect_right.center)
    window.blit(text_surface, text_rect)

    # Draw the start button
    pygame.draw.rect(window, LIGHT_MODE["button"] if not dark_mode else DARK_MODE["button"], start_button_rect, border_radius=button_radius)
    pygame.draw.rect(window, LIGHT_MODE["button_border"] if not dark_mode else DARK_MODE["button_border"], start_button_rect, 2, border_radius=button_radius)
    text_surface = font2.render("Start", True, LIGHT_MODE["text"] if not dark_mode else DARK_MODE["text"])
    text_rect = text_surface.get_rect(center=start_button_rect.center)
    window.blit(text_surface, text_rect)

    # Draw the dark mode toggle button
    dark_mode_toggle_rect = pygame.Rect(window_width - 100, 20, 80, 40)
    pygame.draw.rect(window, LIGHT_MODE["button"] if not dark_mode else DARK_MODE["button"], dark_mode_toggle_rect, border_radius=button_radius)
    pygame.draw.rect(window, LIGHT_MODE["button_border"] if not dark_mode else DARK_MODE["button_border"], dark_mode_toggle_rect, 2, border_radius=button_radius)
    text = "Dark" if dark_mode else "Light"
    text_surface = font2.render(text, True, LIGHT_MODE["text"] if not dark_mode else DARK_MODE["text"])
    text_rect = text_surface.get_rect(center=dark_mode_toggle_rect.center)
    window.blit(text_surface, text_rect)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
