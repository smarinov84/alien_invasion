import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that represents a single alien in the fleet"""

    def __init__(self, screen, game_settings):
        """Initialize the alien and set its starting position"""
        super(Alien, self).__init__()
        self.game_settings = game_settings
        self.screen = screen

        #load the alien image and setup its rect objects
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # align the alien image on the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store a decimal value for the alien's center (in order to move faster
        # across the screen
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)


    def update(self):
        """Move alien to the right"""
        self.x += (self.screen.alien_speed_factor *
                   self.screen.alien_fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        """Return True if alien is at the edge of a screen
        :rtype: boolean
        """
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

