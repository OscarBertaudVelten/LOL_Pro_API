import json

from mwrogue.esports_client import EsportsClient
def get_player_matches(player_name):
    site = EsportsClient("lol")
    response = site.cargo_client.query(
        tables="ScoreboardPlayers=SP",
        fields="SP.Link, SP.Team, SP.Champion, SP.Kills, SP.Deaths, SP.Assists",
        where=f"SP.Link='{player_name}'",
        order_by="SP.DateTime_UTC DESC",
        limit=10
    )

    print(json.dumps(response, indent=2))

get_player_matches("Yike")
