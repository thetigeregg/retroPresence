import csv

csv_path = "./data/games-list.csv"


def load_games_list():
    games_dict = {}
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= 5:
                break
            games_dict[row["name"]] = row
    return games_dict


if __name__ == "__main__":
    games_dict = load_games_list()
    desired_game_name = input("Please enter a game name: ")
    if desired_game_name in games_dict:
        print(games_dict[desired_game_name])
    else:
        print("Name not found.")
