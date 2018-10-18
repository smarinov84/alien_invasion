import pygame

class Ship():

    def __init__(self, screen, game_settings):
        """Initialize the ship and set its starting position"""
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp') # contains the surface representing the ship
        self.rect = self.image.get_rect() # rect = rectangles, this is what pygame treats all elements as
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center (in order to move faster
        # across the screen
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag"""

        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Update rect object from self.center (this back and forth is required
        # given that rect doesnt support decimals
        self.rect.centerx = self.center


    def center_ship(self):
        """Center a ship to the middle of the screen"""
        self.center = self.rect.centerx
