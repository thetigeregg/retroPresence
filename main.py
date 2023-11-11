import csv
import unidecode
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


csv_path = "./data/games-list.csv"


class GameNameCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.text_before_cursor.lower()
        for game_name in get_game_name_suggestions():
            if word.startswith("."):
                if game_name.startswith(word):
                    yield Completion(game_name, start_position=-len(word))
            else:
                if game_name.lstrip(".").startswith(word):
                    yield Completion(game_name, start_position=-len(word))


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
    game_name_completer = GameNameCompleter()
    desired_game_name = prompt(
        "Please enter a game name: ", completer=game_name_completer
    )
