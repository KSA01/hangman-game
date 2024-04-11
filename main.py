
import game
from screens import Screens
import ui
import pygame
import sys
import time
from images import Images
from timer import Timer
from storage import save_data, load_data, del_custom_words

pygame.init()

def main():
    screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SRCALPHA, 32) # pygame screen
    pygame.display.set_caption("Hangman")
    clock = pygame.time.Clock()
    TIME_DURATION = 60 # 60 sec
    
    # Loading Screen Background
    images = Images(screen)

    timer = Timer(TIME_DURATION)

    screens = Screens(screen) # in app game screens

    game.Init() # Initializes the word difficulty analyzer at startup

    input_text = ""
    name_input_text = ""
    user_name = "user1"
    word_streak = 0
    display = ""

    while screens.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data(user_name, game.score, word_streak)
                del_custom_words(screens.file_path, screens.words_entered_list)
                screens.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not screens.start_game and not screens.quit_screen and not screens.mode_select and screens.button_rect.collidepoint(event.pos):
                        #Starts Game
                        screens.mode_select = True
                        time.sleep(0.1)
                    elif not screens.start_game and not screens.quit_screen and not screens.mode_select and screens.stats_reset_button_rect.collidepoint(event.pos):
                        save_data(user_name, 0, 0, reset=True)
                    elif screens.menu_rect.collidepoint(event.pos):
                        #Goes back to main menu
                        if screens.display_rules:
                            screens.display_rules = False
                        elif screens.themes:
                            screens.themes = False
                        elif screens.custom_words:
                            screens.custom_words = False
                        elif screens.start_game and not screens.ensurance:
                            screens.ensurance = True
                    elif not screens.start_game and not screens.quit_screen and not screens.display_rules and not screens.themes and not screens.custom_words and not screens.mode_select and screens.rules_button_rect.collidepoint(event.pos):
                        #Display the rules screen
                        screens.display_rules = True
                    elif not screens.start_game and not screens.quit_screen and not screens.display_rules and not screens.themes and not screens.custom_words and not screens.mode_select and screens.theme_button_rect.collidepoint(event.pos):
                        #Display the themes screen
                        screens.themes = True
                    elif not screens.start_game and not screens.quit_screen and not screens.display_rules and not screens.themes and not screens.custom_words and not screens.mode_select and screens.custom_words_button_rect.collidepoint(event.pos):
                        #Display the custom words screen
                        screens.custom_words = True
                    elif not screens.quit_screen and not screens.start_game and screens.quit_but_rect.collidepoint(event.pos):
                        #Goes to quit menu
                        screens.quit_screen = True
                            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not screens.start_game:
                    # Are you sure you want to quit?
                    screens.quit_screen = True
                elif event.key == pygame.K_ESCAPE and screens.start_game:
                    # Are you sure you want to goto menu?
                    screens.ensurance = True
                elif event.key == pygame.K_BACKSPACE:
                    name_input_text = name_input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Process user input
                    if name_input_text:
                        name_input_text = name_input_text.rstrip('\r')  # Strip out carriage return character
                        user_name = name_input_text
                        name_input_text = ""
                elif screens.start_game:
                    input_text += event.unicode
                elif screens.custom_words:
                    screens.custom_word_input_text += event.unicode
                else:
                    name_input_text += event.unicode


        screen.blit(images.lobby_background, (0, 0))

        # Draw Home Screen
        if not screens.start_game and not screens.mode_select and not screens.quit_screen and not screens.display_rules and not screens.themes and not screens.custom_words:
            #player_data = load_data()
            screens.homeScreen(user_name, name_input_text)

        # Display Quit Screen from Home
        if screens.quit_screen:
            screens.quitScreen(event, user_name, word_streak)

        # Display the rules and info for the game
        if screens.display_rules and not screens.mode_select and not screens.replay_menu and not screens.quit_screen:
           screens.rulesScreen()

        # Display theme selection menu
        if screens.themes and not screens.mode_select and not screens.replay_menu and not screens.quit_screen:
            screen.blit(images.current_theme, (0, 0))
            screens.themesScreen(event, images)

        # Display custom word addition menu
        if screens.custom_words and not screens.mode_select and not screens.replay_menu and not screens.quit_screen:
            screens.customWordsScreen(event)

        # Display the replay menu
        if screens.replay_menu:
            screens.replayScreen(event)
            time.sleep(0.12) # to fix a glitchy transition from replay to home menu

        # Mode select menu
        if screens.mode_select and not screens.replay_menu and not screens.quit_screen and not screens.display_rules:
            screens.modeScreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    timer.reset()
                    if screens.rect_easy.collidepoint(event.pos):
                        screens.start_game = True
                        screens.mode_select = False
                        screens.ensurance = False
                        lives = 10
                        mode = "Easy"
                        timer.TIMER_DURATION = 60
                    elif screens.rect_med.collidepoint(event.pos):
                        screens.start_game = True
                        screens.mode_select = False
                        screens.ensurance = False
                        lives = 7
                        mode = "Med"
                        timer.TIMER_DURATION = 45
                    elif screens.rect_hard.collidepoint(event.pos):
                        screens.start_game = True
                        screens.mode_select = False
                        screens.ensurance = False
                        lives = 7
                        mode = "Hard"
                        timer.TIMER_DURATION = 30
                    
                    time.sleep(0.05)

        if screens.start_game and not screens.replay_menu:
            screens.gameScreen(lives, input_text, display, mode, images.current_theme)

            if screens.ensurance:
                input_text = ""
                screens.ensuranceScreen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if screens.button_rect_cont.collidepoint(event.pos): # Yes quit to menu
                            save_data(user_name, game.score, word_streak)
                            screens.start_game = False
                            screens.mode_select = False
                            screens.new_game = True
                        elif screens.button_rect_dont.collidepoint(event.pos): # No continue game
                            screens.ensurance = False
                            continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Enter key (Y)
                        save_data(user_name, game.score, word_streak)
                        screens.start_game = False
                        screens.mode_select = False
                    elif event.key == pygame.K_ESCAPE: # Escape key (N)
                        screens.ensurance = False
                        continue

            if screens.new_game:
                lives, display = game.hangman(lives, screens.new_game, "", mode)
                word_box_width = len(display) * 10 + 80
                screens.text_box_rect = pygame.Rect(screens.center_x - (word_box_width // 2), screens.bottom_y - 50, word_box_width, 50)
                # Start the timer
                timer.start_timer() # Starts the timer after the hangman games loads in case of lag
                screens.new_game = False

            if event.type == pygame.KEYDOWN and not screens.ensurance:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Process user input
                    if input_text:
                        input_text = input_text.rstrip('\r')  # Strip out carriage return character
                        lives, display = game.hangman(lives, screens.new_game, input_text, mode)
                        input_text = ""
                else:
                    input_text += event.unicode

            # Check if the game is over
            if lives == 0 or lives == "win" or timer.has_expired():
                if lives == "win":
                    screens.player_won = True
                    word_streak += 1
                    if mode == "Med" or mode == "Hard":
                        lives = 7
                    elif mode == "Easy":
                        lives = 10
                
                if timer.has_expired():
                    lives = 0

                # Reset the timer for the next round
                timer.reset()

                if lives == 0:
                    word_streak = 0
                    game.hangman(lives, screens.new_game, "", mode)
                game.draw_hangman(screen, lives, mode, images.current_theme)
                if screens.player_won:
                    game.draw_victory_hangman(screen)
                ui.draw_text_box(screen, screens.text_box_rect, display, screens.guess_font)
                ui.draw_chat(screen, ui.text_list, screens.chat_font)
                pygame.display.flip()
                time.sleep(4)

                save_data(user_name, game.score, word_streak)

                screens.player_won = False
                screens.replay_menu = True

            # Remove elements from chat that have been there for too long
            if len(ui.text_list) >= 6:
                ui.text_list.pop(0)

            # Update the timer
            timer.update()

            timer_text = f"Time: {timer.duration}"
            timer_font = pygame.font.Font(None, 36)
            timer_surface = timer_font.render(timer_text, True, (255, 255, 255))
            screen.blit(timer_surface, (20, ui.SCREEN_HEIGHT-60))
        
        # Update display
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
