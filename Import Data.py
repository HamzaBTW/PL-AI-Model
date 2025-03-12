import pandas as pd
import time
import os
from tqdm import tqdm  # For progress bar

# Define the data directory path
DATA_DIR = r"C:\Users\hamza\Coding\projects\Sport AI Analysis\Data"

# Create the directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

clubs = {
    'Liverpool': '822bd0ba',
    'Manchester City': 'b8fd03ef',
    'Arsenal': '18bb7c10',
    'Tottenham': '361ca564',
    'Chelsea': 'cff3d9bb',
    'Manchester United': '19538871',
    'Aston Villa': '8602292d',
    'Newcastle': 'b2b47a98',
    'Brighton': 'd07537b9',
    'West Ham': '7c21e445',
}

# Dictionary to store data frames for each club
all_data = {}

# Loop through each club
for club_name, club_id in tqdm(clubs.items()):
    url = f"https://fbref.com/en/squads/{club_id}/{club_name.replace(' ', '-')}-Stats"
    
    try:
        # Fetch tables from the club page
        tables = pd.read_html(url)
        print(f"Found {len(tables)} tables for {club_name}")
        
        # Store tables in dictionary
        all_data[club_name] = tables
        
        # Save first table (fixtures) as example
        # Adjust the index as needed to get different tables
        file_path = os.path.join(DATA_DIR, f"{club_name.lower().replace(' ', '_')}_fixtures.csv")
        tables[1].to_csv(file_path, index=False)
        print(f"Saved fixtures for {club_name} to {file_path}")
        
        # Pause to avoid overwhelming the server
        time.sleep(2)
        
    except Exception as e:
        print(f"Error fetching data for {club_name}: {e}")

# Example: Access specific table for specific club
# For example, to access the first table for Liverpool:
# liverpool_table_1 = all_data['Liverpool'][1]

# Optional: Combine similar tables from different clubs
# For example, to combine all fixture tables (assuming they're at index 1)
combined_fixtures = pd.DataFrame()

for club_name, tables in all_data.items():
    if len(tables) > 1:  # Make sure table exists
        # Add a column to identify the club
        fixtures = tables[1].copy()
        fixtures['Club'] = club_name
        combined_fixtures = pd.concat([combined_fixtures, fixtures])

# Save combined data
combined_file_path = os.path.join(DATA_DIR, "all_clubs_fixtures.csv")
combined_fixtures.to_csv(combined_file_path, index=False)
print(f"Combined fixtures saved to {combined_file_path}")

print("Data collection complete!")