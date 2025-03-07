import requests
import json
import mysql.connector  # MySQL connector

# Database connection
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
    "hl": "en-US"
}

# Track unique teams
unique_teams = {}
team_id_counter = 1  # Start from 1

# Pagination
page_token = None

while True:
    if page_token:
        params["pageToken"] = page_token
    else:
        params.pop("pageToken", None)

    # Envoi de la requête GET
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Erreur {response.status_code} : {response.text}")
        break

    data = response.json()

    # Extraction des événements (matchs)
    events = data.get('data', {}).get('schedule', {}).get('events', [])
    for event in events:
        teams = event.get('match', {}).get('teams', [])
        for team in teams:
            team_name = team.get('name')
            team_code = team.get('code')
            team_image = team.get('image')

            # Check for uniqueness by team_code
            if team_code not in unique_teams:
                team_id = team_id_counter
                unique_teams[team_code] = True
                team_id_counter += 1

                # Insert into database
                insert_query = """
                INSERT INTO `Teams` (`team_id`, `team_name`, `team_code`, `team_image`)
                VALUES (%s, %s, %s, %s)
                """
                values = (team_id, team_name, team_code, team_image)

                try:
                    cursor.execute(insert_query, values)
                    conn.commit()
                    print(f"Inserted team: {team_name} ({team_code})")
                except mysql.connector.Error as err:
                    print(f"Database error: {err}")

    # Pagination token
    pages_info = data.get('data', {}).get('schedule', {}).get('pages', {})
    page_token = pages_info.get('older')

    if not page_token:
        print("No more pages to load.")
        break

# Close DB connection
cursor.close()
conn.close()
