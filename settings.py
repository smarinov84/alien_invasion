import sys

class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""

        if sys.platform.title() == 'Darwin':  # Mac OS
            # Platform specific screen settings
            self.screen_width = 1100
            self.screen_height = 600

            # Platform specific Ship settings
            self.ship_speed_factor = 7.5

            # Platform specific Bullet settings
            self.bullet_speed_factor = 10.0

        else:
            # Platform specific screen settings
            self.screen_width = 1200
            self.screen_height = 800

            # Platform specific Ship settings
            self.ship_speed_factor = 1.0

            # Platform specific Bullet settings
            self.bullet_speed_factor = 1.5

        # General screen settings
        self.bg_color = (230, 230, 230)

        # General Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings


    def screen_dimensions(self):
        """
        Returns the predefined screen dimensions as a tuple
        :rtype: tuple
        """
        return (self.screen_width, self.screen_height)