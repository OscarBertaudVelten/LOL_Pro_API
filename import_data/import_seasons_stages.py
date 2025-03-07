import requests
import json
import uuid  # To generate unique IDs
import mysql.connector

# Database connection setup (replace with your actual connection details)
db_connection = mysql.connector.connect(
    host='4.233.145.40',       # Update as needed
    user='lilscraggy',         # Update as needed
    password='lilscraggy',     # Update as needed
    database='LOL'             # Database name
)
cursor = db_connection.cursor()

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

# Fetch the league data from the database
cursor.execute("SELECT league_id, league_name, league_slug FROM Leagues")
leagues = cursor.fetchall()

# Mapping league_slug -> league_id
league_dict = {league[2]: league[0] for league in leagues}

# Track inserted seasons to avoid duplicates
inserted_seasons = {}

# Pagination
page_token = None

while True:
    if page_token:
        params["pageToken"] = page_token
    else:
        params.pop("pageToken", None)

    # API Request
    print(f"Fetching data with pageToken: {page_token}")
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        break

    data = response.json()
    events = data.get('data', {}).get('schedule', {}).get('events', [])
    

    if events:
        print(f"Processing {len(events)} events")
        for event in events:
            print(json.dumps(event, indent=4))

            league_slug = event.get('league', {}).get('slug')
            season_name = event.get('tournament', {}).get('name', 'unknown')  # Use tournament name for season
            stage_name = event.get('blockName', 'unknown')                   # Use blockName for stage

            league_id = league_dict.get(league_slug)

            if league_id and season_name != 'unknown':
                print(f"Checking season: {season_name} for league: {league_slug}")
                # Check if the season already exists
                if (league_id, season_name) not in inserted_seasons:
                    cursor.execute("""
                        SELECT season_id FROM Seasons
                        WHERE league_id = %s AND season_name = %s
                    """, (league_id, season_name))
                    existing_season = cursor.fetchone()

                    if not existing_season:
                        season_id = str(uuid.uuid4())
                        insert_season_query = """
                            INSERT INTO `LOL`.`Seasons` (`season_id`, `league_id`, `season_name`)
                            VALUES (%s, %s, %s);
                        """
                        cursor.execute(insert_season_query, (season_id, league_id, season_name))
                        db_connection.commit()
                        print(f"Inserted season: {season_name} (League: {league_slug})")
                    else:
                        season_id = existing_season[0]
                        print(f"Season already exists: {season_name} (League: {league_slug})")

                    inserted_seasons[(league_id, season_name)] = season_id
                else:
                    season_id = inserted_seasons[(league_id, season_name)]

                # Insert Stage (Week)
                if stage_name != 'unknown':
                    print(f"Checking stage: {stage_name} for season: {season_name}")
                    cursor.execute("""
                        SELECT stage_id FROM Stages
                        WHERE season_id = %s AND stage_name = %s
                    """, (season_id, stage_name))
                    existing_stage = cursor.fetchone()

                    if not existing_stage:
                        stage_id = str(uuid.uuid4())
                        insert_stage_query = """
                            INSERT INTO `LOL`.`Stages` (`stage_id`, `season_id`, `stage_name`)
                            VALUES (%s, %s, %s);
                        """
                        cursor.execute(insert_stage_query, (stage_id, season_id, stage_name))
                        db_connection.commit()
                        print(f"Inserted stage: {stage_name} (Season: {season_name})")
                    else:
                        print(f"Stage already exists: {stage_name} (Season: {season_name})")

    # Pagination token
    page_token = data.get('data', {}).get('schedule', {}).get('pages', {}).get('older')
    if not page_token:
        print("All pages loaded.")
        break

# Close DB connection
cursor.close()
db_connection.close()
print("Database connection closed.")
