import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class indicating bullets fired from the spaceship"""
    def __init__(self, game):
        """Initialize a bullet at the ship position"""
        super().__init__()
        # Set surface from game reference
        self.surface = game.surface
        # Set settings exactly like game settings
        self.settings = game.settings

        # Set bullet color
        self.color = self.settings.bullet_color

        # Create bullet at temp location, fix it
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = game.spaceship.rect.midtop

        # Store bullet position as float for higher precision
        self.y = float(self.rect.y)

    def draw(self):
        """Draw bullet to the surface"""
        pygame.draw.rect(self.surface, self.color, self.rect)

    def update(self):
        """Move the bullet to the top of the surface"""
        # Update position in float for higher precision
        self.y -= self.settings.bullet_speed
        # Update real rect position
        self.rect.y = self.y
