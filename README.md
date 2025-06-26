# Premier League AI Predictor

A machine learning-powered web application that predicts Premier League match outcomes using historical data and provides AI-generated match commentary.

## 🏆 Features

- **Match Outcome Prediction**: Predicts win, draw, or loss for Premier League matches
- **AI Commentary**: Generates realistic match commentary based on predictions
- **Web Interface**: Modern, responsive web UI for easy interaction
- **REST API**: Flask backend with CORS support for integration
- **Historical Data**: Uses real Premier League match data from 2023-2024 seasons

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "PL AI Analysis"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open the web interface**
   - Navigate to `http://localhost:5000` in your browser
   - Or open `PL AI Predictor.html` directly

## 📁 Project Structure

```
PL AI Analysis/
├── app.py                          # Flask backend server
├── Sports AI Model.py              # Data collection and model training
├── commentary_templates.py         # AI commentary generation
├── PL AI Predictor.html           # Web interface
├── predictor.js                   # Frontend JavaScript
├── requirements.txt               # Python dependencies
├── Procfile.rxr                   # Deployment configuration
└── Data/
    ├── models/
    │   ├── match_prediction_model.pkl    # Trained ML model
    │   └── encoders_and_scaler.pkl       # Data preprocessing
    ├── all_clubs_fixtures.csv            # Combined match data
    └── [club]_fixtures.csv               # Individual club data
```

## 🎯 How It Works

### Data Collection
- Fetches Premier League match data from the Football-Data.org API
- Collects historical match results from 2023-2024 seasons
- Processes venue, opponent, and club information

### Machine Learning Model
- Uses scikit-learn for prediction
- Features: Venue (Home/Away), Opponent Team, Club
- Output: Win, Draw, or Loss prediction with probability scores
- Includes data preprocessing with label encoders and scalers

### AI Commentary
- Generates contextual match commentary based on predictions
- Uses probability scores to create realistic commentary
- Provides different templates for win, draw, loss, and uncertain outcomes

## 🌐 API Usage

### Predict Match Outcome

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
    "venue": "Home",
    "club": "Arsenal",
    "opponent": "Manchester City"
}
```

**Response:**
```json
{
    "predicted_outcome": "win",
    "commentary": "And it's looking good for Arsenal at home! Our model gives them a 65.2% chance to win against Manchester City."
}
```

### Available Teams
- Arsenal
- Aston Villa
- Brighton & Hove Albion
- Chelsea
- Liverpool
- Manchester City
- Manchester United
- Newcastle United
- Tottenham Hotspur
- West Ham United

## 🛠️ Development

### Running the Model Locally
```bash
python "Sports AI Model.py"
```

### API Development
```bash
python app.py
```

### Frontend Development
- Edit `PL AI Predictor.html` for UI changes
- Modify `predictor.js` for frontend logic
- Update `commentary_templates.py` for new commentary styles

## 📊 Data Sources

- **Football-Data.org API**: Premier League match data
- **Seasons**: 2023-2024
- **Data Points**: Match results, teams, venues, scores

## 🔧 Dependencies

- **Flask**: Web framework
- **flask-cors**: Cross-origin resource sharing
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning
- **requests**: HTTP requests

## 🚀 Deployment

The project includes a `Procfile.rxr` for deployment on platforms like Heroku.

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue in the repository.

---

**Note**: This application uses historical Premier League data for predictions. Results are for entertainment purposes and should not be used for betting or gambling decisions. 
