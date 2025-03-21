from mwrogue.esports_client import EsportsClient
import json
from api_tools import get_attribute_value

site = EsportsClient("lol")

# Function to get distinct field values for Leagues
def getLeagueFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Leagues=L",
        fields=f"L.{field}",
        group_by=f"L.{field}"
    )
    return json.dumps(response, indent=2)


class League:
    """
    Represents a League with detailed characteristics.

    Attributes:
        League (str): Name of the league (e.g., 'LoL EMEA Championship').
        League_Short (str): Short name/slug for the league (e.g., 'LEC').
        Region (str): Region where the league is based (e.g., 'Europe').
        Level (str): Division/level of the league (e.g., 'Premier').
        IsOfficial (str): Whether the league is official (e.g., 'Yes' or 'No').
    """

    League: str
    League_Short: str
    Region: str
    Level: str
    IsOfficial: str

    def __init__(self, league_short: str):
        # Fetch league data from the database based on the short name (slug)
        response = site.cargo_client.query(
            tables="Leagues=L",
            fields="L.League,L.League_Short,L.Region,L.Level,L.IsOfficial",
            where=f"L.League_Short = '{league_short}'"
        )

        # Check if we got any data for the league
        if response and len(response) > 0:
            # Get the league data
            league_data = response[0]

            # Populate attributes with data from the query result
            self.League: str = league_data['League']
            self.League_Short: str = league_data['League Short']
            self.Region: str = league_data['Region']
            self.Level: str = league_data['Level']
            self.IsOfficial: str = league_data['IsOfficial']
        else:
            raise ValueError(f"League with short name '{league_short}' not found in the database.")

    def __str__(self):
        # String representation that includes essential details about the league
        return (f"League: {self.League} ({self.League_Short})\n"
                f"Region: {self.Region}\n"
                f"Level: {self.Level}\n"
                f"Official: {self.IsOfficial}")

# Example usage:
# print(League("LEC"))
