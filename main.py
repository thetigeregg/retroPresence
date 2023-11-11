import csv
import unidecode
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


csv_path = "./data/games-list.csv"


def normalize_game_name(name):
    return unidecode.unidecode(name.lower())


def load_games_list():
    games_dict = {}
    with open(csv_path, "r") as file:
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


if __name__ == "__main__":
    game_name_completer = WordCompleter(get_game_name_suggestions(), ignore_case=True)
    desired_game_name = prompt(
        "Please enter a game name: ", completer=game_name_completer
    )
