class Settings:
    """Settings of the game"""
    def __init__(self, size, bg_color=(116, 147, 163), bullet_width=3, bullet_height=15,
                 bullet_color=(60, 60, 60), bullets_limit=3, fleet_drop_speed=1,
                 speedup_scale=1.1):
        """Initialize static game settings"""
        # General settings
        self.window_width = size[0]
        self.window_height = size[1]
        self.bg_color = bg_color

        # Spaceship settings
        self.spaceship_limit = 3

        # Star settings
        self.star_limit = 50

        # Bullets settings
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.bullet_color = bullet_color
        self.bullets_limit = bullets_limit

        # Alien settings
        self.fleet_drop_speed = fleet_drop_speed

        # Set how fast the game speedups
        self.speedup_scale = 1.1

        # Initialize settings that can change mid-game
        self.initialize_dynamic()

    def initialize_dynamic(self, spaceship_speed=1.5, bullet_speed=2.5,
                           alien_speed=1.0, alien_points=5, score_scale=1.5):
        """Initialize settings that change mid-game"""
        # Speed of objects
        self.spaceship_speed = spaceship_speed
        self.bullet_speed = bullet_speed
        self.alien_speed = alien_speed
        self.star_speed = 1.0

        # Points for shooting an alien
        self.alien_points = alien_points

        # Score increase after speedup scale
        self.score_scale = score_scale

        # Alien fleet direction: 1 is Right, -1 is Left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase settings of objects when game speeds up"""
        # Increase speeds
        self.spaceship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.star_speed *= self.speedup_scale

        # Increase point factor
        self.alien_points *= self.score_scale
