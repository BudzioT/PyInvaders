from pathlib import Path
import json
import os

import pygame.mixer


class Stats:
    """Class to track statistics"""
    def __init__(self, game):
        """Initialize statistics"""
        # Grab settings from the game
        self.settings = game.settings
        self.reset_stats()

        # Get path to files
        self.base_path = game.base_path

        # Highscore that doesn't reset
        self.high_score = 0
        self.read_highscore()

    def reset_stats(self):
        """Reset statistics"""
        self.spaceship_left = self.settings.spaceship_limit
        self.score = 0
        self.level = 1

    def read_highscore(self):
        """Read highscore from a file"""
        # Open file
        file = Path(os.path.join(self.base_path, "data/highscore.json"))
        # Set new highscore to 0 in case of a failure
        new_highscore = 0
        # If file exists, read highscore from it
        if file.exists():
            # Read highscore from file
            new_highscore = json.loads(file.read_text())
            # If it is higher than current one, set it
            if self.high_score < new_highscore:
                self.high_score = new_highscore
        # Return new highscore
        return new_highscore

    def save_highscore(self):
        """Save highscore to a file"""
        # Open file
        file = Path(os.path.join(self.base_path, "data/highscore.json"))
        # Write highscore into it
        file.write_text(json.dumps(self.high_score))