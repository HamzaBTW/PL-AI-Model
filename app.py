from flask import Flask, request, jsonify
import pickle
import pandas as pd
from commentary_templates import get_commentary_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model and encoders
with open('Data/models/match_prediction_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('Data/models/encoders_and_scaler.pkl', 'rb') as f:
    encoders = pickle.load(f)

label_encoder_venue = encoders['venue_encoder']
label_encoder_opponent = encoders['opponent_encoder']
label_encoder_club = encoders['club_encoder']
scaler = encoders['scaler']

def predict_match_outcome(venue, opponent, club):
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
    result_mapping = model.classes_
    proba_dict = {result: prob for result, prob in zip(result_mapping, probability)}
    top_result = max(proba_dict, key=proba_dict.get)
    top_prob = proba_dict[top_result]
    commentary = get_commentary_template(top_result, club, opponent, venue, top_prob)
    return prediction, commentary

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    venue = data['venue']
    club = data['club']
    opponent = data['opponent']
    predicted_outcome, commentary = predict_match_outcome(venue, opponent, club)
    return jsonify({
        'predicted_outcome': predicted_outcome,
        'commentary': commentary
    })

if __name__ == '__main__':
    app.run(debug=True)