import pygame.font
from pygame.sprite import Group

from Spaceship import Spaceship


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

        # Set initial score text
        self.set_score()
        # Set initial high score text
        self.set_highscore()
        # Set initial level text
        self.set_level()

    def set_score(self):
        """Make rendered image from score text"""
        # Round the highscore to show only powers of ten
        rounded_score = int(round(self.stats.score, -1))
        # Save it nicely (in format 1,000,000...)
        score_text = str(f"{rounded_score:,}")
        # Render the score image
        self.score_image = self.font.render(score_text, True, self.font_color,
                                            self.settings.bg_color)
        # Display score at right side of the surface
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.surface_rect.right - 20
        self.score_rect.top = 20

    def set_highscore(self):
        """Make rendered image from highscore text"""
        # Round the highscore
        highscore = int(round(self.stats.high_score, -1))
        # Save it in a nice format
        highscore_text = str(f"{highscore:,}")
        # Render the highscore image
        self.highscore_image = self.font.render(highscore_text, True, self.font_color,
                                                self.settings.bg_color)
        # Display the highscore at the center top part of the surface
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.top = self.score_rect.top
        self.highscore_rect.centerx = self.surface_rect.centerx

    def set_level(self):
        """Make a rendered image from level text"""
        level_text = str(self.stats.level)
        self.level_image = self.font.render(level_text, True, self.font_color,
                                            self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def draw(self):
        """Draw score, highscore and level onto the surface"""
        self.surface.blit(self.score_image, self.score_rect)
        self.surface.blit(self.highscore_image, self.highscore_rect)
        self.surface.blit(self.level_image, self.level_rect)

    def check_highscore(self):
        """Check if there is a new highscore, set it"""
        if self.stats.score > self.stats.high_score:
            # Set new highscore, update the text
            self.stats.high_score = self.stats.score
            self.set_highscore()
