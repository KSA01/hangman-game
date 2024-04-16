
import pygame
import random
import ui
from storage import load_file
from wordanalyzer import WordDifficulty

center_x = ui.SCREEN_WIDTH // 2
center_y = ui.SCREEN_HEIGHT // 2
bottom_y = ui.SCREEN_HEIGHT
right_x = ui.SCREEN_WIDTH

score = 0 # Keeps track of how many games the user has won
life_count = 0 # Keeps track of life count per game mode

new_word = None
guesses = []
incorrect_guesses = []

def Init(): # Initializes the word difficulty analyzer at startup
    global word_difficulty
    word_difficulty = WordDifficulty()

def choose_word(file_path):
    words = load_file(file_path)
    selected_word = ""
    while len(selected_word) < 1: # Checks to make sure chosen word is greater than 1
        selected_word = random.choice(words)
        selected_word = selected_word.replace(" ", "-")
    return selected_word

def display_word(word, guessed_letters):
    display = ""
    hyphen_added = False  # Flag to track if hyphen is already added
    for letter in word:
        if letter == "-": # If the letter is a hyphen
            if not hyphen_added:  # Add hyphen only once
                guessed_letters.append('-')
                hyphen_added = True
        if letter in guessed_letters: # If current letter in guessed letters list is a letter in the word, append it to the display as correct
            display += " " + letter + " "
        else:
            display += " _ " # Placeholder for each letter
    return display

def hangman(lives, new_game, user_input, mode):
    global score # Players score
    global new_word
    global guesses
    global incorrect_guesses
    global word_difficulty

    attempts = lives  # Set the maximum number of incorrect attempts
    
    if new_game:
        ui.text_list = ["Welcome to Hangman!"]
        file_path = "words/words.txt"
        difficulty = None
        while difficulty != mode:
            new_word = choose_word(file_path)
            difficulty = word_difficulty.evaluate_word_difficulty(new_word)
        guesses = []
        incorrect_guesses = []

    word_to_guess = new_word
    guessed_letters = guesses
    prev_guesses = [None]

    while True:
        if attempts == 0:
            ui.text_list = ["Game over! Your score is now reset.", f"The word was: {str(word_to_guess)}"]
            score = 0
            return False

        current_display = display_word(word_to_guess, guessed_letters)
        if len(guessed_letters) > len(prev_guesses) or new_game:
            if not new_game:
                prev_guesses = guessed_letters
            pass
        
        if current_display.replace(" ", "") == word_to_guess:
            ui.text_list = ["Congratulations! You guessed the word:", f"{str(word_to_guess)}"]
            if mode == "Easy":
                score += (1*lives)
            elif mode == "Med":
                print(lives)
                score += (2*lives)
            else:
                score += (3*lives)
            ui.text_list.append(f"Your current score is now: {score} pt(s)")
            return "win", current_display

        if len(user_input) > 0:
            guess = user_input.lower()

            if len(guess) != 1 or not guess.isalpha(): # if statement for invalid inputs
                ui.text_list.append("Please enter a valid single letter.")
                return attempts, current_display

            if guess in guessed_letters: # if statement for if the input is repeated
                ui.text_list.append("You've already guessed that letter. Try again.")
                return attempts, current_display

            guessed_letters.append(guess)

            if guess not in word_to_guess: # If an attempted guess is wrong
                attempts -= 1
                ui.text_list.append(f"Incorrect! Lives remaining: {str(attempts)}")
                incorrect_guesses.append(guess)
                return attempts, current_display
            
            user_input = ""
            
        else:
            return attempts, current_display

