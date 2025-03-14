import mysql.connector
import json
from datetime import datetime
import re

# Establish a connection to the database
conn = mysql.connector.connect(
    host='localhost',        # e.g., 'localhost' or your database host
    user='root',             # e.g., 'root'
    password='mysql',       # your database password
    database='lol-app'      # your database name
)

cursor = conn.cursor()

# Fetch the league_id for each league
def get_league_id(league_name):
    query = f"SELECT league_id FROM leagues WHERE league_slug = %s"
    cursor.execute(query, (league_name,))
    result = cursor.fetchone()
    return result[0] if result else None


def insert_split_data(league_name, split_name, start_date, end_date):
    league_id = get_league_id(league_name)
    print(start_date)
    # Handle cases for unknown dates, leave them as None (NULL in DB) or use a special date like "0000-01-01"
    if end_date != None and "??" in end_date:
        end_date = None  # Use None to insert NULL into the database

    if start_date == None:
        year = 0

    elif "??" in start_date:
        year = re.match(r"(\d{4})", start_date)
        year = year.group(1) if year else None
        start_date = None  # Set start_date to None to signify unknown date

    elif start_date:  # Check if the start_date is valid
        try:
            datetime.strptime(start_date, "%Y-%m-%d")  # Ensure the date is valid
            year = datetime.strptime(start_date, "%Y-%m-%d").year
        except ValueError:
            start_date = None  # Invalid date format, set to None

    # If league_id exists, insert data
    if league_id:
        query = """
            INSERT INTO splits (league_id, block_name, split_name, start_date, end_date, year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        block_name = league_name  # Use the league name as the block name
        cursor.execute(query, (league_id, block_name, split_name, start_date, end_date, year))
        conn.commit()  # Commit the transaction


# Load the JSON data (assuming openrouter_results.json is in the same directory as this script)
with open('import_data/openrouter_results.json', 'r') as file:
    data = json.load(file)

# Iterate through each league in the data
for league_name, splits in data.items():
    print("-------------" + league_name + "-------------")
    for split in splits:
        print(split)
        # Handle possible missing dates (null values in the JSON)
        start_date = split.get("startDate", None)
        end_date = split.get("endDate", None)
        split_name = split.get("splitName", None)

        # Only insert if splitName is available
        if split_name:
            insert_split_data(league_name, split_name, start_date, end_date)

# Close the connection
cursor.close()
conn.close()

print("Data inserted successfully.")
