from mwrogue.esports_client import EsportsClient
import json
from LOL_Pro_API.unused import tournaments_api

site = EsportsClient("lol")

primary_recent_tournaments = tournaments_api.get_primary_recent_tournaments()

def get_last_n_primary_games():
    response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields="Tournament, Team1, Team2, WinTeam, DateTime_UTC, Team1Score, Team2Score, "
    )
"""
response = site.cargo_client.query(
    tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
    join_on="SP.GameId=SG.GameId",
    fields="SG.Tournament, SG.Gamelength, SG.VOD, SG.Patch, SP.DateTime_UTC, SP.PlayerWin, SP.Side, SP.Team, SP.TeamVs, SP.TeamGold, SP.Champion, SP.IngameRole, SP.Kills, SP.Deaths, SP.Assists, SP.SummonerSpells, SP.KeystoneRune, SP.Trinket, SP.CS, SP.Gold, SP.DamageToChampions, SP.Items, SP.GameId, SP.MatchId",
    where=f"SG.Tournament IN ({primary_recent_tournaments})",
    order_by="SP.DateTime_UTC DESC",
    limit=10
)
"""

def get_player_game_example():
    player_example_response = site.cargo_client.query(
        tables="ScoreboardPlayers=SP",
        fields="OverviewPage,Name,Link,Champion,Kills,Deaths,Assists,SummonerSpells,Gold,CS,DamageToChampions,VisionScore,Items,Trinket,KeystoneMastery,KeystoneRune,PrimaryTree,SecondaryTree,Runes,TeamKills,TeamGold,Team,TeamVs,Time,PlayerWin,DateTime_UTC,DST,Tournament,Role,Role_Number,IngameRole,Side,UniqueLine,UniqueLineVs,UniqueRole,UniqueRoleVs,GameId,MatchId,GameTeamId,GameRoleId,GameRoleIdVs,StatsPage",
        where=f"SP.Name='Yike'",
        order_by="SP.DateTime_UTC DESC",
        limit=1
    )
    return json.dumps(player_example_response, indent=2)

#print(get_player_game_example())