def draw_hangman(screen, lives, mode, background):
    global bottom_y
    global right_x
    global center_x
    global center_y
    global life_count

    if lives == 0:
        life_count = 10
    elif mode == "Med" or mode == "Hard":
        life_count = 7
    elif mode == "Easy":
        life_count = 10

    screen.blit(background, (0, 0))  

    # Draw the hangman's stand
    draw_stand(screen)

    # Draw score box
    score_string = f"Score: {score}pt(s)"
    score_rect = pygame.Rect(right_x - 260, 20, 250, 70)
    score_font = pygame.font.Font(None, 50)
    ui.draw_text_box(screen, score_rect, score_string, score_font)
    
    # Draw parts of the hangman based on remaining lives
    if life_count - lives >= 1: # Head
        pygame.draw.circle(screen, "blue", [center_x, bottom_y - 425], 50)
    if life_count - lives >= 2: # Neck
        pygame.draw.line(screen, "blue", [center_x, bottom_y - 375], [center_x, bottom_y - 350], 4)
    if life_count - lives >= 3: # Body
        pygame.draw.line(screen, "blue", [center_x, bottom_y - 350], [center_x, bottom_y - 270], 10)
    if life_count - lives >= 4: # Left Arm
        pygame.draw.line(screen, "blue", [center_x, bottom_y - 350], [center_x - 80, bottom_y - 320], 4)
    if life_count - lives >= 5: # Right Arm
        pygame.draw.line(screen, "blue", [center_x, bottom_y - 350], [center_x + 80, bottom_y - 320], 4)
    if life_count - lives >= 6: # Left Leg
        pygame.draw.line(screen, "blue", [center_x, bottom_y - 270], [center_x - 30, bottom_y - 170], 4)
    if life_count - lives >= 7: # Right Leg
        pygame.draw.line(screen, "blue", [center_x, bottom_y - 270], [center_x + 30, bottom_y - 170], 4)
    if life_count - lives >= 8: # Mouth
        pygame.draw.circle(screen, "white", [center_x, bottom_y - 405], 10, 4)
    if life_count - lives >= 9: # Left Eye
        pygame.draw.line(screen, "white", [center_x - 15, bottom_y - 445], [center_x - 25, bottom_y - 435], 4)
        pygame.draw.line(screen, "white", [center_x - 25, bottom_y - 445], [center_x - 15, bottom_y - 435], 4)
    if life_count - lives >= 10: # Right Eye
        pygame.draw.line(screen, "white", [center_x + 20, bottom_y - 445], [center_x + 10, bottom_y - 435], 4)
        pygame.draw.line(screen, "white", [center_x + 10, bottom_y - 445], [center_x + 20, bottom_y - 435], 4)

def draw_victory_hangman(screen):
    global bottom_y
    global right_x
    global center_x
    global center_y
    global life_count

    pygame.draw.circle(screen, "blue", [center_x, bottom_y - 325], 50) # Head
    pygame.draw.line(screen, "blue", [center_x, bottom_y - 275], [center_x, bottom_y - 250], 4) # Neck
    pygame.draw.line(screen, "blue", [center_x, bottom_y - 250], [center_x, bottom_y - 170], 10) # Body
    pygame.draw.line(screen, "blue", [center_x, bottom_y - 250], [center_x - 80, bottom_y - 280], 4) # Left Arm
    pygame.draw.line(screen, "blue", [center_x, bottom_y - 250], [center_x + 80, bottom_y - 280], 4) # Right Arm
    pygame.draw.line(screen, "blue", [center_x, bottom_y - 170], [center_x - 30, bottom_y - 70], 4) # Left Leg
    pygame.draw.line(screen, "blue", [center_x, bottom_y - 170], [center_x + 30, bottom_y - 70], 4) # Right Leg
    pygame.draw.circle(screen, "white", [center_x - 20, bottom_y - 340], 4) # Left Eye
    pygame.draw.circle(screen, "white", [center_x + 20, bottom_y - 340], 4) # Right Eye
    pygame.draw.circle(screen, "white", [center_x, bottom_y - 305], 10) # Mouth
    pygame.draw.rect(screen, "blue", [(center_x - 10), (bottom_y - 315), 20, 10]) # Mouth cover

def draw_stand(screen):
    global bottom_y
    global right_x
    global center_x
    global center_y

    # Draw the base of the stand
    pygame.draw.rect(screen, (128, 64, 0), [(center_x - 450), (bottom_y - 80), 200, 20])

    # Draw the vertical pole
    pygame.draw.rect(screen, (128, 64, 0), [(center_x - 350), (bottom_y - 580), 20, 600])

    # Draw the horizontal pole
    pygame.draw.rect(screen, (128, 64, 0), [(center_x - 350), (bottom_y - 580), 375, 20])

    # Draw the rope
    rope_color = (210, 180, 140)  # Brown color for the rope

    # Draw the rope
    pygame.draw.line(screen, rope_color, (center_x, bottom_y - 560), (center_x, bottom_y - 475), 7)