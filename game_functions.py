import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_events(game_settings, screen, ship,  bullets, stats, play_button,
                 aliens, sb):
    """Respond to keypresses and mouse events
    :param sb: Scoreboard
    :param play_button:
    :param aliens: Alien
    :param stats: GameStats
    :param game_settings: Settings
    :param screen:
    :param bullets:
    :rtype: none
    :param ship: Ship
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets,
                                 stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y,
                              game_settings, screen, ship, aliens, bullets, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, game_settings,
                      screen, ship, aliens, bullets, sb):
    """Check if the user pressed the play button and if so start the game
    :param sb: Scoreboard
    :param play_button:
    :param game_settings:
    :param screen:
    :param ship: Ship
    :param aliens: Alien
    :param bullets:
    :param stats: GameStats
    :param play_button:
    :param mouse_x:
    :param mouse_y:
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game stats
        start_game(game_settings, screen, ship, stats, aliens, bullets, sb)

def check_keydown_events(event, game_settings, screen, ship, bullets, stats,
                         aliens, sb):
    """Checks if a key has been pressed and accordingly sets the
    ship moving_right/moving_left flag and/or fire a bullet
    :param sb: Scoreboard
    :param stats: GameStats
    :param aliens: Alien
    :param game_settings: Settings
    :param screen:
    :param bullets:
    :param event:
    :param ship: Ship
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(game_settings, screen, ship, stats, aliens, bullets, sb)


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


def update_screen(game_settings, screen, ship, bullets, aliens, stats,
                  play_button, sb):
    """Update images on the screen and flip to the new screen
    :param sb: Scoreboard
    :param stats: GameStats
    :param aliens: Alien
    :param play_button:
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

    # Draw the scoreboard information
    sb.show_score()
    sb.show_high_score()
    sb.show_level()
    sb.show_ships()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(bullets, aliens, game_settings, screen, ship, stats, sb):
    """Update bullets shown on the screen
    :param aliens: Alien
    :param game_settings: Settings
    :param screen:
    :param ship: Ship
    :param stats: GameStats
    :param sb: Scoreboard
    :param bullets: Bullet
    """
    # Update bullet position
    bullets.update()  # automatically invokes bullet.update for each sprite

    # Get rid of bullets that have disappeared from screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets,
                                  stats, sb)


def check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets,
                                  stats, sb):
    """Handles the check for determining whether a bullet has hit an alien ship
    :param ship: Ship
    :param stats: GameStats
    :param sb: Scoreboard
    :param game_settings: Settings
    :param screen:
    :param aliens: Aliens
    :param bullets: Bullets
    """
    # Check for any bullets that have hit aliens
    # If so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        game_settings.increase_speed()
        # Increment the level
        stats.level += 1
        sb.prep_level()

        # Create the new fleet and star the next level
        create_fleet(game_settings, screen, aliens, ship)


def update_aliens(game_settings, aliens, ship, stats, screen, bullets, sb):
    """Update the position of all aliens in the fleet
    :param game_settings: Settings
    :param aliens: Alien
    :param ship: Ship
    :param stats: GameStats
    :param screen:
    :param bullets:
    :param sb: Scoreboard
    """
    # Check if the fleet is at the screen's edges
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, ship, aliens, bullets, sb)

    # Look if any aliens made it to the bottom of the screen
    check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets,
                        sb)


def ship_hit(game_settings, stats, screen, ship, aliens, bullets, sb):
    """Respond to ship being hit by alien
    :param sb: Scoreboard
    :param game_settings: Settings
    :param stats: GameStats
    :param screen:
    :param ship: Ship
    :param aliens: Alien
    :param bullets:
    """
    if stats.ship_left > 0:
        # Decrement ships_left
        stats.ship_left -= 1

        # Update Scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(game_settings,screen, aliens, ship)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen
    :param sb: Scoreboard
    :param game_settings: Settings
    :param stats: GameStats
    :param screen:
    :param ship: Ship
    :param aliens: Aliens
    :param bullets:
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same way as if a ship was hit
            ship_hit(game_settings, stats, screen, ship, aliens, bullets, sb)
            break

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


def start_game(game_settings, screen, ship, stats, aliens, bullets, sb):
    """Kicks of the game based on user input either through keyboard key
    or mouse press"""
    # Reset the game stats
    game_settings.initialize_dynamic_settings()
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship
    create_fleet(game_settings, screen, aliens, ship)
    ship.center_ship()


def check_high_score(stats, sb):
    """"Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
