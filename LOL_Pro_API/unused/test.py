from mwrogue.esports_client import EsportsClient
import json
from datetime import datetime


site = EsportsClient("lol")

response = site.cargo_client.query(
    tables="ScoreboardGames",
    fields="Tournament, GameId",
    where=f"GameId = '2025 First Stand_Finals_1_3'"
)
