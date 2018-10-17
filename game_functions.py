import sys
import pygame

from bullet import Bullet
from alien import Alien

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


def update_screen(game_settings, screen, ship, bullets, aliens):
    """Update images on the screen and flip to the new screen
    :param bullets: sprite of bullet objects
    :param game_settings: general settings for the game
    :param screen: screen object for the game
    :param ship: ship object
    """
    # Redraw the screen
    screen.fill(game_settings.bg_color)

    # Redraw all bullets behind ship abd aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the ship on the screen
    ship.blitme()
    # Draw the alien on the screen
    aliens.draw(screen)

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


def update_aliens(game_settings, aliens):
    """Update the position of all aliens in the fleet"""
    # Check if the fleet is at the screen's edges
    check_fleet_edges(game_settings, aliens)
    aliens.update()


def fire_bullet(game_settings, screen, ship , bullets):
    """Create bullets to be displayed on the screen if user pressed SPACE bar
    :param game_settings:
    :param screen:
    :param ship:
    :param bullets:
    """
    # Create a new bullet and add it to the bullets group if we haven't
    # Reached the maximum bullets allowed
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(game_settings, screen, aliens, ship):
    """Create a full fleet of aliens
    :param game_settings: 
    :param screen: 
    :param aliens: 
    """
    # Create an alien and find the number of aliens in a row
    # Spacing between aliens is equal to one alien width
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_row(game_settings, alien.rect.height,
                                 ship.rect.height)

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
            create_alien(game_settings, screen, alien_number, aliens,
                         row_number)


def get_number_aliens_x(game_settings, alien_width):
    """
    Determine the number of aliens that can fit on a screen
    :rtype: object
    :param game_settings:
    :param screen:
    """
    available_space_x = game_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))

    return number_aliens_x


def create_alien(game_settings, screen, alien_number, aliens, row_number):
    """Create an alien and add it to a row
    :param game_settings:
    :param screen:
    :param alien_number:
    :param aliens:
    """
    # Create an alien and place it in the row
    alien = Alien(screen, game_settings)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width) * alien_number

    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height) * row_number
    aliens.add(alien)


def get_number_row(game_settings, alien_height, ship_height):
    """Determine the number of alien rows that fit on the screen
    :rtype: int
    :param game_settings: 
    :param alien_height: 
    :param ship_height: 
    :return number_rows:
    """
    available_space_y = (game_settings.screen_height - (3 * alien_height)
                         - ship_height)

    number_rows = int(available_space_y / (2 * alien_height))
    
    return number_rows


def check_fleet_edges(game_settings, aliens):
    """Respond appropriately if any aliens have reached the screen's edges
    :param game_settigs:
    :param aliens:
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet and change direction
    :param game_settings:
    :param aliens:
    """
    for alien in aliens.sprites():
        alien.rect.y += game_settings.alien_fleet_drop_speed
    game_settings.alien_fleet_direction *= -1
