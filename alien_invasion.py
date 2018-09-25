import sys
import pygame

from settings import Settings
from ship import Ship

def run_game():
    # Initialize and create the screen object
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(game_settings.screen_dimensions())
    pygame.display.set_caption('Alien Invasion')

    # Set the background color
    bg_color = (230, 230, 230)

    # Initialize objects
    ship = Ship(screen)

    # Start the main loop for the game
    # This is an event loop that manages screen updates when users perform
    # event actions
    while True:

        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Redraw the screen during each pass through the loop
        screen.fill(game_settings.bg_color)

        # Draw the ship on the screen
        ship.blitme()

        # Make the most recently drawn screen visible
        pygame.display.flip()

run_game()