import json
import os
from datetime import UTC, datetime

import requests

URL = "https://statsapi.mlb.com/api/v1/"
SPORT_ID = "1"


def get_todays_games():
    """
    Get the games info once per day, then reuse that info unless the file is deleted.
    """
    file_path = f"res/games/{datetime.now(tz=UTC).strftime('%Y-%m-%d')}-games.json"

    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            json.dump(requests.get(URL + f"schedule?{SPORT_ID}=1").json(), f, indent=4)

    with open(file_path, "r") as f:
        return json.load(f)["dates"][0]["games"]


def get_players():
    """
    Get all players from json if available, else makes a request
    """
    file_path = "res/players.json"

    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            json.dump(
                requests.get(URL + f"sports/{SPORT_ID}/players").json(), f, indent=4
            )

    with open(file_path, "r") as f:
        return json.load(f)["people"]


def get_teams():
    """
    Get all teams from json if available, else makes a request
    """
    file_path = "res/teams.json"

    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            json.dump(
                requests.get(URL + f"/teams?sportId={SPORT_ID}").json(), f, indent=4
            )

    with open(file_path, "r") as f:
        return json.load(f)["teams"]


def show_results(games):
    print(
        f" {'=' * 10} GAMES ON {datetime.now(tz=UTC).strftime('%m %d, %Y')} {'=' * 10} "
    )

    for game in games:
        away: dict = game["teams"]["away"]
        home: dict = game["teams"]["home"]

        print(
            f"{game['status']['abstractGameState']}: "
            + f"{away['team']['name']} @ {home['team']['name']} "
            + f"{away.get('score', '0')} - {home.get('score', '0')}"
        )


def main():
    pass


if __name__ == "__main__":
    main()
