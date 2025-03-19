from mwrogue.esports_client import EsportsClient
import json

site = EsportsClient("lol")

"""
OverviewPage (str)
Name (str)
Link (str)
Champion (str)
Kills (int)
Deaths (int)
Assists (int)
SummonerSpells (str) (list ,)
Gold (int)
CS (int)
DamageToChampions (int)
VisionScore (int)
Items (str) (list ;)
Trinket (str)
KeystoneMastery (str)
KeystoneRune (str)
PrimaryTree (str)
SecondaryTree (str)
Runes - Text
TeamKills (int)
TeamGold (int)
Team (str)
TeamVs (str)
Time (str)
PlayerWin (str)
DateTime_UTC (str)
DST (str)
Tournament (str)
Role (str)
Role_Number (int)
IngameRole (str)
Side (int)
UniqueLine (str)
UniqueLineVs (str)
UniqueRole (str)
UniqueRoleVs (str)
GameId (str)
MatchId (str)
GameTeamId (str)
GameRoleId (str)
GameRoleIdVs (str)
StatsPage (str)
"""

from mwrogue.esports_client import EsportsClient
import datetime as dt

# Specify the player whose recent games you want to fetch
player_name = "Yike"  # Replace with the player's name

# Define the date range for "recent" games (last 30 days, for example)
date_today = dt.datetime.now().date()
date_last_30_days = date_today - dt.timedelta(days=30)

# Query the database for the player's recent games
response = site.cargo_client.query(
    tables="ScoreboardGames=SG, ScoreboardPlayers=SP, Tournaments=T",
    join_on="SG.GameId=SP.GameId, SG.OverviewPage=T.OverviewPage",
    fields="T.Name=Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SP.Champion, SP.Kills, SP.Deaths, SP.Assists, SP.Link, SP.Role",
    where="SP.Link='%s' AND SG.DateTime_UTC >= '%s'" % (player_name, str(date_last_30_days)),
    order_by="SG.DateTime_UTC DESC",
    limit=10  # Adjust the limit for the number of recent games you want
)

# Output the results
for game in response:
    print(f"Tournament: {game['Tournament']}")
    print(f"Teams: {game['Team1']} vs {game['Team2']}")
    print(f"Winner: {game['Winner']}")
    print(f"Champion: {game['Champion']}")
    print(f"Stats: {game['Kills']} Kills | {game['Deaths']} Deaths | {game['Assists']} Assists")
    print('-' * 40)
