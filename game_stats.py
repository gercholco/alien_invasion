
class GameStats():
    """tracks statistics for Alien Invasion."""
    def __init__(self, ai_settings):
        """initialize statistics"""
        self.ai_settings = ai_settings
        self.ships_left = 0
        self.reset_stats()
        
        #Startgame in an inactive state
        self.game_active = False

        #Highscore should never be reset
        self.high_score = 0
        

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1