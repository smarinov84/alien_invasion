import sys
import pygame

from bullet import Bullet

def check_events(game_settings, screen, ship,  bullets):
    """Respond to keypresses and mouse events
    :param game_settings:
    :param screen:
    :param bullets:
    :rtype: none
    :param ship: ship object
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Checks if a key has been pressed and accordingly sets the
    ship moving_right/moving_left flag and/or fire a bullet
    :param game_settings:
    :param screen:
    :param bullets:
    :param event:
    :param ship:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


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


def update_screen(game_settings, screen, ship, bullets, alien):
    """Update images on the screen and flip to the new screen
    :param bullets: sprite of bullet objects
    :param game_settings: general settings for the game
    :param screen: screen object for the game
    :param ship: ship object
    """

    # Redraw the screen
    screen.fill(game_settings.bg_color)

    # Draw the ship on the screen
    ship.blitme()
    # Draw the alien on the screen
    alien.blitme()

    # Redraw all bullets behind ship abd aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(bullets):
    """Update bullets shown on the screen
    :param bullets:
    """
    # Update bullet position
    bullets.update()  # automatically invokes bullet.update for each sprite

    # Get rid of bullets that have disappeared from screen
    for bullet in bullets.copy():
        if bullet.bullet_rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(game_settings, screen, ship ,bullets):
    """Create bullets to be displayed on the screen if user pressed SPACE bar"""
    # Create a new bullet and add it to the bullets group if we haven't
    # Reached the maximum bullets allowed
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)