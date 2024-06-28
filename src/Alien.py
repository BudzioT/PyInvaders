import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class that represents an enemy alien"""
    def __init__(self, game):
        """Initialize alien and its position"""
        super().__init__()
        # Get the game surface
        self.surface = game.surface
        # Use game settings
        self.settings = game.settings

        # Load the image, set its hitboxes
        self.image = pygame.image.load("images/enemy0.bmp")
        self.rect = self.image.get_rect()

        # Spawn the aliens at the top left part of the surface
        # (subtracted by height and width of the image)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store float position for higher precision
        self.x = float(self.rect.x)

    def update(self):
        """Update the position of alien"""
        # Move alien in specified direction
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return if alien touches the edge"""
        surface_rect = self.surface.get_rect()
        return (self.rect.right >= surface_rect.right) or (self.rect.left <= 0)
