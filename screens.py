
import pygame
import ui
import game
from storage import save_data, load_data

class Screens:
    def __init__(self, screen):
        self.screen = screen
        self.center_x = ui.SCREEN_WIDTH // 2
        self.center_y = ui.SCREEN_HEIGHT // 2
        self.bottom_y = ui.SCREEN_HEIGHT
        self.right_x = ui.SCREEN_WIDTH

        self.running = True
        self.new_game = True
        self.mode_select = False
        self.start_game = False
        self.quit_screen = False
        self.replay_menu = False
        self.ensurance = False
        self.display_rules = False
        self.themes = False
        self.custom_words = False
        self.player_won = False

        self.button_font = pygame.font.Font(None, 30)
        self.input_font = pygame.font.Font(None, 30)
        self.guess_font = pygame.font.Font(None, 50)
        self.lives_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 120)
        self.chat_font = pygame.font.Font(None, 25)

        self.stats_width = self.right_x / 4
        self.stats_height = self.bottom_y / 3

        self.rules_width = self.right_x / 4
        self.rules_height = self.bottom_y / 2

        self.input_box_rect = pygame.Rect((self.center_x - 300), (self.bottom_y * (5/6)), 100, 30)
        self.title_rect = pygame.Rect((self.center_x) - (600 // 2), (self.bottom_y / 50), 600, 130)
        self.menu_rect = pygame.Rect(20, 20, 100, 100)
        self.quit_but_rect = pygame.Rect(self.right_x - 120, 20, 100, 100)
        self.text_box_rect = pygame.Rect(self.center_x - (420 // 2), self.bottom_y - 50, 400, 50)
        self.lives_box_rect = pygame.Rect(self.right_x - 180, 100, 170, 70)
        self.incorrect_box_rect = pygame.Rect(self.right_x - 280, self.bottom_y - 50, 170, 40)
        self.rules_button_rect = pygame.Rect(self.center_x - (150 // 2), self.center_y + 40, 150, 50)
        self.button_rect = pygame.Rect(self.center_x - (150 // 2), self.center_y - 20, 150, 50)
        self.theme_button_rect = pygame.Rect(self.center_x - (150 // 2), self.center_y + 100, 150, 50)
        self.custom_words_button_rect = pygame.Rect(self.center_x - (150 // 2), self.center_y + 160, 150, 50)
        self.welc_title_rect = pygame.Rect((self.center_x) - (1000 // 2), (self.bottom_y / 50), 1000, 130)
        
        self.stats_box_rect = pygame.Rect(self.right_x / 16, (self.bottom_y / 2) - (self.stats_height / 4), self.stats_width, self.stats_height)
        self.stats_reset_button_rect = pygame.Rect(self.right_x / 16 + 100, self.bottom_y - (self.stats_height), 130, 30)
        
        self.quit_rect = pygame.Rect((self.center_x) - (600 // 2), (self.bottom_y / 100), 600, 130)
        self.button_rect_yes = pygame.Rect(self.center_x - 120, self.center_y - (50 // 2), 100, 50)
        self.button_rect_no = pygame.Rect(self.center_x + 20, self.center_y - (50 // 2), 100, 50)
        
        self.dir_box_rect = pygame.Rect(self.right_x - (self.rules_width*1.25), (self.bottom_y / 2) - (self.stats_height / 4), self.rules_width, self.rules_height)
        self.howto_box_rect = pygame.Rect(self.right_x / 2 - (self.rules_width/2), (self.bottom_y / 2) - (self.stats_height / 4), self.rules_width, self.rules_height)
        self.rules_box_rect = pygame.Rect(self.right_x / 16, (self.bottom_y / 2) - (self.stats_height / 4), self.rules_width, self.rules_height)
        
        self.rect_easy = pygame.Rect((self.center_x - (150*2)), (self.bottom_y * (7/12)), 150, 50)
        self.rect_med = pygame.Rect((self.center_x) - (150//2), (self.bottom_y * (7/12)), 150, 50)
        self.rect_hard = pygame.Rect((self.center_x + 150), (self.bottom_y * (7/12)), 150, 50)

        self.top_rect = pygame.Rect((self.center_x) - (350 // 2), (self.bottom_y // 4), 350, 50)
        self.replay_rect = pygame.Rect(self.center_x - (500 // 2), self.center_y - 200, 500, 50)
        self.button_rect_replay = pygame.Rect(self.center_x - 120, self.center_y - 100, 100, 50)
        self.button_rect_not = pygame.Rect(self.center_x + 20, self.center_y - 100, 100, 50)

        self.sure_rect = pygame.Rect((self.center_x) - (650 // 2), (self.bottom_y / 100), 650, 130)
        self.button_rect_cont = pygame.Rect(self.center_x - 120, self.center_y - (50 // 2), 100, 50)
        self.button_rect_dont = pygame.Rect(self.center_x + 20, self.center_y - (50 // 2), 100, 50)

    def homeScreen(self, user_name, name_input_text, player_data):
        # Draw Start Screen Title
        ui.draw_text_box(self.screen, self.welc_title_rect, "Welcome to Hangman!", self.title_font)

        # Draw Quit Button
        button_hover_quit = self.quit_but_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.quit_but_rect, "Quit", self.lives_font, button_hover_quit)

        # Draw Start Button
        button_hover = self.button_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.button_rect, "Start Game!", self.button_font, button_hover)

        # Draw Rules Button
        button_hover_rules = self.rules_button_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.rules_button_rect, "Rules", self.button_font, button_hover_rules)

        # Draw Theme Button
        button_hover_theme = self.theme_button_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.theme_button_rect, "Theme Select", self.button_font, button_hover_theme)

        # Draw Custom Words Button
        button_hover_custom_words = self.custom_words_button_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.custom_words_button_rect, "Custom Words", self.button_font, button_hover_custom_words)

        # Draw User Name Entry Box
        name_box_width = self.right_x / 4
        name_box_height = self.bottom_y / 3
        name_input_box_rect = pygame.Rect(self.right_x - (name_box_width - 20), (self.bottom_y*2/3 + 20) - (name_box_height / 4), 100, 30)
        name_box_rect = pygame.Rect(self.right_x - (name_box_width*1.3), (self.bottom_y / 2) - (name_box_height / 4), name_box_width, name_box_height)
        name_box_list = ["", "Current User Name is: ", f"{user_name}", "", "Enter a User Name Below"]
        ui.draw_multiline_text_box(self.screen, name_box_rect, "User Name", name_box_list, self.lives_font, self.chat_font)
        ui.draw_input_box(self.screen, name_input_box_rect, name_input_text, self.input_font)

        # Draw Player Stats Box
        high_score = 0
        high_streak = 0
        if player_data:
            for entry in player_data:
                if entry["user"] == user_name:
                    high_score = entry["score"]
                    high_streak = entry["word-streak"]

        stats_list = ["", f"High Score: {high_score}", "", f"Most Words: {high_streak}"]
        ui.draw_multiline_text_box(self.screen, self.stats_box_rect, "Player Stats", stats_list, self.lives_font, self.lives_font)

        # Draw Stats Reset Button
        button_hover_stats_reset = self.stats_reset_button_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.stats_reset_button_rect, "Reset", self.button_font, button_hover_stats_reset)

    def quitScreen(self, event, user_name, word_streak):
        ui.draw_text_box(self.screen, self.quit_rect, "Are you sure you want to quit?", self.lives_font)
        button_hover_yes = self.button_rect_yes.collidepoint(pygame.mouse.get_pos())
        button_hover_no = self.button_rect_no.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.button_rect_yes, "YES", self.lives_font, button_hover_yes)
        ui.draw_button(self.screen, self.button_rect_no, "NO", self.lives_font, button_hover_no)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_rect_yes.collidepoint(event.pos):
                    save_data(user_name, game.score, word_streak)
                    self.running = False
                    return
                elif self.button_rect_no.collidepoint(event.pos):
                    self.quit_screen = False
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not self.start_game: # Enter key
                    save_data(user_name, game.score, word_streak)
                    self.running = False
                    return
                elif event.key == pygame.K_ESCAPE and not self.start_game: # Escape key
                    self.quit_screen = False
                    return

    def rulesScreen(self):
        # Draw Start Screen Title
        ui.draw_text_box(self.screen, self.welc_title_rect, "Welcome to Hangman!", self.title_font)

        # Draw menu button
        button_hover_menu = self.menu_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.menu_rect, "Menu", self.lives_font, button_hover_menu)

        # Rules
        rules_list = ["You must guess the word correctly", "in order to earn a score",
                        "Your score will increment for each", "word you guess correctly",
                        "If you fail to correctly guess the", "word then your score resets",
                        "If you also exit the game your score", "will be reset when you return",
                        "However, the game will save your", "highest score to your player stats",
                        "The game will also save the most", "amount of words you guess correctly", 
                        "consecutively to your player stats too"
                        ]
        ui.draw_multiline_text_box(self.screen, self.rules_box_rect, "Hangman Rules", rules_list, self.lives_font, self.chat_font)

        # How to play
        howto_list = ["Once in the main menu hit the start-", "game button",
                        "You will then choose your difficulty-", "Easy, Medium or Hard",
                        "You will then be prompted into the game",
                        "Here you must enter a single letter-", "at a time",
                        "You can see your letter currently-", "in the gray input box",
                        "If you wish to change it hit del-", "before you hit enter to not lose a life",
                        "In the bottom right you see the list-", "of incorrect guessed letters",
                        "Once you complete the word or fail-", "the game will end and give you a prompt" 
                        ]
        ui.draw_multiline_text_box(self.screen, self.howto_box_rect, "How to Play", howto_list, self.lives_font, self.chat_font)

        # Directions
        dir_list = ["Easy", "You have 10 lives/guesses to guess", "the word correctly",
                    "Your final score is your", "remaining guesses with no multiplier",
                    "Medium", "You have 7 lives/guesses to guess", "the word correctly",
                    "Your final score is your", "remaining guesses times 2",
                    "Hard", "You have 7 lives/guesses to guess", "the word correctly",
                    "Your final score is your", "remaining guesses times 3"
                    ]
        ui.draw_multiline_text_box(self.screen, self.dir_box_rect, "Game Directions", dir_list, self.lives_font, self.chat_font)

    def themesScreen(self, event, images):
        # Draw Start Screen Title
        ui.draw_text_box(self.screen, self.welc_title_rect, "Theme Selection", self.title_font)
        
        # Draw menu button
        button_hover_menu = self.menu_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.menu_rect, "Menu", self.lives_font, button_hover_menu)

        button_rects = {}
        button_hovers = {}
        h = ui.SCREEN_HEIGHT

        # Sets the rect hit box for all themes
        for i in range(8):
            if i < 4:
                button_rect_theme = pygame.Rect(self.center_x - 300, h/5 + ((i+1)*100), 200, 50)
            else:
                button_rect_theme = pygame.Rect(self.center_x + 100, h/5 + ((i-3)*100), 200, 50)
            button_hover_theme = button_rect_theme.collidepoint(pygame.mouse.get_pos())
            button_rects[i] = button_rect_theme
            button_hovers[i] = button_hover_theme

        # Draws a button for each theme
        for i in range(8):
            ui.draw_button(self.screen, button_rects[i], f"Theme {i+1}", self.lives_font, button_hovers[i])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for key, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        images.changeTheme(key)

    def customWordsScreen(self):
        pass

    def replayScreen(self, event):
        ui.draw_text_box(self.screen, self.replay_rect, "Do you wish to play again?", self.lives_font)
        button_hover_replay = self.button_rect_replay.collidepoint(pygame.mouse.get_pos())
        button_hover_not = self.button_rect_not.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.button_rect_replay, "YES", self.lives_font, button_hover_replay)
        ui.draw_button(self.screen, self.button_rect_not, "NO", self.lives_font, button_hover_not)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_rect_not.collidepoint(event.pos): # No goto main menu
                    self.start_game = False
                    self.new_game = True
                    self.replay_menu = False
                    game.score = 0
                elif self.button_rect_replay.collidepoint(event.pos): # Yes goto mode select
                    self.start_game = False
                    self.new_game = True
                    self.mode_select = True
                    self.replay_menu = False

    def modeScreen(self):
        # Draw title
        ui.draw_text_box(self.screen, self.title_rect, "H A N G M A N", self.title_font)
        ui.draw_text_box(self.screen, self.top_rect, "Choose a Difficulty", self.lives_font)
        button_hover_easy = self.rect_easy.collidepoint(pygame.mouse.get_pos())
        button_hover_med = self.rect_med.collidepoint(pygame.mouse.get_pos())
        button_hover_hard = self.rect_hard.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.rect_easy, "Easy", self.button_font, button_hover_easy)
        ui.draw_button(self.screen, self.rect_med, "Medium", self.button_font, button_hover_med)
        ui.draw_button(self.screen, self.rect_hard, "Hard", self.button_font, button_hover_hard)

    def gameScreen(self, lives, input_text, display, mode, current_theme):
        # Call hangman function
        game.draw_hangman(self.screen, lives, mode, current_theme)

        # Draw Chat
        ui.draw_chat(self.screen, ui.text_list, self.chat_font)
        
        # Draw title
        if not self.ensurance:
            ui.draw_text_box(self.screen, self.title_rect, "H A N G M A N", self.title_font)

        # Draw the text box for the word to guess
        ui.draw_text_box(self.screen, self.text_box_rect, display, self.guess_font)
        
        # Draw lives box
        lives_string = f"Lives: {lives}"
        ui.draw_text_box(self.screen, self.lives_box_rect, lives_string, self.lives_font)

        # Draw input box
        ui.draw_input_box(self.screen, self.input_box_rect, input_text, self.input_font)

        # Draw menu button
        button_hover_menu = self.menu_rect.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.menu_rect, "Menu", self.lives_font, button_hover_menu)

        # Draw Incorrect Guess Letters
        ui.draw_list_text(self.screen, self.incorrect_box_rect, game.incorrect_guesses, self.chat_font)

    def ensuranceScreen(self):
        ui.draw_text_box(self.screen, self.sure_rect, "Your game will not save. Are you sure?", self.lives_font)
        button_hover_cont = self.button_rect_cont.collidepoint(pygame.mouse.get_pos())
        button_hover_dont = self.button_rect_dont.collidepoint(pygame.mouse.get_pos())
        ui.draw_button(self.screen, self.button_rect_cont, "YES", self.lives_font, button_hover_cont)
        ui.draw_button(self.screen, self.button_rect_dont, "NO", self.lives_font, button_hover_dont)