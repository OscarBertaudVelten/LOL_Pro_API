import requests
import json
import uuid  # To generate a unique league_id

# Database connection setup (assuming you have a database connection setup here)
import mysql.connector

# Connection details (replace with your actual database details)
conn = mysql.connector.connect(
    host='localhost', # Update as needed
    user='root', # Update as needed
    password='mysql', # Update as needed
    database='Lol-App' # Database name
)
cursor = conn.cursor()

# URL de l'API pour la requête
base_url = "https://esports-api.lolesports.com/persisted/gw/getSchedule"

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
inserted_ = set()

while True:
    if page_token:
        params["pageToken"] = page_token  # Ajouter le token pour paginer
    else:
        params.pop("pageToken", None)  # Supprimer le token s'il n'est pas défini

    # Envoi de la requête GET
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Erreur {response.status_code} : {response.text}")
        break

    data = response.json()

    # Extraction des événements (matchs)
    events = data.get('data', {}).get('schedule', {}).get('events', [])
    if events:
        for event in events:
            blockName = event.get('blockName', {})
            league = event.get('league', {}).get('name', {})
            season = league + "-" + blockName

            # Check if the league has already been inserted
            if blockName != {} and season not in inserted_:
                # Mark the league as inserted
                inserted_.add(season)
                print(season)

    # Récupérer le token de la page suivante (older)
    pages_info = data.get('data', {}).get('schedule', {}).get('pages', {})
    page_token = pages_info.get('older')  # Utilisation du token "older"

    if not page_token:
        print("Plus de pages à charger.")
        break

# Close the database connection
cursor.close()
conn.close()
