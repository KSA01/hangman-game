
import json

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