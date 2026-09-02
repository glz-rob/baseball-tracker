import json
import os
import platform
import subprocess
from datetime import UTC, datetime

import requests

URL = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"


def get_todays_games():
    """
    Get the games info once per day, then reuse that info unless the file is deleted.
    """
    file_path = f"res/games/{datetime.now(tz=UTC).strftime('%Y-%m-%d')}-games.json"

    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            json.dump(requests.get(URL).json(), f, indent=4)

    with open(file_path, "r") as f:
        return json.load(f)["dates"][0]["games"]


def show_results(games):
    print(f" --- GAMES ON {datetime.now(tz=UTC).strftime('%m %d, %Y')} --- ")

    for game in games:
        away = game["teams"]["away"]
        home = game["teams"]["home"]

        print(
            f"{game['status']['abstractGameState']}: "
            + f"{away['team']['name']} @ {home['team']['name']} "
            + f"{away['score']} - {home['score']}"
        )


def other():
    # res = requests.get(URL)
    # res: dict = res.json()

    # print(res["dates"])
    with open("res/test.json", "r") as f:
        data = json.load(f)

    games = [game for game in data["dates"][0]["games"]]

    print(f"--- GAMES ON {data['dates'][0]['date']} ---")

    for game in games:
        away = game["teams"]["away"]
        home = game["teams"]["home"]

        print(
            f"{game['status']['abstractGameState']}: "
            + f"{away['team']['name']} @ "
            + f"{home['team']['name']}"
            # + f"{away['score']} - {home['score']}"
        )

    with open("res/written.json", "w") as f:
        json.dump(data, f, indent=4)


def main():
    games = get_todays_games()
    show_results(games)


if __name__ == "__main__":
    main()
