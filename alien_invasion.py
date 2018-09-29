import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game()  :
    # Initialize and create the screen object
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(game_settings.screen_dimensions())
    pygame.display.set_caption('Alien Invasion')

    # Initialize objects
    ship = Ship(screen, game_settings)

    # Make a group to store bullets in
    bullets = Group()
    # Make a group of aliens
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(game_settings, screen, aliens)

    # Start the main loop for the game
    # This is an event loop that manages screen updates when users perform
    # event actions
    while True:

        # Watch for keyboard and mouse events
        gf.check_events(game_settings, screen, ship, bullets)

        # Reflect ship object movements
        ship.update()

        # Reflect the bullet objects on the screen
        gf.update_bullets(bullets)

        # Redraw the screen during each pass through the loop and reflect
        # all event changes
        gf.update_screen(game_settings, screen, ship, bullets, aliens)

run_game()