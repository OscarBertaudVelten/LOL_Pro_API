from mwrogue.esports_client import EsportsClient
import json
from datetime import datetime
from api_tools import get_attribute_value

site = EsportsClient("lol")

class TeamStats:
    """
    Represents the stats of a team in a game.

    Attributes:
        Name (str): Name of the team (e.g., 'Karmine Corp').
        Score (int): Score of the team (e.g., 3).
        Bans (str): Banned champions for the team (e.g., 'Nidalee,Yone,Ambessa,Ziggs,Caitlyn').
        Picks (str): Champion picks for the team (e.g., 'Kennen,Pantheon,Galio,Draven,Renata Glasc').
        Players (str): Players in the team (e.g., 'Canna,Yike,Vladi,Caliste,Targamas').
        Dragons (int): Number of dragons taken by the team (e.g., 2).
        Barons (int): Number of barons taken by the team (e.g., 0).
        Towers (int): Number of towers destroyed by the team (e.g., 0).
        Gold (int): Gold earned by the team (e.g., 60785).
        Kills (int): Kills made by the team (e.g., 10).
        RiftHeralds (int): Rift heralds secured by the team (e.g., 1).
        VoidGrubs (int): Void Grubs secured by the team (e.g., 4).
        Atakhans (int): Atakhans secured by the team (e.g., 0).
        Inhibitors (int): Inhibitors destroyed by the team (e.g., 0).
    """

    def __init__(self, name: str, score: int, bans: str, picks: str, players: str, dragons: int, barons: int, towers: int,
                 gold: int, kills: int, riftheralds: int, voidgrubs: int, atakhans: int, inhibitors: int):
        self.Name = name
        self.Score = score
        self.Bans = bans
        self.Picks = picks
        self.Players = players
        self.Dragons = dragons
        self.Barons = barons
        self.Towers = towers
        self.Gold = gold
        self.Kills = kills
        self.RiftHeralds = riftheralds
        self.VoidGrubs = voidgrubs
        self.Atakhans = atakhans
        self.Inhibitors = inhibitors


    def __str__(self):
        return (f"Team Name: {self.Name}\n"
                f"Score: {self.Score}\n"
                f"Bans: {self.Bans}\n"
                f"Picks: {self.Picks}\n"
                f"Players: {self.Players}\n"
                f"Dragons: {self.Dragons}\n"
                f"Barons: {self.Barons}\n"
                f"Towers: {self.Towers}\n"
                f"Gold: {self.Gold}\n"
                f"Kills: {self.Kills}\n"
                f"Rift Heralds: {self.RiftHeralds}\n"
                f"Void Grubs: {self.VoidGrubs}\n"
                f"Atakhans: {self.Atakhans}\n"
                f"Inhibitors: {self.Inhibitors}")


    def to_short_str(self):
        return (f"Team Name: {self.Name}\n"
                f"Score: {self.Score}\n"
                f"Picks: {self.Picks}\n"
                f"Players: {self.Players}")



