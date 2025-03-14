from mwrogue.esports_client import EsportsClient
import json

site = EsportsClient("lol")

def getCargoFields():
    response = site.cargo_client.query(
        tables="CargoFields=CF",
        fields="CF.Name, CF.CargoTable"
    )

    return "\n".join(f"{entry['Name']}, {entry['CargoTable']}" for entry in response)

# print(getCargoFields())