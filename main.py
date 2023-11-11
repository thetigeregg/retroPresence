import csv
import unidecode
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import json
from pypresence import Presence
import time

config_path = "./data/config.json"
modern_platforms = [
    "PC (Microsoft Windows)",
    "PlayStation 4",
    "PlayStation 5",
    "Android",
    "Nintendo Switch",
]
region_labels=["Japan","Europe"]
platform_clean_names = {
    "Sega Mega Drive/Genesis": "Sega Genesis",
    "Super Nintendo Entertainment System (SNES)": "SNES",
    "Nintendo Entertainment System (NES)": "NES",
    "Family Computer Disk System": "Famicom Disk System (NES)",
}


def get_value_from_config_file(key):
    with open(config_path, "r") as file:
        data = json.load(file)
    return data.get(key, None)


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        for game_name in get_game_name_suggestions():
            if word in game_name:
                yield Completion(game_name, start_position=-len(word))


def normalize_game_name(name):
    return unidecode.unidecode(name.lower())


def get_final_platform(platform):
    if platform in platform_clean_names:
        return platform_clean_names[platform]
    else:
        return platform
    
def split_and_check(input_string, check_list):
    # Split the input string into a list of trimmed strings
    split_list = [s.strip() for s in input_string.split(',')]

    # Check which elements of split_list are in check_list
    in_list = [s for s in split_list if s in check_list]

    if in_list[0]
        return in_list[0]
    else
        return null

def load_games_list():
    games_dict = {}
    with open(get_value_from_config_file("csvPath"), "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= 5:
                break
            normalized_name = normalize_game_name(row["name"])
            games_dict[normalized_name] = row
    return games_dict


def get_game_name_suggestions():
    games_dict = load_games_list()
    return list(games_dict.keys())


def get_client_id(platform):
    if platform in modern_platforms:
        return get_value_from_config_file("modernClientId")
    else:
        return get_value_from_config_file("retroClientId")

def get_year(date_string):
    return date_string.split('-')[0]


def set_discord_presence(game_data):
    client_id = get_client_id(
        game_data["platform"]
    )  # Replace with your app's client ID
    RPC = Presence(client_id)
    RPC.connect()

    start_time = int(time.time())
    platform_display = get_final_platform(game_data["platform"])
    region_display = split_and_check(game_data["labels"], region_labels)
    if region_display:
        region_display = ", " + region_display
    year = get_year(game_data["release_date"])
    state_display = platform_display + " (" + (year or "") + (region_display or "") + ")"

    
    # Set the Rich Presence data based on game_data
    RPC.update(
        details=game_data["name"],
        large_image="game_image",  # Replace with your game's image key
        large_text=game_data["name"],  # Replace with your invite URL
        start=start_time,
        small_image="small",
        state=state_display,
    )


if __name__ == "__main__":
    game_name_completer = GameNameCompleter()
    desired_game_name = prompt(
        "Please enter a game name: ", completer=game_name_completer
    )
    game_data = load_games_list()[normalize_game_name(desired_game_name)]
    set_discord_presence(game_data)
    while True:  # Keep the script running
        time.sleep(15)