class ScoreboardGame:
    """
    Represents a game in the scoreboard with detailed characteristics.

    Attributes:
        Tournament (str): Name of the tournament (e.g., 'First Stand 2025').
        Winner (int): Index of the winner (1 or 2).
        DateTimeUTC (str): Date and time of the game in UTC (e.g., '2025-03-16 10:52:00').
        DST (str): Daylight saving time (e.g., 'spring').
        Gamelength (str): Length of the game (e.g., '35:53').
        Patch (str): Patch version for the game (e.g., '25.05').
        Team1Stats (TeamStats): Stats for team 1
        Team2Stats (TeamStats): Stats for team 2
        VOD (str): Link to the VOD of the game (e.g., 'https://youtu.be/ETH4A5-XKpQ?t=4').
        MatchId (str): Unique identifier for the match (e.g., '2025 First Stand_Finals_1').
    """

    Tournament: str
    Winner: int
    DateTimeUTC: str
    DST: str
    Gamelength: str
    Patch: str
    Team1Stats: TeamStats
    Team2Stats: TeamStats
    VOD: str
    MatchId: str


    def __init__(self, match_id: str):
        # Fetch game data from the database based on the match_id
        response = site.cargo_client.query(
            tables="ScoreboardGames=SG",
            fields="SG.Tournament,SG.Team1,SG.Team2,SG.Winner,SG.DateTimeUTC,SG.DST,SG.Team1Score,SG.Team2Score,SG.Gamelength,SG.Patch,SG.Team1Bans,SG.Team2Bans,SG.Team1Picks,SG.Team2Picks,SG.Team1Players,SG.Team2Players,SG.Team1Dragons,SG.Team2Dragons,SG.Team1Barons,SG.Team2Barons,SG.Team1Towers,SG.Team2Towers,SG.Team1Gold,SG.Team2Gold,SG.Team1Kills,SG.Team2Kills,SG.Team1RiftHeralds,SG.Team2RiftHeralds,SG.Team1VoidGrubs,SG.Team2VoidGrubs,SG.Team1Atakhans,SG.Team2Atakhans,SG.Team1Inhibitors,SG.Team2Inhibitors,SG.VOD,SG.MatchId",
            where=f"SG.MatchId = '{match_id}'"
        )

        # Check if we got any data for the match
        if response and len(response) > 0:
            game_data = response[0]

            # Populate basic match details
            self.Tournament: str = game_data['Tournament']
            self.Winner: int = game_data['Winner']
            self.DateTimeUTC: str = game_data['DateTimeUTC']
            self.DST: str = game_data['DST']
            self.Gamelength: str = game_data['Gamelength']
            self.Patch: str = game_data['Patch']
            self.VOD: str = game_data['VOD']
            self.MatchId: str = game_data['MatchId']

            # Store team stats using TeamStats class
            self.Team1Stats = TeamStats(
                game_data['Team1'], game_data['Team1Score'], game_data['Team1Bans'], game_data['Team1Picks'],
                game_data['Team1Players'], game_data['Team1Dragons'], game_data['Team1Barons'],
                game_data['Team1Towers'], game_data['Team1Gold'], game_data['Team1Kills'],
                game_data['Team1RiftHeralds'], game_data['Team1VoidGrubs'], game_data['Team1Atakhans'],
                game_data['Team1Inhibitors']
            )

            self.Team2Stats = TeamStats(
                game_data['Team2'], game_data['Team2Score'], game_data['Team2Bans'], game_data['Team2Picks'],
                game_data['Team2Players'], game_data['Team2Dragons'], game_data['Team2Barons'],
                game_data['Team2Towers'], game_data['Team2Gold'], game_data['Team2Kills'],
                game_data['Team2RiftHeralds'], game_data['Team2VoidGrubs'], game_data['Team2Atakhans'],
                game_data['Team2Inhibitors']
            )

        else:
            raise ValueError(f"Game with MatchId '{match_id}' not found in the database.")

    def __str__(self):
        return (f"Match ID: {self.MatchId}\n"
                f"Tournament: {self.Tournament}\n"
                f"Team 1: {self.Team1Stats.Name}\n"
                f"Team 2: {self.Team2Stats.Name}\n"
                f"Winner: {'Team 1' if self.Winner == 1 else 'Team 2'}\n"
                f"Date and Time: {self.DateTimeUTC}\n"
                f"Game Length: {self.Gamelength}\n"
                f"VOD: {self.VOD}")


def get_game_scoreboard_example():
    response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields=(
            "OverviewPage,Tournament,Team1,Team2,WinTeam,LossTeam,DateTime_UTC,DST,"
            "Team1Score,Team2Score,Winner,Gamelength,Gamelength_Number,Team1Bans,"
            "Team2Bans,Team1Picks,Team2Picks,Team1Players,Team2Players,Team1Dragons,"
            "Team2Dragons,Team1Barons,Team2Barons,Team1Towers,Team2Towers,Team1Gold,"
            "Team2Gold,Team1Kills,Team2Kills,Team1RiftHeralds,Team2RiftHeralds,"
            "Team1VoidGrubs,Team2VoidGrubs,Team1Atakhans,Team2Atakhans,Team1Inhibitors,"
            "Team2Inhibitors,Patch,LegacyPatch,PatchSort,MatchHistory,VOD,N_Page,"
            "N_MatchInTab,N_MatchInPage,N_GameInMatch,Gamename,UniqueLine,GameId,"
            "MatchId,RiotPlatformGameId,RiotPlatformId,RiotGameId,RiotHash,RiotVersion"
        ),
        where=f"GameId='2025 First Stand_Finals_1_3'"
    )

    return json.dumps(response, indent=2)


def get_nb_games_in_match(match_id: str) -> int:
    response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields="COUNT(*)=nbGames",
        where=f"MatchId='{match_id}'"
    )

    return response[0]['nbGames']

# Example usage
print(get_nb_games_in_match('2025 First Stand_Finals_1'))
