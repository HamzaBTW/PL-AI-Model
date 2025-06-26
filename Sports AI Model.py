import requests
import pandas as pd
import os
import pickle
import random
from commentary_templates import get_commentary_template

API_TOKEN = '050be06c781542fea99c07add0f6724e'
headers = {'X-Auth-Token': API_TOKEN}

matches = []
for season in [2023, 2024]:
    url = f'https://api.football-data.org/v4/competitions/PL/matches?season={season}'
    response = requests.get(url, headers=headers)
    data = response.json()
    for match in data.get('matches', []):
        if match.get('status') == 'FINISHED':
            matches.append({
                'date': match.get('utcDate'),
                'homeTeam': match.get('homeTeam', {}).get('name'),
                'awayTeam': match.get('awayTeam', {}).get('name'),
                'score_home': match.get('score', {}).get('fullTime', {}).get('home'),
                'score_away': match.get('score', {}).get('fullTime', {}).get('away'),
                'status': match.get('status'),
                'matchday': match.get('matchday'),
                'season': season
            })

os.makedirs('Data', exist_ok=True)
df = pd.DataFrame(matches)
df.to_csv('Data/all_clubs_fixtures.csv', index=False)
print(df)

# --- Prediction Section ---

# Load model and encoders
MODELS_DIR = os.path.join('Data', 'models')
with open(os.path.join(MODELS_DIR, 'match_prediction_model.pkl'), 'rb') as f:
    model = pickle.load(f)
with open(os.path.join(MODELS_DIR, 'encoders_and_scaler.pkl'), 'rb') as f:
    encoders = pickle.load(f)

label_encoder_venue = encoders['venue_encoder']
label_encoder_opponent = encoders['opponent_encoder']
label_encoder_club = encoders['club_encoder']
scaler = encoders['scaler']

def predict_match_outcome(venue, opponent, club, label_encoder_venue, label_encoder_opponent, label_encoder_club, scaler):
    try:
        venue_encoded = label_encoder_venue.transform([venue])[0]
    except ValueError:
        venue_encoded = -1  
    try:
        opponent_encoded = label_encoder_opponent.transform([opponent])[0]
    except ValueError:
        opponent_encoded = -1  
    try:
        club_encoded = label_encoder_club.transform([club])[0]
    except ValueError:
        club_encoded = -1  
    input_data = pd.DataFrame({
        'Venue': [venue_encoded],
        'Opponent': [opponent_encoded],
        'Club': [club_encoded]
    })
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    return prediction, probability

# Get valid team names from the data
team_names = set()
for match in matches:
    if match['homeTeam']:
        team_names.add(match['homeTeam'])
    if match['awayTeam']:
        team_names.add(match['awayTeam'])
team_names = sorted(team_names)

valid_venues = ['Home', 'Away']

def choose_from_list(prompt, options):
    print(prompt)
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

print("\n--- Match Outcome Prediction ---")
venue = choose_from_list("Select the venue:", valid_venues)
opponent = choose_from_list("Select the opponent team:", team_names)
club = choose_from_list("Select your club:", team_names)

predicted_outcome, probability = predict_match_outcome(
    venue, opponent, club,
    label_encoder_venue,
    label_encoder_opponent,
    label_encoder_club,
    scaler
)

print(f"\nPredicted outcome: {predicted_outcome}")
result_mapping = model.classes_
for i, result in enumerate(result_mapping):
    print(f"Probability of {result}: {probability[i]:.2f} ({probability[i]*100:.1f}%)")

# Remove the old commentator_description function and use the new one
# Find the top predicted outcome and probability
proba_dict = {result: prob for result, prob in zip(result_mapping, probability)}
top_result = max(proba_dict, key=proba_dict.get)
top_prob = proba_dict[top_result]

commentary = get_commentary_template(top_result, club, opponent, venue, top_prob)
print("\n--- Match Commentary ---")
print(commentary)