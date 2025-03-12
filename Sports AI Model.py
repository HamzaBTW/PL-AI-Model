import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Define the data directory path
DATA_DIR = r"C:\Users\hamza\Coding\projects\Sport AI Analysis\Data"

# Load the fixtures data from the specified directory
fixtures_file_path = os.path.join(DATA_DIR, "all_clubs_fixtures.csv")
fixtures_df = pd.read_csv(fixtures_file_path)

print(f"Loaded data from {fixtures_file_path}")
print(f"Data shape: {fixtures_df.shape}")

for col in ['Venue', 'Opponent', 'Club']:
    fixtures_df[col] = fixtures_df[col].astype(object)

fixtures_df.fillna("Unknown", inplace=True)

label_encoder_venue = LabelEncoder()
label_encoder_opponent = LabelEncoder()
label_encoder_club = LabelEncoder()

fixtures_df['Venue'] = label_encoder_venue.fit_transform(fixtures_df['Venue'])
fixtures_df['Opponent'] = label_encoder_opponent.fit_transform(fixtures_df['Opponent'])
fixtures_df['Club'] = label_encoder_club.fit_transform(fixtures_df['Club'])

X = fixtures_df[['Venue', 'Opponent', 'Club']]  
y = fixtures_df['Result']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, solver='liblinear', C=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the model and encoders for future use
import pickle

# Create a models directory if it doesn't exist
MODELS_DIR = os.path.join(DATA_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Save the model and encoders
with open(os.path.join(MODELS_DIR, 'match_prediction_model.pkl'), 'wb') as f:
    pickle.dump(model, f)
    
with open(os.path.join(MODELS_DIR, 'encoders_and_scaler.pkl'), 'wb') as f:
    pickle.dump({
        'venue_encoder': label_encoder_venue,
        'opponent_encoder': label_encoder_opponent,
        'club_encoder': label_encoder_club,
        'scaler': scaler
    }, f)

print(f"Model and encoders saved to {MODELS_DIR}")

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

# Get user input for prediction
print("\n--- Match Outcome Prediction ---")
venue = input("Enter the venue (Home/Away): ")
opponent = input("Enter the opponent team: ")
club = input("Enter your club: ")

# Make prediction
predicted_outcome, probability = predict_match_outcome(venue, opponent, club, 
                                                      label_encoder_venue, 
                                                      label_encoder_opponent, 
                                                      label_encoder_club, 
                                                      scaler)

print(f"\nPredicted outcome: {predicted_outcome}")

# Display probability information
result_mapping = model.classes_
for i, result in enumerate(result_mapping):
    print(f"Probability of {result}: {probability[i]:.2f} ({probability[i]*100:.1f}%)")