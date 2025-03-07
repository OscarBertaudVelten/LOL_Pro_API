import requests
import json
from datetime import datetime
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',  # Update as needed
    user='root',       # Update as needed
    password='mysql',  # Update as needed
    database='Lol-App' # Database name
)

# Create a cursor object to execute queries
cursor = conn.cursor()

# Get all league slugs from the database
cursor.execute("SELECT league_slug FROM Leagues")
valid_league_slugs = {row[0] for row in cursor.fetchall()}  # Use a set for fast lookups

# Close the database connection
cursor.close()
conn.close()

# URL for API request
base_url = "https://esports-api.lolesports.com/persisted/gw/getSchedule"

# Headers with API key
headers = {
    "Accept": "application/json",
    "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
}

# Initial parameters
params = {
    "hl": "en-US"  # Data language
}

# Pagination
page_token = None

# Dictionary to store match dates for each league
match_dates = {slug: [] for slug in valid_league_slugs}

print("Fetching matches...")

# Loop through every page and match
while True:
    if page_token:
        params["pageToken"] = page_token  # Add token for pagination
    else:
        params.pop("pageToken", None)  # Remove token if not defined

    # Send the GET request
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        break

    data = response.json()

    # Extract the events (matches)
    events = data.get('data', {}).get('schedule', {}).get('events', [])
    if events:
        for event in events:
            league_slug = event.get('league', {}).get('slug')

            # Only process if league_slug is valid (exists in database)
            if league_slug in valid_league_slugs:
                # Extract and parse match date
                match_date = datetime.strptime(event.get("startTime", ""), "%Y-%m-%dT%H:%M:%SZ")

                # Store the date in memory
                match_dates[league_slug].append(match_date)

                print(f"Extracted match for {league_slug} on {match_date.strftime('%d/%m/%y')}")

    # Get the token for the next page (older)
    pages_info = data.get('data', {}).get('schedule', {}).get('pages', {})
    page_token = pages_info.get('older')  # Use "older" token

    if not page_token:
        print("No more pages to load.")
        break

# Sort and write to files
print("\nSorting and writing matches to files...")

for league_slug, dates in match_dates.items():
    if dates:
        print(f"Sorting matches for {league_slug}...")
        sorted_dates = sorted(dates)  # Sort dates in chronological order

        file_path = f"import_data/match_dates/match_dates_{league_slug}.txt"
        with open(file_path, "w") as file:
            for date in sorted_dates:
                formatted_date = date.strftime("%d/%m/%y")
                file.write(formatted_date + "\n")

        print(f"Written {len(sorted_dates)} matches to {file_path}")

print("\nMatch dates for valid leagues have been recorded and sorted.")
