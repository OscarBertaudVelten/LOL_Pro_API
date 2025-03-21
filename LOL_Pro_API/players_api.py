from mwrogue.esports_client import EsportsClient
import json

from LOL_Pro_API import images_api
from LOL_Pro_API.api_tools import get_attribute_value
import html
from LOL_Pro_API.teams_api import Team as TeamClass


site = EsportsClient("lol")


def decode_soloqueue_ids(soloqueue_ids):
    if not soloqueue_ids:  # Vérifie si c'est None ou vide
        return {}

    decoded_string = html.unescape(str(soloqueue_ids))  # Convertit en string pour éviter les erreurs
    parts = decoded_string.split("<br>")
    result = {}

    current_region = None
    for part in parts:
        if ":" in part:
            key, value = part.split(":", 1)
            current_region = key.strip().replace("'", "").strip()
            first_id = value.strip().replace("'", "").strip()
            result[current_region] = [first_id]
        elif current_region:
            new_id = part.strip().replace("'", "").strip()
            result[current_region].append(new_id)

    return result



# Parses the FavChamps string into a list of favorite champions.
def parse_fav_champs(fav_champs: str):
    if not fav_champs:
        return []

    # Split by commas and strip whitespace from each champion name
    return [champ.strip() for champ in fav_champs.split(",")]


# Function to get distinct field values for Players
def getPlayerFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Players=P",
        fields=f"P.{field}",
        group_by=f"P.{field}"
    )
    return json.dumps(response, indent=2)


