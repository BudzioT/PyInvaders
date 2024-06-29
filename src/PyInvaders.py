import sys
import os
from time import sleep
from random import randint

import pygame

from Settings import Settings
from Spaceship import Spaceship
from Bullet import Bullet
from Alien import Alien
from Star import Star
from Stats import Stats
from Button import Button
from Scoreboard import Scoreboard
from Title import Title


class PyInvaders:
    """Class to manage the entire game"""

    def __init__(self, size=(720, 576), fullscreen=False):
        """Initialize the game"""
        # Initialize pygame
        pygame.init()
        # Initialize pygame mixer
        pygame.mixer.init()

        # Get directory of the current script
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Set sounds
        self.shoot_sound = pygame.mixer.Sound(os.path.join(self.base_path, "sounds/shoot.wav"))
        self.death_sound = pygame.mixer.Sound(os.path.join(self.base_path, "sounds/explosion.wav"))
        self.kill_sound = pygame.mixer.Sound(os.path.join(self.base_path, "sounds/invaderkilled.wav"))

        # Set game to active
        self.active = False
        # Set game to choose difficulty mode
        self.choose_diff = False

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

        # Game statistics
        self.stats = Stats(self)
        # Game scoreboard
        self.scoreboard = Scoreboard(self)
        # Spaceship - the player
        self.spaceship = Spaceship(self)
        # Bullets group
        self.bullets = pygame.sprite.Group()
        # Aliens group
        self.aliens = pygame.sprite.Group()
        # Stars group
        self.stars = pygame.sprite.Group()

        # Create alien fleet
        self._create_fleet()

        # Create Start Button
        self.start_button = Button(self, "Start")

        # Easy button
        self.easy_button = Button(self, "Easy", button_color=(125, 227, 70),
                                  center=100)
        # Normal button
        self.normal_button = Button(self, "Normal", button_color=(240, 234, 117))
        # Hard button
        self.hard_button = Button(self, "Hard", button_color=(250, 35, 60),
                                  center=self.settings.window_width - 100)
        # Title text
        self.title = Title(self)

    def run(self):
        """Run the game"""
        while True:
            # Handle events
            self._get_events()

            # If the game is active, run the entire mechanics
            if self.active:
                # Update positions
                self.spaceship.update_pos()
                self.bullets.update()
                self._update_aliens()
                self._update_stars()

            # Update the surface
            self._update_surface()
            # Run the loop in 60 FPS
            self.timer.tick(60)

    def _get_events(self):
        """Get and handle events"""
        for event in pygame.event.get():
            # If user wants to quit, do it
            if event.type == pygame.QUIT:
                # Save the highscore
                self.stats.save_highscore()
                sys.exit()
            # Check for mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position, check if it touches any button
                mouse_pos = pygame.mouse.get_pos()
                # If user is choosing difficulty, check which one, if any, he clicked
                if self.choose_diff:
                    self._check_choose_diff(mouse_pos)
                # If user is starting, check if he clicks start button
                else:
                    self._check_start(mouse_pos)

            # On pressing a key
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            # On releasing key
            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

    def _update_surface(self):
        """Fill the surface and update it"""
        self.surface.fill(self.settings.bg_color)
        self.stars.draw(surface=self.surface)
        self.spaceship.draw()
        self._update_bullets()
        self.aliens.draw(surface=self.surface)

        # Draw the scoreboard
        self.scoreboard.draw()

        # If the game isn't active, draw the choose difficulty buttons
        if not self.active and not self.choose_diff:
            # Fill the background
            self.surface.fill(self.settings.bg_color)
            # Draw the title
            self.title.draw()
            # Draw the button
            self.start_button.draw_button()
        # If difficulty isn't chosen, draw the start button
        elif self.choose_diff:
            # Fill the background
            self.surface.fill(self.settings.bg_color)
            # Draw the buttons
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()

        # Update the contents of a surface
        pygame.display.flip()

    def _handle_keyup_events(self, event):
        """Handle events when releasing keys"""
        # Exit when escape is clicked
        if event.key == pygame.K_ESCAPE:
            self.stats.save_highscore()
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
        # If game is active, handle movement key presses
        if self.active:
            # Indicate movement to the left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.spaceship.move_flags["Left"] = True
            # Indicate movement to the right
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.spaceship.move_flags["Right"] = True
        # If game isn't active
        else:
            # On 'p', start the game
            if event.key == pygame.K_p:
                self._start_game()

    def _fire_bullet(self):
        """Create a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_limit:
            bullet = Bullet(self)
            self.bullets.add(bullet)
            self.shoot_sound.play()

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
        # Check for collision between bullets and aliens
        self._check_bullets_collisions()

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

    def _create_star_group(self):
        """Create group of stars"""
        # Create a star for size matters
        star = Star(self)
        # While there is still space for stars, spawn them randomly
        while len(self.stars) < self.settings.star_limit:
            # Create a new star
            new_star = Star(self)
            # Randomize its position
            new_star.rect.x = randint(0, self.settings.window_width - star.rect.width)
            new_star.rect.y = randint(0, self.settings.window_height -
                                      int(0.3 * self.settings.window_height))
            # Add it to the group
            self.stars.add(new_star)

    def _create_alien(self, current_x, current_y):
        """Create an alien at the given position, add it to the fleet"""
        # Create a new alien, set its position to current drawing one
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        # Add it to the fleet
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Update all aliens positions"""
        self.aliens.update()
        self._check_fleet_edges()

        # Check for collisions between spaceship and aliens
        if pygame.sprite.spritecollideany(self.spaceship, self.aliens):
            # Handle spaceship getting hit
            self._spaceship_hit()
        # Check for collisions between aliens and bottom part of visible surface
        self._check_bottom_collision()

    def _update_stars(self):
        """Update stars position"""
        self._create_star_group()
        for star in self.stars.sprites():
            star.update()

    def _check_fleet_edges(self):
        """If aliens touch the edge, change the direction"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Move the fleet down and change its direction"""
        # Move every alien down
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # Change direction to opposite of the current one
        self.settings.fleet_direction *= -1

    def _check_bullets_collisions(self):
        """Check for collisions between bullets and aliens, spawn aliens if needed"""
        # Check for collisions with aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # If there is a collision, update the score
        if collisions:
            # Check every collision, increase the score with every one of them
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                # Play alien kill sound
                self.kill_sound.play()
            # Update the displayed score
            self.scoreboard.set_score()
            self.scoreboard.check_highscore()

        # If all aliens are destroyed, spawn new ones and destroy old bullets
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

            # Increase level
            self.stats.level += 1
            self.scoreboard.set_level()
            # Speedup the game
            self.settings.increase_speed()

    def _spaceship_hit(self):
        """Handle spaceship getting hit"""
        # Play death sound effect
        self.death_sound.play()

        # If this was the last live, set game status to not active
        if self.stats.spaceship_left <= 0:
            self.active = False
            # Show the mouse
            pygame.mouse.set_visible(True)
            return None

        # Decrement spaceships count
        self.stats.spaceship_left -= 1
        # Update the spaceships count
        self.scoreboard.set_spaceships()
        # Clean remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # Save the highscore in case of rage-quit
        self.stats.save_highscore()

        # Create new fleet of aliens, move spaceship to the starting position
        self._create_fleet()
        self.spaceship.center()

        # Wait a while to give player time
        sleep(0.5)

    def _check_bottom_collision(self):
        """Check collision between bottom of the surface and aliens"""
        # Check for collisions with every alien
        for alien in self.aliens.sprites():
            # If it touches or is lower than the visible surface,
            # indicate spaceship getting hit
            if alien.rect.bottom >= self.settings.window_height:
                self._spaceship_hit()
                break
        # Clean stars
        for star in self.stars.sprites().copy():
            # Check if the star is under the visible surface, clean it
            if star.rect.top >= self.settings.window_height:
                self.stars.remove(star)

    def _check_start(self, mouse_pos):
        """If mouse is on the Start button, start the game if it isn't started already"""
        if (self.start_button.rect.collidepoint(mouse_pos) and not self.active
                and not self.choose_diff):
            self.choose_diff = True

    def _start_game(self, speed_factor, point_factor):
        """Start the game, reset everything needed, set the next game based of
        off difficulty chosen"""
        # Reset statistics
        self.stats.reset_stats()
        # Reset the score
        self.scoreboard.set_score()
        # Reset the level
        self.scoreboard.set_level()
        # Reset spaceships count
        self.scoreboard.set_spaceships()

        # Return speed to basic one
        self.settings.initialize_dynamic()
        # Activate the game
        self.active = True

        # Cleanup bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        # Create new set of aliens
        self._create_fleet()
        # Reset the ship position
        self.spaceship.center()

        # Set speed and point factor
        self.settings.speedup_scale = speed_factor
        self.settings.score_scale = point_factor

        # Hide the mouse when playing
        pygame.mouse.set_visible(False)

    def _check_choose_diff(self, mouse_pos):
        """Check if user chose any difficulty"""
        if self.choose_diff and not self.active:
            # If user picked easy, use small factors
            if self.easy_button.rect.collidepoint(mouse_pos):
                self._start_game(0.8, 0.8)
                self.choose_diff = False
                self.active = True
            # If user picked normal, use normal factors
            elif self.normal_button.rect.collidepoint(mouse_pos):
                self._start_game(1.1, 1.5)
                self.choose_diff = False
                self.active = True
            # If user picked hard, use big factors
            elif self.hard_button.rect.collidepoint(mouse_pos):
                self._start_game(1.4, 2.5)
                self.choose_diff = False
                self.active = True


# If filled is called directly, create and run the game
if __name__ == "__main__":
    game = PyInvaders()
    game.run()
    game.stats.save_highscore()
