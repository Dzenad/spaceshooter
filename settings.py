class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Intitialize the game's settings"""

        # Screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Game
        self.game_title = "Alien Invasion"
        self.frame_rate = 120

        # Ship
        self.ship_speed = 3

        # Bullet
        self.bullet_speed = 2.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 60, 60)
        self.bullets_allowed = 10
