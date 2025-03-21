from mwrogue.esports_client import EsportsClient
import json
from api_tools import get_attribute_value
from datetime import datetime, timedelta

site = EsportsClient("lol")

# Function to get distinct field values for Tournaments
def getTournamentFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Tournaments=T",
        fields=f"T.{field}",
        group_by=f"T.{field}",
        where="T.Region='Europe'"
    )
    return json.dumps(response, indent=2)


class Tournament:
    """
    Represents a Tournament with detailed characteristics.

    Attributes:
        Name (str): Name of the tournament (e.g., 'LEC 2019 Spring Playoffs').
        OverviewPage (str): URL to the tournament's overview page on Leaguepedia (e.g., 'LEC/2019 Season/Spring Playoffs').
        DateStart (str): Start date of the tournament (e.g., '2019-03-29').
        Date (str): End date of the tournament (e.g., '2019-04-14').
        League (str): League name associated with the tournament (e.g., 'LoL EMEA Championship').
        Region (str): Region where the tournament is held (e.g., 'Europe').
        Prizepool (str): Prizepool for the tournament (e.g., '\u20ac 200,000').
        Country (str): Country where the tournament is held (e.g., 'None').
        ClosestTimezone (str): Closest timezone to the event (e.g., 'CET').
        Rulebook (str): URL to the tournament's rulebook (e.g., 'https://...').
        EventType (str): Type of the event (e.g., 'Online', 'LAN').
        Split (str): Split of the tournament (e.g., 'Spring').
        TournamentLevel (str): Level of the tournament (e.g., 'Primary').
        IsQualifier (bool): Whether the tournament is a qualifier (True/False).
        IsPlayoffs (bool): Whether the tournament is playoffs (True/False).
        IsOfficial (bool): Whether the tournament is official (True/False).
        Year (str): Year of the tournament (e.g., '2019').
        LeagueIconKey (str): Icon key for the associated league (e.g., 'LEC').
        IsOngoing (bool): Whether the tournament is currently ongoing (True/False).
    """

    Name: str
    OverviewPage: str
    DateStart: str
    Date: str
    DateStartFuzzy: str
    League: str
    Region: str
    Prizepool: str
    Country: str
    ClosestTimezone: str
    Rulebook: str
    EventType: str
    Split: str
    TournamentLevel: str
    IsQualifier: bool
    IsPlayoffs: bool
    IsOfficial: bool
    Year: str
    LeagueIconKey: str
    IsOngoing: bool

    def __init__(self, tournament_name: str):
        # Fetch tournament data from the database based on the tournament name
        response = site.cargo_client.query(
            tables="Tournaments=T",
            fields="T.Name,T.OverviewPage,T.DateStart,T.Date,T.DateStartFuzzy,T.League,T.Region,T.Prizepool,T.Currency,T.Country,T.ClosestTimezone,T.Rulebook,T.EventType,T.Split,T.TournamentLevel,T.IsQualifier,T.IsPlayoffs,T.IsOfficial,T.Year,T.LeagueIconKey",
            where=f"T.Name = '{tournament_name}'"
        )

        # Check if we got any data for the tournament
        if response and len(response) > 0:
            # Get the tournament data
            tournament_data = response[0]

            # Populate attributes with data from the query result
            self.Name: str = tournament_data['Name']
            self.OverviewPage: str = tournament_data['OverviewPage']
            self.DateStart: str = tournament_data['DateStart']
            self.Date: str = tournament_data['Date']
            self.DateStartFuzzy: str = tournament_data['DateStartFuzzy']
            self.League: str = tournament_data['League']
            self.Region: str = tournament_data['Region']
            self.Prizepool: str = tournament_data['Prizepool']
            self.Country: str = tournament_data['Country']
            self.ClosestTimezone: str = tournament_data['ClosestTimezone']
            self.Rulebook: str = tournament_data['Rulebook']
            self.EventType: str = tournament_data['EventType']
            self.Split: str = tournament_data['Split']
            self.TournamentLevel: str = tournament_data['TournamentLevel']
            self.IsQualifier: bool = bool(tournament_data['IsQualifier'])
            self.IsPlayoffs: bool = bool(tournament_data['IsPlayoffs'])
            self.IsOfficial: bool = bool(tournament_data['IsOfficial'])
            self.Year: str = tournament_data['Year']
            self.LeagueIconKey: str = tournament_data['LeagueIconKey']
            self.IsOngoing = self.is_ongoing()

        else:
            raise ValueError(f"Tournament with name '{tournament_name}' not found in the database.")


    def is_ongoing(self) -> bool:
        """
        Determines if the tournament is currently live by comparing the current date with
        the tournament's start and end dates.
        """
        current_date = datetime.now().date()

        # Parse the start and end dates from string to date objects
        start_date = datetime.strptime(self.DateStart, '%Y-%m-%d').date()
        end_date = datetime.strptime(self.Date, '%Y-%m-%d').date()

        # Check if current date is within the tournament start and end date range
        return start_date <= current_date <= end_date



    def __str__(self):
        # String representation that includes essential details about the tournament
        return (f"Tournament: {self.Name}\n"
                f"Overview Page: https://lol.fandom.com/wiki/{self.OverviewPage.replace(' ', '_')}\n"
                f"Start Date: {self.DateStart}\n"
                f"End Date: {self.Date}\n"
                f"League: {self.League}\n"
                f"Region: {self.Region}\n"
                f"Prizepool: {self.Prizepool}\n"
                f"Timezone: {self.ClosestTimezone}\n"
                f"Event Type: {self.EventType}\n"
                f"Split: {self.Split}\n"
                f"Level: {self.TournamentLevel}\n"
                f"Qualifier: {self.IsQualifier}\n"
                f"Playoffs: {self.IsPlayoffs}\n"
                f"Official: {self.IsOfficial}\n"
                f"Year: {self.Year}\n"
                f"Icon Key: {self.LeagueIconKey}")


def get_primary_recent_tournaments():
    six_months_ago = (datetime.today() - timedelta(days=180)).strftime("%Y-%m-%d")

    response = site.cargo_client.query(
        tables="Tournaments=T",
        fields="T.Name",
        where=f"T.TournamentLevel='Primary' AND T.Date >= '{six_months_ago}'"
    )
    return ", ".join(f"'{entry['Name']}'" for entry in response)


# print(get_primary_recent_tournaments())
# Example usage:
# print(Tournament("Asia Masters 2025 Swiss 1"))

