import json
from datetime import datetime
from time import sleep

from mwrogue.esports_client import EsportsClient

from LOL_Pro_API import images_api
from LOL_Pro_API.api_tools import TRACKED_REGIONS

nb_requests = 0

site = EsportsClient("lol")

def get_last_primary_tournaments_by_region():
    global nb_requests
    print("Fetching last primary tournaments by region...")

    current_date = datetime.now().strftime('%Y-%m-%d')
    tracked_regions = "'" + "', '".join(TRACKED_REGIONS) + "'"

    response = site.cargo_client.query(
        tables="Tournaments=T, Leagues=L",
        join_on="T.League=L.League",
        fields="T.Name, L.Region",
        where=f"L.Level='Primary' AND T.Date < '{current_date}' AND L.Region IN ({tracked_regions}) AND T.IsQualifier='0'",
        order_by="T.Date DESC",
    )

    nb_requests += 1
    print(f"API Request #{nb_requests}: Retrieved {len(response)} tournaments")

    last_tournaments = {}
    for tournament in response:
        region = tournament["Region"]
        if region not in last_tournaments:
            last_tournaments[region] = tournament  # Store only the first tournament per region

    print(f"Selected {len(last_tournaments)} tournaments (one per region)")
    return list(last_tournaments.values())


def get_players_in_tournament(tournament_name: str):
    global nb_requests
    print(f"Fetching players for tournament: {tournament_name}...")

    response = site.cargo_client.query(
        tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
        join_on="SP.MatchId=SG.MatchId",
        fields="SP.Name",
        group_by="SP.Name",
        where=f"SG.Tournament = '{tournament_name}'"
    )

    nb_requests += 1
    print(f"API Request #{nb_requests}: Retrieved {len(response)} players")
    return response


def get_player_kda_in_tournament(tournament_name: str, player_name: str):
    global nb_requests
    print(f"Fetching KDA for player '{player_name}' in tournament '{tournament_name}'...")

    response = site.cargo_client.query(
        tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
        join_on="SP.MatchId=SG.MatchId",
        fields="SP.Kills, SP.Deaths, SP.Assists, SP.GameId",
        group_by="SP.GameId",
        where=f"SP.Name = '{player_name}' AND SG.Tournament = '{tournament_name}'"
    )

    nb_requests += 1
    print(f"API Request #{nb_requests}: Retrieved {len(response)} games for player {player_name}")

    player_stats = {
        "kills": 0,
        "deaths": 0,
        "assists": 0
    }

    for game in response:
        player_stats["kills"] += int(game["Kills"])
        player_stats["deaths"] += int(game["Deaths"])
        player_stats["assists"] += int(game["Assists"])

    player_stats["kda"] = calc_kda(player_stats)
    print(f"Player {player_name} - KDA: {player_stats['kda']} (Kills: {player_stats['kills']}, Deaths: {player_stats['deaths']}, Assists: {player_stats['assists']})")

    return player_stats


def calc_kda(player_stats: dict):
    if player_stats["deaths"] == 0:
        return player_stats["kills"] + player_stats["assists"]
    return round((player_stats["kills"] + player_stats["assists"]) / player_stats["deaths"], 1)


def get_all_players_kda_in_tournament(tournament_name: str):
    print(f"Fetching all players' KDA for tournament '{tournament_name}'...")

    players = get_players_in_tournament(tournament_name)
    players_stats = {}

    for player in players:
        players_stats[player["Name"]] = get_player_kda_in_tournament(tournament_name, player["Name"])
        sleep(1)  # Avoid API rate-limiting

    print(f"Processed KDA for {len(players_stats)} players in tournament '{tournament_name}'")
    return players_stats


def get_top_players_in_tracked_regions():
    print("Fetching top players in tracked regions...")

    top_players = {}
    last_tournaments = get_last_primary_tournaments_by_region()

    for tournament in last_tournaments:
        tournament_name = tournament["Name"]
        print(f"Processing tournament: {tournament_name}")

        players_stats = get_all_players_kda_in_tournament(tournament_name)
        max_kda = 0

        for player_name, player_stats in players_stats.items():
            if player_stats['kda'] > max_kda:
                top_players[tournament_name] = {
                    "name": player_name,
                    "stats": player_stats
                }
                max_kda = player_stats['kda']

        print(f"Top player in {tournament_name}: {top_players[tournament_name]['name']} with KDA {top_players[tournament_name]['stats']['kda']}")

    for tournament, player in top_players.items():
        player['Image'] = images_api.get_image_url_with_player_name(player['name'])

    with open("top_players.json", "w") as file:
        json.dump(top_players, file, indent=4)
        print("Saved top players data to 'top_players.json'")

    return top_players


if __name__ == "__main__":
    print(json.dumps(get_top_players_in_tracked_regions(), indent=2))