import requests

# URL de l'API pour la requête
base_url = "https://esports-api.lolesports.com/persisted/gw/getNews"

# Headers avec la clé API
headers = {
    "Accept": "application/json",
    "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
}

# Paramètres initiaux
params = {
    "hl": "en-US"  # Langue des données
}

# Pagination
page_token = None

# Set to track inserted leagues
inserted_leagues = set()
league_id_counter = 1  # Start from 1

while True:
    if page_token:
        params["pageToken"] = page_token  # Ajouter le token pour paginer
    else:
        params.pop("pageToken", None)  # Supprimer le token s'il n'est pas défini

    # Envoi de la requête GET
    response = requests.get(base_url, headers=headers, params="opt")

    if response.status_code != 200:
        print(f"Erreur {response.status_code} : {response.text}")
        break

    data = response.json()
    print(data)
