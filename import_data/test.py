from mwrogue.esports_client import EsportsClient
import json

site = EsportsClient("lol")

response = site.cargo_client.query(
    tables="Tournaments=T",
    fields="T.Name",
    where="T.Name like '%LEC%'"
)

for tournament in response:
    print(tournament['Name'])

