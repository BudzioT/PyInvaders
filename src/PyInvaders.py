import sys
import pygame

from Settings import Settings
from Spaceship import Spaceship


class PyInvaders:
    """Class to manage the entire game"""

    def __init__(self, size=(720, 576), fullscreen=False):
        """Initialize the game"""
        pygame.init()

        # Set game settings
        self.settings = Settings(size)

        # Set new surface with certain size and name PyInvaders
        if fullscreen:
            self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("PyInvaders")

        # Timer for frame rate calculation
        self.timer = pygame.time.Clock()

        # Spaceship - the player
        self.spaceship = Spaceship(self)

    def run(self):
        """Run the game"""
        while True:
            self._get_events()
            self.spaceship.update_pos()
            self._update_surface()
            # Run the loop in 60 FPS
            self.timer.tick(60)

    def _get_events(self):
        """Get and handle events"""
        for event in pygame.event.get():
            # If user wants to quit, do it
            if event.type == pygame.QUIT:
                sys.exit()

            # On pressing a key
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            # On releasing key
            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

    def _update_surface(self):
        """Fill the surface and update it"""
        self.surface.fill(self.settings.bg_color)
        self.spaceship.draw()

        # Update the contents of a surface
        pygame.display.flip()

    def _handle_keyup_events(self, event):
        """Handle events when releasing keys"""
        # Exit when escape is clicked
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        # Stop movement to the left
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.spaceship.move_flags["Left"] = False
        # Stop movement to the right
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.spaceship.move_flags["Right"] = False

    def _handle_keydown_events(self, event):
        """Handle events when pressing keys"""
        # Indicate movement to the left
        if event.key == pygame.K_LEFT:
            self.spaceship.move_flags["Left"] = True
        # Indicate movement to the right
        elif event.key == pygame.K_RIGHT:
            self.spaceship.move_flags["Right"] = True


# If filled is called directly, create and run the game
if __name__ == "__main__":
    game = PyInvaders()
    game.run()
