from mwrogue.esports_client import EsportsClient
import json
from LOL_Pro_API.api_tools import get_attribute_value
from LOL_Pro_API import images_api

site = EsportsClient("lol")

# Function to get distinct field values for Teams
def getTeamFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Teams=T",
        fields=f"T.{field}",
        group_by=f"T.{field}"
    )
    return json.dumps(response, indent=2)


class Team:
    """
    Represents a Team with detailed characteristics.

    Attributes:
        Name (str): Full name of the team.
        Short (str): Short name or acronym for the team.
        OverviewPage (str): URL to the team's overview page.
        Location (str): Country or region of the team.
        TeamLocation (str): Specific location of the team.
        Region (str): Competitive region the team belongs to.
        OrganizationPage (str): URL to the team's organization page.
        IsDisbanded (bool): Whether the team is disbanded.
        RenamedTo (str): New name of the team if renamed.
        IsLowercase (bool): Whether the team name is lowercase.

        Image (str): URL of the team logo.
        RosterPhoto (str): URL of the team roster photo.

        Socials (dict): Dictionary containing the teams's social media handles.
    """

    Name: str
    Short: str
    OverviewPage: str
    Location: str
    TeamLocation: str
    Region: str
    OrganizationPage: str
    IsDisbanded: bool
    RenamedTo: str
    IsLowercase: bool

    RosterPhoto: str
    Image: str

    Socials: dict

    def __init__(self, team_name: str):
        # Fetch team data from the database based on the short name
        response = site.cargo_client.query(
            tables="Teams=T",
            fields=(
                "T.Name, T.Short, T.OverviewPage, T.Location, T.TeamLocation, T.Region, T.OrganizationPage, "
                "T.Twitter, T.Youtube, T.Facebook, T.Instagram, T.Bluesky, T.Discord, T.Snapchat, "
                "T.Vk, T.Subreddit, T.Website, T.RosterPhoto, T.IsDisbanded, T.RenamedTo, T.IsLowercase, T.Image"
            ),
            where=f"T.Name = '{team_name}'"
        )

        # Check if we got any data for the team
        if response and len(response) > 0:
            # Get the team data
            team_data = response[0]

            default_values = {
                'Name': '',
                'Short': '',
                'OverviewPage': '',
                'Location': '',
                'TeamLocation': '',
                'Region': '',
                'OrganizationPage': '',
                'IsDisbanded': False,
                'RenamedTo': '',
                'IsLowercase': False
            }

            for key, default_value in default_values.items():
                setattr(self, key, get_attribute_value(team_data, key, default_value))

            self.Image = images_api.get_image_url(team_data['Image'])
            self.RosterPhoto = images_api.get_image_url(team_data['RosterPhoto'])

            social_fields = ['Twitter', 'Youtube', 'Facebook', 'Instagram',
                             'Bluesky', 'Discord', 'Snapchat', 'Vk', 'Subreddit', 'Website']
            self.Socials = {key: team_data[key] for key in social_fields if team_data.get(key)}

        else:
            raise ValueError(f"Team with team name '{team_name}' not found in the database.")

    def __str__(self):
        # String representation that includes details about the team
        return (
            f"Team Name: {self.Name}\n"
            f"Short Name: {self.Short}\n"
            f"Overview Page: {self.OverviewPage}\n"
            f"Location: {self.Location}\n"
            f"Team Location: {self.TeamLocation}\n"
            f"Region: {self.Region}\n"
            f"Organization Page: {self.OrganizationPage}\n"
            f"Roster Photo: {self.RosterPhoto}\n"
            f"Is Disbanded: {self.IsDisbanded}\n"
            f"Renamed To: {self.RenamedTo}\n"
            f"Is Lowercase: {self.IsLowercase}\n"
            f"Socials: {json.dumps(self.Socials, indent=2)}\n"
            f"Image: {self.Image}"
        )


    def to_dict(self):
        return {
            "Name": self.Name,
            "Short": self.Short,
            "OverviewPage": self.OverviewPage,
            "Location": self.Location,
            "TeamLocation": self.TeamLocation,
            "Region": self.Region,
            "OrganizationPage": self.OrganizationPage,
            "IsDisbanded": self.IsDisbanded,
            "RenamedTo": self.RenamedTo,
            "IsLowercase": self.IsLowercase,
            "RosterPhoto": self.RosterPhoto,
            "Image": self.Image,
            "Socials": self.Socials
        }