class Player:
    """
    Représente un joueur professionnel de League of Legends avec ses caractéristiques détaillées.

    Attributs:
        ID (str): Identifiant unique du joueur (ex: 'Yike').
        OverviewPage (str): URL de la page de présentation du joueur sur Leaguepedia.
        Player (str): Pseudonyme du joueur en jeu.
        Name (str): Prénom ou surnom du joueur.
        NameFull (str): Nom complet du joueur (ex: 'Martin Sundelin').
        Country (str): Pays de naissance du joueur (ex: 'Sweden').
        Nationality (str): Nationalité du joueur sous forme de liste (ex: 'Sweden,Peru').
        NationalityPrimary (str): Nationalité principale du joueur.
        Age (int): Âge du joueur.
        Birthdate (str): Date de naissance du joueur (format: 'YYYY-MM-DD').
        Deathdate (str): Date de décès du joueur, si applicable.
        Residency (str): Région de résidence du joueur (ex: 'EMEA').
        ResidencyFormer (str): Ancienne région de résidence du joueur.
        Team (Team): Instance de l'équipe actuelle du joueur.
        Role (str): Rôle du joueur en jeu (ex: 'Jungle').
        RoleLast (str): Dernier rôle occupé par le joueur.
        Contract (str): Date de fin de contrat du joueur (format: 'YYYY-MM-DD').
        FavChamps (list): Liste des champions favoris du joueur.
        SoloqueueIds (dict): Dictionnaire des identifiants de soloqueue du joueur par région (ex: {"EUW": "KC Yiken", "KR": "YIK"}).
        IsRetired (bool): Indique si le joueur est à la retraite.
        IsSubstitute (bool): Indique si le joueur est remplaçant.
        IsLowercase (bool): Indique si le pseudonyme du joueur est entièrement en minuscules.
        IsAutoTeam (bool): Indique si l'équipe est générée automatiquement.
        IsLowContent (bool): Indique si le joueur a peu de contenu disponible.
        Socials (dict): Dictionnaire contenant les liens vers les réseaux sociaux du joueur.
        Image (str): URL de l'Image du joueur.

    Méthodes:
        __init__(player_name: str): Initialise une instance de joueur en récupérant ses données depuis la base de données.
        __str__(): Retourne une représentation sous forme de chaîne du joueur avec ses informations essentielles.
    """

    ID: str
    OverviewPage: str
    Player: str
    Name: str
    NameFull: str
    Country: str
    Nationality: str
    NationalityPrimary: str
    Age: int
    Birthdate: str
    Deathdate: str
    ResidencyFormer: str
    Team: TeamClass
    Residency: str
    Role: str
    Contract: str
    FavChamps: list
    SoloqueueIds: dict
    RoleLast: str
    IsRetired: bool
    IsSubstitute: bool
    IsLowercase: bool
    IsAutoTeam: bool
    IsLowContent: bool
    Socials: dict
    Image: str

    def __init__(self, player_name: str):
        # Fetch player data from the database based on the player's in-game name
        response = site.cargo_client.query(
            tables="Players=P",
            fields="P.ID,P.OverviewPage,P.Player,P.Name,P.NameFull,P.Country,P.Nationality,P.NationalityPrimary,P.Age,P.Birthdate,P.Deathdate,P.ResidencyFormer,P.Team,P.Residency,P.Role,P.Contract,P.FavChamps,P.SoloqueueIds,P.Askfm,P.Bluesky,P.Discord,P.Facebook,P.Instagram,P.Lolpros,P.Reddit,P.Snapchat,P.Stream,P.Twitter,P.Threads,P.LinkedIn,P.Vk,P.Website,P.Weibo,P.Youtube,P.RoleLast,P.IsRetired,P.IsSubstitute,P.IsLowercase,P.IsAutoTeam,P.IsLowContent",
            where=f"P.Player = '{player_name}'"
        )

        # Check if we got any data for the player
        if response and len(response) > 0:
            # Get the player data
            player_data = response[0]



            # Gestion des types spécifiques
            self.Age = int(player_data.get('Age', 0) or 0)
            self.IsRetired = bool(player_data.get('IsRetired', False))
            self.IsSubstitute = bool(player_data.get('IsSubstitute', False))
            self.IsLowercase = bool(player_data.get('IsLowercase', False))
            self.IsAutoTeam = bool(player_data.get('IsAutoTeam', False))
            self.IsLowContent = bool(player_data.get('IsLowContent', False))
            self.Image = str(images_api.get_player_image_url(player_name))

            # Initialisation de l'équipe avec gestion d'erreur
            team_name = player_data.get('Team', "")
            try:
                self.Team = TeamClass(team_name) if team_name else None
            except Exception as e:
                print(f"Warning: Failed to initialize Team for player '{self.Player}'. Error: {e}")
                self.Team = "None"  # Assign None if an error occurs

            self.SoloqueueIds = decode_soloqueue_ids(player_data.get('SoloqueueIds', ""))
            self.FavChamps = parse_fav_champs(player_data.get('FavChamps', ""))

            # Récupération des réseaux sociaux non vides
            social_fields = ['Askfm', 'Bluesky', 'Discord', 'Facebook', 'Instagram', 'Lolpros',
                             'Reddit', 'Snapchat', 'Stream', 'Twitter', 'Threads', 'LinkedIn',
                             'Vk', 'Website', 'Weibo', 'Youtube']
            self.Socials = {key: player_data[key] for key in social_fields if player_data.get(key)}

        else:
            raise ValueError(f"Player with name '{player_name}' not found in the database.")


    def __str__(self):
        # String representation that includes essential details about the player
        return (f"Player: {self.Player} ({self.NameFull})\n"
                f"Country: {self.Country}\n"
                f"Nationality: {self.Nationality}\n"
                f"Age: {self.Age}\n"
                f"Birthdate: {self.Birthdate}\n"
                f"Team: {self.Team}\n"
                f"Residency: {self.Residency}\n"
                f"Role: {self.Role}\n"
                f"Contract: {self.Contract}\n"
                f"Favorite Champions: {self.FavChamps}\n"
                f"Soloqueue IDs: {self.SoloqueueIds}\n"
                f"Social Media: {json.dumps(self.Socials, indent=2)}\n"
                f"Image: {self.Image}")
    

    def to_dict(self):
        return {
            "ID": self.ID,
            "OverviewPage": self.OverviewPage,
            "Player": self.Player,
            "Name": self.Name,
            "NameFull": self.NameFull,
            "Country": self.Country,
            "Nationality": self.Nationality,
            "NationalityPrimary": self.NationalityPrimary,
            "Age": self.Age,
            "Birthdate": self.Birthdate,
            "Deathdate": self.Deathdate,
            "ResidencyFormer": self.ResidencyFormer,
            "Team": self.Team.to_dict() if self.Team else None,
            "Residency": self.Residency,
            "Role": self.Role,
            "Contract": self.Contract,
            "FavChamps": self.FavChamps,
            "SoloqueueIds": self.SoloqueueIds,
            "RoleLast": self.RoleLast,
            "IsRetired": self.IsRetired,
            "IsSubstitute": self.IsSubstitute,
            "IsLowercase": self.IsLowercase,
            "IsAutoTeam": self.IsAutoTeam,
            "IsLowContent": self.IsLowContent,
            "Socials": self.Socials,
            "Image": self.Image,
        }


# Example usage:
print(Player("Yike"))