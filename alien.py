import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that represents a single alien in the fleet"""

    def __init__(self, screen, game_settings):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.game_settings = game_settings
        self.screen = screen

        #load the alien image and setup its rect objects
        self.image = pygame.image.load('images/alien.bmp')
        self.alien_rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # align the alien image on the screen
        self.alien_rect.x = self.alien_rect.width
        self.alien_rect.y = self.alien_rect.height

        # Store a decimal value for the alien's center (in order to move faster
        # across the screen
        self.x = float(self.alien_rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.alien_rect)