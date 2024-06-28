class Settings:
    """Settings of the game"""
    def __init__(self, size, bg_color=(39, 53, 87)):
        """Initialize settings"""
        self.window_width = size[0]
        self.window_height = size[1]
        self.bg_color = bg_color
