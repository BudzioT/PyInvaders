import pygame.font


class Scoreboard:
    """Class representing scores"""
    def __init__(self, game, font_color=(30, 30, 30)):
        """Initialize scoring properties"""
        # Grab surface from the game
        self.surface = game.surface
        self.surface_rect = self.surface.get_rect()
        # Use settings and statistics from the game
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for displaying scores
        self.font_color = font_color
        self.font = pygame.font.SysFont(None, 48)

        # Prepare initial score text
        self.set_score()

    def set_score(self):
        """Make rendered image from score text"""
        score_text = str(self.stats.score)
        self.score_image = self.font.render(score_text, True, self.font_color,
                                            self.settings.bg_color)
        # Display score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.surface_rect.right - 20
        self.score_rect.top = 20

    def draw(self):
        """Draw the score onto the surface"""
        self.surface.blit(self.score_image, self.score_rect)
