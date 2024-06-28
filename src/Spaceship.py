import pygame


class Spaceship:
    """Class representing a spaceship"""
    def __init__(self, game):
        """Initialize spaceship at starting position"""
        # Set surface and its rectangle from game reference
        self.surface = game.surface
        self.surface_rect = self.surface.get_rect()

        # Load the sprite, get its hitboxes
        self.sprite = pygame.image.load("images/player0.bmp")
        self.rect = self.sprite.get_rect()

        # Spawn the spaceship at the bottom of game surface
        self.rect.midbottom = self.surface_rect.midbottom

    def draw(self):
        """Draw the spaceship"""
        self.surface.blit(self.sprite, self.rect)
