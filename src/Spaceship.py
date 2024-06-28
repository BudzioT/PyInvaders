import pygame
from pygame.sprite import Sprite


class Spaceship(Sprite):
    """Class representing a spaceship"""
    def __init__(self, game):
        """Initialize spaceship at starting position"""
        super().__init__()
        # Set surface and its rectangle from game reference
        self.surface = game.surface
        self.surface_rect = self.surface.get_rect()
        # Set settings exactly like game settings
        self.settings = game.settings

        # Load the image, get its hitboxes
        self.image = pygame.image.load("images/player0.bmp")
        self.rect = self.image.get_rect()

        # Spawn the spaceship at the bottom of game surface
        self.rect.midbottom = self.surface_rect.midbottom

        # Exact horizontal location
        self.x = float(self.rect.x)

        # Flags indicating movement
        self.move_flags = {
            "Left": False,
            "Right": False,
        }

    def draw(self):
        """Draw the spaceship"""
        self.surface.blit(self.image, self.rect)

    def update_pos(self):
        """Update position based of movement flags"""
        if self.move_flags["Left"] and self.rect.left > 0:
            self.x -= self.settings.spaceship_speed
        if self.move_flags["Right"] and self.rect.right < self.surface_rect.right:
            self.x += self.settings.spaceship_speed

        # Update real rect position
        self.rect.x = self.x

    def center(self):
        """Center the spaceship"""
        self.rect.midbottom = self.surface_rect.midbottom
        self.x = float(self.rect.x)
