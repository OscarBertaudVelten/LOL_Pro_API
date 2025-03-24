import json
from typing import List

from mwrogue.esports_client import EsportsClient

from LOL_Pro_API import images_api
from LOL_Pro_API.game_scoreboard_api import GameScoreboard
from LOL_Pro_API.teams_api import Team

site = EsportsClient("lol")

class MatchScoreboard:
    """
    Represents a match's scoreboard, including the list of games played, the teams, and the final scores.

    Attributes:
        match_id (str): The unique match identifier.
        Games (List[GameScoreboard]): List of ScoreboardGame objects containing the data of the games.
        Team1Score (int): Total score of team 1 from the last game.
        Team2Score (int): Total score of team 2 from the last game.
        DateTime (str): The UTC DateTime of the first game in the match.
        DST (str): Daylight saving time of the first game.
        Team1 (Team object): Team1 details (first team).
        Team2 (Team object): Team2 details (second team).
    """

    MatchId: str
    Team1: Team
    Team2: Team
    Games: List[GameScoreboard]
    Team1Score: int
    Team2Score: int
    DateTime: str
    DST: str

    def __init__(self, match_id: str):
        self.match_id = match_id
        self.Team1Score = 0
        self.Team2Score = 0
        self.DateTime = ''
        self.DST = ''

        self.Games = []
        self.get_games_from_match(match_id)

        if self.Games:
            # Store the DateTime and DST from the first game
            self.DateTime = self.Games[0].DateTime
            self.DST = self.Games[0].DST

            self.Team1Score = self.Games[-1].Team1Stats.Score
            self.Team2Score = self.Games[-1].Team2Stats.Score

            self.Team1 = Team(self.Games[-1].Team1Stats.Name)
            self.Team2 = Team(self.Games[-1].Team2Stats.Name)
        else:
            self.Team1 = None
            self.Team2 = None
            self.Team1Score = 0
            self.Team2Score = 0


    def get_games_from_match(self, match_id: str):
        """
        Queries the database to get all games related to the match_id and returns them as a list of GameScoreboard objects.
        """
        response = site.cargo_client.query(
            tables="ScoreboardGames",
            fields="Tournament, Team1, Team2, Winner, DateTime_UTC=DateTime, DST, Team1Score, Team2Score, "
                   "Gamelength, Patch, Team1Bans, Team2Bans, Team1Picks, Team2Picks, Team1Players, "
                   "Team2Players, Team1Dragons, Team2Dragons, Team1Barons, Team2Barons, Team1Towers, "
                   "Team2Towers, Team1Gold, Team2Gold, Team1Kills, Team2Kills, Team1RiftHeralds, "
                   "Team2RiftHeralds, Team1VoidGrubs, Team2VoidGrubs, Team1Atakhans, Team2Atakhans, "
                   "Team1Inhibitors, Team2Inhibitors, VOD, GameId",
            where=f"MatchId = '{match_id}'",
            order_by="DateTime"
        )
        print(json.dumps(response, indent=4))

        # Convert the API response into GameScoreboard objects
        for game_data in response:
            game_id = game_data['GameId']
            self.Games.append(GameScoreboard(game_id))

    def __str__(self):
        return (f"Match ID: {self.match_id}\n"
                f"Team 1: {self.Team1.Name} | Team 2: {self.Team2.Name}\n"
                f"Date: {self.DateTime} | DST: {self.DST}\n"
                f"Final Score - {self.Team1.Name}: {self.Team1Score} | {self.Team2.Name}: {self.Team2Score}")


def get_last_n_matches_of_player(player_name: str, n: int):
    if n > 20:
        n = 20

    last_matches = site.cargo_client.query(
        tables="ScoreboardGames=SG, ScoreboardPlayers=SP",
        join_on="SG.GameId=SP.GameId",
        fields="SP.MatchId, SG.DateTime_UTC, SG.Tournament",
        where=f"SP.Name = '{player_name}'",
        group_by="SP.MatchId",
        order_by="SG.DateTime_UTC DESC",
        limit=n
    )


    for match in last_matches:
        match = get_match_info(match)

        match["Team1Image"] = images_api.get_image_url_with_teamname(match["Team1"])
        match["Team2Image"] = images_api.get_image_url_with_teamname(match["Team2"])

        match["MatchId"] = match["MatchId"].replace("/", " ").replace("_", " ")
    return last_matches


def get_match_info(match: dict):
    response = site.cargo_client.query(
        tables="ScoreboardGames",
        fields="Team1Score, Team2Score, Team1, Team2",
        order_by="DateTime_UTC DESC",
        where=f"MatchId = '{match['MatchId']}'",
        limit=1
    )
    tmp_match = response[-1]
    match["Team1"] = tmp_match["Team1"]
    match["Team2"] = tmp_match["Team2"]
    match["Team1Score"] = tmp_match["Team1Score"]
    match["Team2Score"] = tmp_match["Team2Score"]

    return match


if __name__ == "__main__":
    print(json.dumps(get_last_n_matches_of_player("Faker", 5), indent=2))



