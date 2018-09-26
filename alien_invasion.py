import pygame

from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    # Initialize and create the screen object
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(game_settings.screen_dimensions())
    pygame.display.set_caption('Alien Invasion')

    # Initialize objects
    ship = Ship(screen, game_settings)

    # Start the main loop for the game
    # This is an event loop that manages screen updates when users perform
    # event actions
    while True:

        # Watch for keyboard and mouse events
        gf.check_events(ship)

        # Reflect any ship movement
        ship.update()

        # Redraw the screen during each pass through the loop and reflect
        # all event changes
        gf.update_screen(game_settings, screen, ship)

run_game()