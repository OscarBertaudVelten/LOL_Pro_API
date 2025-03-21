from mwrogue.esports_client import EsportsClient
import json
from datetime import datetime
from api_tools import get_attribute_value

site = EsportsClient("lol")

response = site.cargo_client.query(
    tables="ScoreboardGames",
    fields="N_GameInMatch",
    where=f"MatchId = '2025 First Stand_Finals_1'"
)
print(response)