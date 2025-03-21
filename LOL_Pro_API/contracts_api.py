from mwrogue.esports_client import EsportsClient
import json
from api_tools import get_attribute_value

site = EsportsClient("lol")

# Function to get distinct field values for Contracts
def getContractFieldValues(field: str):
    response = site.cargo_client.query(
        tables="Contracts=C",
        fields=f"C.{field}",
        group_by=f"C.{field}"
    )
    return json.dumps(response, indent=2)


class Contract:
    """
    Represents a Contract with detailed characteristics.

    Attributes:
        Player (str): Name of the player (e.g., 'Yike').
        Team (str): Name of the team (e.g., 'Team A').
        ContractEnd (str): End date of the contract (e.g., '2025-06-30').
        IsRemoval (bool): Whether the contract is a removal (True/False).
        NewsId (str): ID of the news article associated with the contract.
    """

    Player: str
    Team: str
    ContractEnd: str
    IsRemoval: bool
    NewsId: str

    def __init__(self, contract_data: dict):
        # Fetch contract data from the database based on the player's name

        # Populate attributes with data from the query result
        self.Player: str = contract_data['Player']
        self.Team: str = contract_data['Team']
        self.ContractEnd: str = contract_data['ContractEnd']
        self.IsRemoval: bool = bool(contract_data['IsRemoval'])
        self.NewsId: str = contract_data['NewsId']

    def __str__(self):
        # String representation that includes essential details about the contract
        return (f"Player: {self.Player}\n"
                f"Team: {self.Team}\n"
                f"Contract End: {self.ContractEnd}\n"
                f"Is Removal: {self.IsRemoval}\n"
                f"News ID: {self.NewsId}")


class Contracts:
    contracts: [Contract]

    def __init__(self, player_name: str):
        self.contracts = []

        # Fetch contract data from the database based on the player's name
        response = site.cargo_client.query(
            tables="Contracts=C",
            fields="C.Player,C.Team,C.ContractEnd,C.IsRemoval,C.NewsId",
            where=f"C.Player = '{player_name}'",
            order_by=f"C.ContractEnd DESC"
        )

        # Check if we got any data for the player
        if response and len(response) > 0:
            # Get the contract data
            contracts_data = response
            for i in range(len(contracts_data)):
                tmp_contract = Contract(contracts_data[i])
                self.contracts.append(tmp_contract)
        else:
            raise ValueError(f"Player '{player_name}' not found in the database.")

    def __str__(self):
        # Start with the player's name and the number of contracts
        result = f"Player: {self.contracts[0].Player} ({len(self.contracts)} contracts)\n"

        # Iterate over each contract to append its details
        for contract in self.contracts:
            result += (f"  Team: {contract.Team}\n"
                       f"  Contract End: {contract.ContractEnd}\n"
                       f"  Is Removal: {contract.IsRemoval}\n"
                       f"  News ID: {contract.NewsId}\n\n")

        return result



# print(Contracts("Perkz"))

