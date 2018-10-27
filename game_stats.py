class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        # Start the game in active state
        self.game_active = False
        # Keep track of highest score
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ship_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1

