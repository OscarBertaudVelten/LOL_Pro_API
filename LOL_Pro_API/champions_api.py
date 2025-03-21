from mwrogue.esports_client import EsportsClient
import json
from api_tools import get_attribute_value

site = EsportsClient("lol")

# Function to get distinct field values for Champions
def getChampionFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Champions=C",
        fields=f"C.{field}",
        group_by=f"C.{field}"
    )
    return json.dumps(response, indent=2)


class Champion:
    """
    Represents a League of Legends champion with detailed characteristics.

    Attributes:
        Name (str): Name of the champion (e.g., 'Aatrox').
        Title (str): Title of the champion (e.g., 'The Darkin Blade').
        ReleaseDate (str): Release date of the champion (format 'YYYY-MM-DD').
        BE (int): Cost in Blue Essence (e.g., 4800).
        RP (int): Cost in RP (e.g., 880).
        Attributes (str): Roles of the champion separated by commas (e.g., 'Fighter,Tank').
        Resource (str): Type of resource used (e.g., 'Blood Well').
        RealName (str): Real name of the champion (e.g., 'null' if not applicable).
        Health (float): Base health points.
        HPLevel (float): Health points gained per level.
        HPDisplay (str): Display of health points (wiki format).
        HPLevelDisplay (str): Display of health points per level (wiki format).
        HPRegen (float): Base health regeneration.
        HPRegenLevel (float): Health regeneration gained per level.
        Mana (float): Base mana (null if not applicable).
        ManaLevel (float): Mana gained per level (null if not applicable).
        ManaRegen (float): Base mana regeneration (null if not applicable).
        ManaRegenLevel (float): Mana regeneration gained per level (null if not applicable).
        Energy (float): Base energy (null if not applicable).
        EnergyRegen (float): Base energy regeneration (null if not applicable).
        Movespeed (float): Movement speed.
        AttackDamage (float): Base attack damage.
        ADLevel (float): Attack damage gained per level.
        AttackSpeed (float): Base attack speed.
        ASLevel (float): Attack speed gained per level.
        AttackRange (float): Base attack range.
        Armor (float): Base armor.
        ArmorLevel (float): Armor gained per level.
        MagicResist (float): Base magic resistance.
        MagicResistLevel (float): Magic resistance gained per level.
        Pronoun (str): Pronoun associated with the champion (e.g., 'He/Him', 'She/Her', 'They/Them').
        KeyInteger (int): Unique identifier of the champion in Riot's data.
    """

    Name: str
    Title: str
    ReleaseDate: str
    BE: int
    RP: int
    Attributes: str
    Resource: str
    RealName: str
    Health: float
    HPLevel: float
    HPDisplay: str
    HPLevelDisplay: str
    HPRegen: float
    HPRegenLevel: float
    Mana: float
    ManaLevel: float
    ManaRegen: float
    ManaRegenLevel: float
    Energy: float
    EnergyRegen: float
    Movespeed: float
    AttackDamage: float
    ADLevel: float
    AttackSpeed: float
    ASLevel: float
    AttackRange: float
    Armor: float
    ArmorLevel: float
    MagicResist: float
    MagicResistLevel: float
    Pronoun: str
    KeyInteger: int

    def __init__(self, champion_name: str):
        # Fetch champion data from the database based on the name
        response = site.cargo_client.query(
            tables="Champions=C",
            fields="C.Name,C.Title,C.ReleaseDate,C.BE,C.RP,C.Attributes,C.Resource,C.RealName,C.Health,C.HPLevel,C.HPDisplay,C.HPLevelDisplay,C.HPRegen,C.HPRegenLevel,C.Mana,C.ManaLevel,C.ManaRegen,C.ManaRegenLevel,C.Energy,C.EnergyRegen,C.Movespeed,C.AttackDamage,C.ADLevel,C.AttackSpeed,C.ASLevel,C.AttackRange,C.Armor,C.ArmorLevel,C.MagicResist,C.MagicResistLevel,C.Pronoun,C.KeyInteger",
            where=f"C.Name = '{champion_name}'"
        )

        # Check if we got any data for the champion
        if response and len(response) > 0:
            # Get the champion data
            champ_data = response[0]

            # Populate attributes with data from the query result
            self.Name = champ_data['Name']
            self.Title = champ_data['Title']
            self.ReleaseDate = champ_data['ReleaseDate']
            self.BE = champ_data['BE']
            self.RP = champ_data['RP']
            self.Attributes = champ_data['Attributes']
            self.Resource = champ_data['Resource']
            self.RealName = champ_data['RealName'] if champ_data['RealName'] != 'null' else None
            self.Health = champ_data['Health']
            self.HPLevel = champ_data['HPLevel']
            self.HPDisplay = champ_data['HPDisplay']
            self.HPLevelDisplay = champ_data['HPLevelDisplay']
            self.HPRegen = champ_data['HPRegen']
            self.HPRegenLevel = champ_data['HPRegenLevel']
            self.Mana = champ_data['Mana'] if champ_data['Mana'] != 'null' else None
            self.ManaLevel = champ_data['ManaLevel'] if champ_data['ManaLevel'] != 'null' else None
            self.ManaRegen = champ_data['ManaRegen'] if champ_data['ManaRegen'] != 'null' else None
            self.ManaRegenLevel = champ_data['ManaRegenLevel'] if champ_data['ManaRegenLevel'] != 'null' else None
            self.Energy = champ_data['Energy'] if champ_data['Energy'] != 'null' else None
            self.EnergyRegen = champ_data['EnergyRegen'] if champ_data['EnergyRegen'] != 'null' else None
            self.Movespeed = champ_data['Movespeed']
            self.AttackDamage = champ_data['AttackDamage']
            self.ADLevel = champ_data['ADLevel']
            self.AttackSpeed = champ_data['AttackSpeed']
            self.ASLevel = champ_data['ASLevel']
            self.AttackRange = champ_data['AttackRange']
            self.Armor = champ_data['Armor']
            self.ArmorLevel = champ_data['ArmorLevel']
            self.MagicResist = champ_data['MagicResist']
            self.MagicResistLevel = champ_data['MagicResistLevel']
            self.Pronoun = champ_data['Pronoun']
            self.KeyInteger = champ_data['KeyInteger']
        else:
            raise ValueError(f"Champion '{champion_name}' not found in the database.")


    def __str__(self):
        # String representation that includes essential details about the champion
        return (f"Champion: {self.Name}\n"
                f"Title: {self.Title}\n"
                f"Release Date: {self.ReleaseDate}\n"
                f"Cost: {self.BE} BE / {self.RP} RP\n"
                f"Attributes: {self.Attributes}\n"
                f"Resource: {self.Resource}\n"
                f"Real Name: {self.RealName}\n"
                f"Health: {self.Health} (Level: {self.HPLevel})\n"
                f"HP Regen: {self.HPRegen} (Level: {self.HPRegenLevel})\n"
                f"Mana: {self.Mana} (Level: {self.ManaLevel})\n"
                f"Mana Regen: {self.ManaRegen} (Level: {self.ManaRegenLevel})\n"
                f"Energy: {self.Energy}\n"
                f"Energy Regen: {self.EnergyRegen}\n"
                f"Movespeed: {self.Movespeed}\n"
                f"Attack Damage: {self.AttackDamage} (Level: {self.ADLevel})\n"
                f"Attack Speed: {self.AttackSpeed} (Level: {self.ASLevel})\n"
                f"Attack Range: {self.AttackRange}\n"
                f"Armor: {self.Armor} (Level: {self.ArmorLevel})\n"
                f"Magic Resist: {self.MagicResist} (Level: {self.MagicResistLevel})\n"
                f"Pronoun: {self.Pronoun}\n"
                f"Key Integer: {self.KeyInteger}")

# Example usage:
# print(Champion("Aatrox"))
