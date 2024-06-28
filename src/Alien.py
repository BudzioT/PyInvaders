import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class that represents an enemy alien"""
    def __init__(self, game):
        """Initialize alien and its position"""
        super().__init__()
        # Get the game surface
        self.surface = game.surface

        # Load the sprite, set its hitboxes
        self.sprite = pygame.image.load("images/enemy0.bmp")
        self.rect = self.sprite.get_rect()
