from mwrogue.esports_client import EsportsClient
import json


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

        print(json.dumps(response, indent=2))



Champion("Aatrox")