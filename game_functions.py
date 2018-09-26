import sys
import pygame

def check_events(ship):
    """Respond to keypresses and mouse events
    :rtype: none
    :param ship: ship object
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ship):
    """Checks if a key has been pressed and accordingly sets the
    ship moving_right/moving_left flag
    :param event:
    :param ship:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True


def check_keyup_events(event, ship):
    """Checks if a key has been released and accordingly sets the
    ship moving_right/moving_left flag
    :param event:
    :param ship:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(game_settings, screen, ship):
    """Update images on the screen and flip to the new screen
    :param game_settings: general settings for the game
    :param screen: screen object for the game
    :param ship: ship object
    """

    # Redraw the screen
    screen.fill(game_settings.bg_color)

    # Draw the ship on the screen
    ship.blitme()

    # Make the most recently drawn screen visible
    pygame.display.flip()