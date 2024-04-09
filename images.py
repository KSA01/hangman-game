
import pygame
import ui
from datetime import datetime

'''current_second = datetime.now().second
current_minute = datetime.now().minute
current_hour = datetime.now().hour'''

current_day = datetime.now().day # int (3)
current_month = datetime.now().month # int (4)
current_year = datetime.now().year # int (2024)

class Images:
    def __init__(self, screen):
        self.screen = screen
        self.load_background = pygame.image.load("images/loading.jpg")
        self.load_background = pygame.transform.scale(self.load_background, (ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
        self.lobby_background = pygame.image.load("images/lobby3.jpeg")
        self.lobby_background = pygame.transform.scale(self.lobby_background, (ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))

        # Loading Screen Background
        screen.blit(self.load_background, (0, 0))
        pygame.display.flip()

        self.themes = {}

        for i in range(8):
            theme_image = pygame.image.load(f"images/themes/theme{i+1}.jpg")
            scaled_theme = pygame.transform.scale(theme_image, (ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
            self.themes[i] = scaled_theme

        if current_month == 3: # Easter
            self.current_theme = self.themes[2]
        elif current_month == 10: # Halloween
            self.current_theme = self.themes[4]
        elif current_month == 12: # Christmas
            self.current_theme = self.themes[6]
        else: # Default
            self.current_theme = self.themes[1]

    def changeTheme(self, themeId):
        self.current_theme = self.themes[themeId]