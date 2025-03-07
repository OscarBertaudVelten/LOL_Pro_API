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
inserted_leagues = set()
league_id_counter = 1  # Start from 1

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
            # Extract the league info
            league_id = league_id_counter
            league_id_counter += 1
            league_name = event.get('league', {}).get('name')
            league_slug = event.get('league', {}).get('slug')

            # Check if the league has already been inserted
            if (league_name, league_slug) not in inserted_leagues:

                # Insert the league into the database
                insert_query = """
                    INSERT INTO `Leagues` (`league_id`, `league_name`, `league_slug`)
                    VALUES (%s, %s, %s);
                """
                cursor.execute(insert_query, (league_id, league_name, league_slug))
                conn.commit()

                # Mark the league as inserted
                inserted_leagues.add((league_name, league_slug))
                print(f"Inserted league: {league_name}, {league_slug}")

    # Récupérer le token de la page suivante (older)
    pages_info = data.get('data', {}).get('schedule', {}).get('pages', {})
    page_token = pages_info.get('older')  # Utilisation du token "older"

    if not page_token:
        print("Plus de pages à charger.")
        break

# Close the database connection
cursor.close()
conn.close()
