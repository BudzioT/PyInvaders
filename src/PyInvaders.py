import sys
import pygame

from Settings import Settings
from Spaceship import Spaceship


class PyInvaders:
    """Class to manage the entire game"""

    def __init__(self, size=(720, 576)):
        """Initialize the game"""
        pygame.init()

        # Set game settings
        self.settings = Settings(size)

        # Set new surface with certain size and name PyInvaders
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("PyInvaders")

        # Timer for frame rate calculation
        self.timer = pygame.time.Clock()

        # Spaceship - the player
        self.spaceship = Spaceship()

    def run(self):
        """Run the game"""
        while True:
            # Event loop
            for event in pygame.event.get():
                # If user wants to quit, do it
                if event.type == pygame.QUIT:
                    sys.exit()

                # Fill the surface with the background color
                self.surface.fill(self.settings.bg_color)

                # Update the contents of a surface
                pygame.display.flip()
                # Run the loop in 60 FPS
                self.timer.tick(60)


# If filled is called directly, create and run the game
if __name__ == "__main__":
    game = PyInvaders((720, 576))
    game.run()
