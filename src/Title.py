import pygame.font


class Title:
    """Class representing title"""
    def __init__(self, game):
        """Initialize class"""
        # Set the surface exactly like the game
        self.surface = game.surface
        self.game = game
        self.surface_rect = self.surface.get_rect()

        # Set the font and its color
        self.font_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 76)
        # Set the title
        self._set_title()

    def _set_title(self):
        """Create an image from the title"""
        self.title_image = self.font.render("PyInvaders", True, self.font_color,
                                            self.game.settings.bg_color)
        # Place it in upper center of the surface
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.centerx = self.surface_rect.centerx
        self.title_image_rect.centery = self.surface_rect.centery - 150

    def draw(self):
        """Draw the title onto the surface"""
        # Draw an image of the title
        self.surface.blit(self.title_image, self.title_image_rect)
