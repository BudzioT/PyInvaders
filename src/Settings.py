class Settings:
    """Settings of the game"""
    def __init__(self, size, bg_color=(116, 147, 163), ship_speed=1.5,
                 bullet_speed=2.0, bullet_width=3, bullet_height=15,
                 bullet_color=(60, 60, 60), bullets_limit=3, alien_speed=1.0):
        """Initialize game settings"""
        # General settings
        self.window_width = size[0]
        self.window_height = size[1]
        self.bg_color = bg_color

        # Spaceship settings
        self.spaceship_speed = ship_speed

        # Bullets settings
        self.bullet_speed = bullet_speed
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.bullet_color = bullet_color
        self.bullets_limit = bullets_limit

        # Alien settings
        self.alien_speed = alien_speed
