import json

from mwrogue.esports_client import EsportsClient
from LOL_Pro_API.api_tools import get_attribute_value

site = EsportsClient("lol")

class TeamStats:
    """
    Represents the stats of a team in a game.

    Attributes:
        Name (str): Name of the team (e.g., 'Karmine Corp').
        Score (int): Score of the team (e.g., 3).
        Bans (list): Banned champions for the team (e.g., 'Nidalee,Yone,Ambessa,Ziggs,Caitlyn').
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

    Name: str
    Score: int
    Bans: [str]
    Picks: [str]
    Players: [str]
    Dragons: int
    Barons: int
    Towers: int
    Gold: int
    Kills: int
    RiftHeralds: int
    VoidGrubs: int
    Atakhans: int
    Inhibitors: int


    def __init__(self, team_stats):

        default_values = {
            'Name': '',
            'Score': 0,
            'Dragons': 0,
            'Barons': 0,
            'Towers': 0,
            'Gold': 0,
            'Kills': 0,
            'RiftHeralds': 0,
            'VoidGrubs': 0,
            'Atakhans': 0,
            'Inhibitors': 0
        }

        for key, default_value in default_values.items():
            setattr(self, key, get_attribute_value(team_stats, key, default_value))

        self.Bans = [ban.strip() for ban in team_stats['Bans'].split(',')]
        self.Picks = [pick.strip() for pick in team_stats['Picks'].split(',')]
        self.Players = [player.strip() for player in team_stats['Players'].split(',')]


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


    def to_dict(self):
        """
        Convert the TeamStats instance to a dictionary.
        """
        return {
            'Name': self.Name,
            'Score': self.Score,
            'Bans': self.Bans,
            'Picks': self.Picks,
            'Players': self.Players,
            'Dragons': self.Dragons,
            'Barons': self.Barons,
            'Towers': self.Towers,
            'Gold': self.Gold,
            'Kills': self.Kills,
            'RiftHeralds': self.RiftHeralds,
            'VoidGrubs': self.VoidGrubs,
            'Atakhans': self.Atakhans,
            'Inhibitors': self.Inhibitors
        }



class GameScoreboard:
    """
    Represents a game in the scoreboard with detailed characteristics.

    Attributes:
        Tournament (str): Name of the tournament (e.g., 'First Stand 2025').
        Winner (int): Index of the winner (1 or 2).
        DateTime (str): Date and time of the game in UTC (e.g., '2025-03-16 10:52:00').
        DST (str): Daylight saving time (e.g., 'spring').
        Gamelength (str): Length of the game (e.g., '35:53').
        Patch (str): Patch version for the game (e.g., '25.05').
        Team1Stats (TeamStats): Stats for team 1
        Team2Stats (TeamStats): Stats for team 2
        VOD (str): Link to the VOD of the game (e.g., 'https://youtu.be/ETH4A5-XKpQ?t=4').
        GameId (str): Unique identifier for the game (e.g., '2025 First Stand_Finals_1').
    """

    Tournament: str
    Winner: int
    DateTime: str
    DST: str
    Gamelength: str
    Patch: str
    Team1Stats: TeamStats
    Team2Stats: TeamStats
    VOD: str
    GameId: str


    def __init__(self, game_id: str):
        # Fetch game data from the database based on the game_id
        response = site.cargo_client.query(
            tables="ScoreboardGames",
            fields="Tournament, Team1, Team2, Winner, DateTime_UTC=DateTime, DST, Team1Score, Team2Score, Gamelength, Patch, Team1Bans, Team2Bans, Team1Picks, Team2Picks, Team1Players, Team2Players, Team1Dragons, Team2Dragons, Team1Barons, Team2Barons, Team1Towers, Team2Towers, Team1Gold, Team2Gold, Team1Kills, Team2Kills, Team1RiftHeralds, Team2RiftHeralds, Team1VoidGrubs, Team2VoidGrubs, Team1Atakhans, Team2Atakhans, Team1Inhibitors, Team2Inhibitors, VOD, GameId",
            where=f"GameId = '{game_id}'"
        )

        # Check if we got any data for the game
        if response and len(response) > 0:
            game_data = response[0]
            print(response[0]['DateTime'])

            default_values = {
                'Tournament': '',
                'Winner': 1,
                'DateTime': '',
                'DST': '',
                'Gamelength': '',
                'Patch': '',
                'VOD': '',
                'GameId': ''
            }

            # Populate basic game details
            for key, default_value in default_values.items():
                setattr(self, key, get_attribute_value(game_data, key, default_value))

            # Store team stats using TeamStats class
            self.Team1Stats = TeamStats({
                'Name': game_data['Team1'], 'Score': game_data['Team1Score'], 'Bans': game_data['Team1Bans'],
                'Picks': game_data['Team1Picks'], 'Players': game_data['Team1Players'], 'Dragons': game_data['Team1Dragons'],
                'Barons': game_data['Team1Barons'], 'Towers': game_data['Team1Towers'], 'Gold': game_data['Team1Gold'],
                'Kills': game_data['Team1Kills'], 'RiftHeralds': game_data['Team1RiftHeralds'],
                'VoidGrubs': game_data['Team1VoidGrubs'], 'Atakhans': game_data['Team1Atakhans'], 'Inhibitors': game_data['Team1Inhibitors']
            })

            self.Team2Stats = TeamStats({
                'Name': game_data['Team2'], 'Score': game_data['Team2Score'], 'Bans': game_data['Team2Bans'],
                'Picks': game_data['Team2Picks'], 'Players': game_data['Team2Players'], 'Dragons': game_data['Team2Dragons'],
                'Barons': game_data['Team2Barons'], 'Towers': game_data['Team2Towers'], 'Gold': game_data['Team2Gold'],
                'Kills': game_data['Team2Kills'], 'RiftHeralds': game_data['Team2RiftHeralds'],
                'VoidGrubs': game_data['Team2VoidGrubs'], 'Atakhans': game_data['Team2Atakhans'], 'Inhibitors': game_data['Team2Inhibitors']
            })

        else:
            raise ValueError(f"Game with gameId '{game_id}' not found in the database.")

    def __str__(self):
        return (f"game ID: {self.GameId}\n"
                f"Tournament: {self.Tournament}\n"
                f"Team 1: {self.Team1Stats.Name}\n"
                f"Team 2: {self.Team2Stats.Name}\n"
                f"Winner: {'Team 1' if self.Winner == 1 else 'Team 2'}\n"
                f"Date and Time: {self.DateTime}\n"
                f"Game Length: {self.Gamelength}\n"
                f"VOD: {self.VOD}")

    def to_dict(self):
        """
        Convert the GameScoreboard instance to a dictionary.
        """
        return {
            'Tournament': self.Tournament,
            'Winner': self.Winner,
            'DateTime_UTC': self.DateTime,
            'DST': self.DST,
            'Gamelength': self.Gamelength,
            'Patch': self.Patch,
            'VOD': self.VOD,
            'GameId': self.GameId,
            'Team1Stats': self.Team1Stats.to_dict(),
            'Team2Stats': self.Team2Stats.to_dict()
        }





def get_game_scoreboard_example():
    response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields=(
            "OverviewPage,Tournament,Team1,Team2,WinTeam,LossTeam,DateTime_UTC=DateTime,DST,"
            "Team1Score,Team2Score,Winner,Gamelength,Gamelength_Number,Team1Bans,"
            "Team2Bans,Team1Picks,Team2Picks,Team1Players,Team2Players,Team1Dragons,"
            "Team2Dragons,Team1Barons,Team2Barons,Team1Towers,Team2Towers,Team1Gold,"
            "Team2Gold,Team1Kills,Team2Kills,Team1RiftHeralds,Team2RiftHeralds,"
            "Team1VoidGrubs,Team2VoidGrubs,Team1Atakhans,Team2Atakhans,Team1Inhibitors,"
            "Team2Inhibitors,Patch,LegacyPatch,PatchSort,gameHistory,VOD,N_Page,"
            "N_gameInTab,N_gameInPage,N_GameIngame,Gamename,UniqueLine,GameId,"
            "gameId,RiotPlatformGameId,RiotPlatformId,RiotGameId,RiotHash,RiotVersion"
        ),
        where=f"GameId='2025 First Stand_Finals_1_3'"
    )

    return response[0]


def get_nb_games_in_game(game_id: str) -> int:
    response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields="COUNT(*)=nbGames",
        where=f"gameId='{game_id}'"
    )

    return response[0]['nbGames']

