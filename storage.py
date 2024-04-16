
import json

def load_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def add_custom_words(file_path, words_list): # Adds the custom words to the game's word list
    with open(file_path, 'r+') as file:
        #file.write('\n')
        lines = file.readlines()
        for word in words_list:
            if word.strip() not in lines:
                file.write('\n' + word.strip())

        # Removes empty line at the end
        '''file.seek(0, 2)  # Move to the end of the file
        pos = file.tell() - 1  # Start at the end of the file
        while pos > 0 and file.read(1) != "\n":  # Move backwards until a newline is found
            pos -= 1
            file.seek(pos, 0)
        if pos > 0:
            file.seek(pos, 0)
            file.truncate()'''

    with open("data/addedwords.json", "w") as json_file:
        json.dump(words_list, json_file, indent=4)

def get_custom_words(): # Retrieves the custom words added for game initialize
    try:
        with open("data/addedwords.json", "r") as json_file:
            try:
                data = json.load(json_file)
                return data
            except json.JSONDecodeError:
                return None
    except FileNotFoundError:
        return None

def del_custom_words(file_path, words_list): # Removes the custom words from the words list
    if words_list:
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)  # Moves the file pointer to the beginning
            for line in lines:
                if line.strip() not in words_list:
                    file.write(line)  # Write the line back to the file if it's not in the list
            file.truncate()  # Truncate the file to remove any remaining content after the updated lines

            # Removes empty line at the end
            file.seek(0, 2)  # Move to the end of the file
            pos = file.tell() - 1  # Start at the end of the file
            while pos > 0 and file.read(1) != "\n":  # Move backwards until a newline is found
                pos -= 1
                file.seek(pos, 0)
            if pos > 0:
                file.seek(pos, 0)
                file.truncate()
        
        words_list = {}
        with open("data/addedwords.json", "w") as json_file:
            json.dump(words_list, json_file, indent=4)

def save_data(user, score, streak, reset=False):
    if not reset:
        data = load_data()  # Load existing data
        if data is None:
            data = []  # Initialize empty list if no data exists
        
        user_exists = False
        for entry in data:
            if entry["user"] == user:
                user_exists = True
                if score > entry["score"]:
                    entry["score"] = score
                if streak > entry["word-streak"]:
                    entry["word-streak"] = streak
                break  # Found the user, no need to continue
        
        if not user_exists:
            new_data = {"user": user, "score": score, "word-streak": streak}
            data.append(new_data)  # Add new user data
        
        with open("data/gamedata.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

    # If the user chooses to reset their streaks
    elif reset:
        data = load_data()  # Load existing data
        if data is None:
            data = []  # Initialize empty list if no data exists
        
        for entry in data:
            if entry["user"] == user:
                entry["score"] = 0
                entry["word-streak"] = 0

        with open("data/gamedata.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

def load_data():
    try:
        with open("data/gamedata.json", "r") as json_file:
            try:
                data = json.load(json_file)
                return data
            except json.JSONDecodeError:
                return None
    except FileNotFoundError:
        return None