class Stats:
    """Class to track statistics"""
    def __init__(self, game):
        """Initialize statistics"""
        # Grab settings from the game
        self.settings = game.settings
        self.reset_stats()

        # Highscore that doesn't reset
        self.high_score = 0

    def reset_stats(self):
        """Reset statistics"""
        self.spaceship_left = self.settings.spaceship_limit
        self.score = 0
        self.level = 1
