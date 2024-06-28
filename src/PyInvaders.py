import sys
import pygame

from Settings import Settings
from Spaceship import Spaceship
from Bullet import Bullet
from Alien import Alien


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
        # Bullets group
        self.bullets = pygame.sprite.Group()
        # Aliens group
        self.aliens = pygame.sprite.Group()

        # Create alien fleet
        self._create_fleet()

    def run(self):
        """Run the game"""
        while True:
            # Handle events
            self._get_events()
            # Update positions
            self.spaceship.update_pos()
            self.bullets.update()
            # Update the surface
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
        self._update_bullets()
        self.aliens.draw(surface=self.surface)

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
        # Fire a bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _handle_keydown_events(self, event):
        """Handle events when pressing keys"""
        # Indicate movement to the left
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.spaceship.move_flags["Left"] = True
        # Indicate movement to the right
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.spaceship.move_flags["Right"] = True

    def _fire_bullet(self):
        """Create a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_limit:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _cleanup_bullets(self):
        """Cleanup bullets after they leave the visible surface"""
        # Go through each bullet
        for bullet in self.bullets.sprites().copy():
            # If bottom part of the bullet is higher than visible surface, remove it
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_bullets(self):
        """Draw existing bullets and cleanup old ones"""
        # Draw every bullet
        for bullet in self.bullets.sprites():
            bullet.draw()
        # Cleanup old ones
        self._cleanup_bullets()

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create first alien to get aliens size
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Current drawing horizontal position
        current_x, current_y = alien_width, alien_height

        # While there is space to draw alien, draw it
        # (space between aliens is the same as one alien's width and height)
        # Margin between right edge is two aliens width, between bottom is three aliens height

        # Draw rows of aliens
        while current_y < (self.settings.window_height - 3 * alien_height):
            # Draw columns of aliens
            while current_x < (self.settings.window_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                # Move drawing position by size of the current alien plus additional space
                current_x += 2 * alien_width
            # After drawing every column, go back to horizontal start
            current_x = alien_width
            # Move vertically down
            current_y += 2 * alien_height

    def _create_alien(self, current_x, current_y):
        """Create an alien at the given position, add it to the fleet"""
        # Create a new alien, set its position to current drawing one
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        # Add it to the fleet
        self.aliens.add(new_alien)


# If filled is called directly, create and run the game
if __name__ == "__main__":
    game = PyInvaders()
    game.run()
