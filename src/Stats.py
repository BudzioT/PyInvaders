class Stats:
    """Class to track statistics"""
    def __init__(self, game):
        """Initialize statistics"""
        # Grab settings from the game
        self.settings = game.settings
        self.reset_stats()

    def reset_stats(self):
        """Reset statistics"""
        self.spaceship_left = self.settings.spaceship_limit
