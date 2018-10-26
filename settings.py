import sys

class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the static game's settings"""

        if sys.platform.title() == 'Darwin':  # Mac OS
            # Platform specific screen settings
            self.screen_width = 1100
            self.screen_height = 600

            # Platform specific Ship settings
            self.ship_limit = 3

            # Platform specific Alien settings
            self.alien_fleet_drop_speed = 15.0

        else:
            # Platform specific screen settings
            self.screen_width = 1200
            self.screen_height = 800

            # Platform specific Ship settings
            self.ship_limit = 3

            # Platform specific Alien settings
            self.alien_fleet_drop_speed = 10.0

        # General screen settings
        self.bg_color = (230, 230, 230)

        # General Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # General game settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def screen_dimensions(self):
        """
        Returns the predefined screen dimensions as a tuple
        :rtype: tuple
        """
        return (self.screen_width, self.screen_height)


    def initialize_dynamic_settings(self):
        """"Initialize settings that change throughout the game"""
        if sys.platform.title() == 'Darwin':  # Mac OS

            # Platform specific Ship settings
            self.ship_speed_factor = 7.5

            # Platform specific Bullet settings
            self.bullet_speed_factor = 10.0

            # Platform specific Alien settings
            self.alien_speed_factor = 2
            self.alien_fleet_direction = 1 # 1=right, -1=left

        else:

            # Platform specific Ship settings
            self.ship_speed_factor = 1.5

            # Platform specific Bullet settings
            self.bullet_speed_factor = 3

            # Platform specific Alien settings
            self.alien_speed_factor = 1
            self.alien_fleet_direction = 1 # 1=right, -1=left


        self.alien_points = 50 # amount of points a user get for shot alien

    def increase_speed(self):
        """"Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
