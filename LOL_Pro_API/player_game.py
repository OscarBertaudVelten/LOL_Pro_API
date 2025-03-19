from mwrogue.esports_client import EsportsClient
import datetime as dt
import json
from LOL_Pro_API import tournaments_api

# Specify the player whose recent games you want to fetch
player_name = "Yike"  # Replace with the player's name
site = EsportsClient("lol")

# Define the date range for "recent" games (last 30 days, for example)
date_today = dt.datetime.now().date()
date_last_30_days = date_today - dt.timedelta(days=30)


response = site.cargo_client.query(
    tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
    join_on="SP.GameId=SG.GameId",
    fields="SG.Tournament, SG.Gamelength, SG.VOD, SG.Patch, SP.DateTime_UTC, SP.PlayerWin, SP.Side, SP.Team, SP.TeamVs, SP.TeamGold, SP.Champion, SP.IngameRole, SP.Kills, SP.Deaths, SP.Assists, SP.SummonerSpells, SP.KeystoneRune, SP.Trinket, SP.CS, SP.Gold, SP.DamageToChampions, SP.Items, SP.GameId, SP.MatchId",
    where=f"SG.Tournament IN ({tournaments_api.getPrimaryTournaments()})",
    order_by="SP.DateTime_UTC DESC",
    limit=10
)


def getPlayerGameExample():
    response = site.cargo_client.query(
        tables="ScoreboardPlayers=SP",
        fields="OverviewPage,Name,Link,Champion,Kills,Deaths,Assists,SummonerSpells,Gold,CS,DamageToChampions,VisionScore,Items,Trinket,KeystoneMastery,KeystoneRune,PrimaryTree,SecondaryTree,Runes,TeamKills,TeamGold,Team,TeamVs,Time,PlayerWin,DateTime_UTC,DST,Tournament,Role,Role_Number,IngameRole,Side,UniqueLine,UniqueLineVs,UniqueRole,UniqueRoleVs,GameId,MatchId,GameTeamId,GameRoleId,GameRoleIdVs,StatsPage",
        where=f"SP.Name='{player_name}'",
        order_by="SP.DateTime_UTC DESC",
        limit=1
    )
    return json.dumps(response, indent=2)

#print(getPlayerGameExample())
print(json.dumps(response, indent=2))