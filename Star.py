from random import randint

import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Class representing star"""
    def __init__(self, game):
        """Initialize star"""
        super().__init__()
        # Get game's surface
        self.surface = game.surface
        # Grab settings from the game
        self.settings = game.settings

        # Load the image, set its rectangle
        self.image = pygame.image.load("images/star0.bmp")
        self.rect = self.image.get_rect()

        # Spawn the stars at the top of the screen
        self.rect.y = 0
        self.rect.x = self.rect.width

        # Get random star speed
        self.star_speed = randint(1, 4)

    def update(self):
        """Update position of stars"""
        self.rect.y += self.settings.star_speed
