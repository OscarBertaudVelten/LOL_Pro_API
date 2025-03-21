from mwrogue.esports_client import EsportsClient
import json
from api_tools import get_attribute_value

site = EsportsClient("lol")

# Function to get distinct field values for Entities
def getEntityFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Entities=E",
        fields=f"E.{field}",
        group_by=f"E.{field}"
    )
    return json.dumps(response, indent=2)


class Entity:
    """
    Represents an Entity (e.g., a team or organization) with detailed characteristics.

    Attributes:
        Entity (str): Name of the entity (e.g., 'Karmine Corp').
        EntityName (str): Name of the entity (e.g., 'Karmine Corp').
        EntityPage (str): URL to the entity's page on Leaguepedia (e.g., 'Karmine Corp').
        EntityType (str): Type of the entity (e.g., 'Team').
        Display (str): Display Name of the entity (e.g., 'Karmine Corp').
        IsLowercase (bool): Whether the entity name is lowercase (True or False).
        DisambigSentence (str): Sentence to disambiguate the entity (e.g., '[[Karmine Corp|Karmine Corp]] (Team)').
    """

    Entity: str
    EntityName: str
    EntityPage: str
    EntityType: str
    Display: str
    IsLowercase: bool
    DisambigSentence: str

    def __init__(self, entity_name: str, disambiguation: str = ""):
        # Fetch entity data from the database based on the entity name
        response = site.cargo_client.query(
            tables="Entities=E",
            fields="E.Entity,E.EntityName,E.EntityPage,E.EntityType,E.Display,E.IsLowercase,E.DisambigSentence",
            where=f"E.EntityName = '{entity_name}'"
        )

        # Check if we got any data for the entity
        if response:
            if len(response) == 1:
                # Single result - use the result
                entity_data = response[0]
                self._populate_entity_data(entity_data)
            elif len(response) > 1:
                # Multiple results - check if disambiguation is provided
                if not disambiguation:
                    raise ValueError(f"Multiple entities with the name '{entity_name}' found. Please provide a disambiguation sentence.")
                else:
                    # Disambiguate using the provided sentence or use the DisambigSentence from the data
                    self._handle_disambiguation(response, disambiguation)
            else:
                raise ValueError(f"Entity with name '{entity_name}' not found in the database.")
        else:
            raise ValueError(f"Entity with name '{entity_name}' not found in the database.")

    def _populate_entity_data(self, entity_data):
        # Populate attributes with data from the query result
        self.Entity = entity_data['Entity']
        self.EntityName = entity_data['EntityName']
        self.EntityPage = entity_data['EntityPage']
        self.EntityType = entity_data['EntityType']
        self.Display = entity_data['Display']
        self.IsLowercase = bool(entity_data['IsLowercase'])
        self.DisambigSentence = entity_data['DisambigSentence']

    def _handle_disambiguation(self, response, disambiguation):
        # If there are multiple results, we need to find the correct entity to use
        for entity_data in response:
            # If disambiguation matches or is provided, populate it
            if disambiguation == entity_data['DisambigSentence']:
                self._populate_entity_data(entity_data)
                break
        else:
            raise ValueError(f"Disambiguation sentence '{disambiguation}' did not match any entity.")

    def __str__(self):
        # String representation that includes essential details about the entity
        return (f"Entity: {self.Entity}\n"
                f"Entity Name: {self.EntityName}\n"
                f"Entity Page: {self.EntityPage}\n"
                f"Entity Type: {self.EntityType}\n"
                f"Display Name: {self.Display}\n"
                f"Is Lowercase: {self.IsLowercase}\n"
                f"Disambiguation: {self.DisambigSentence}")


# print(Entity("Karmine"))
