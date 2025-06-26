// predictor.js

// Example team list, should be replaced by backend fetch if needed
const teams = [
    'Arsenal FC', 'Aston Villa FC', 'Brentford FC', 'Brighton & Hove Albion FC', 'Burnley FC',
    'Chelsea FC', 'Crystal Palace FC', 'Everton FC', 'Fulham FC', 'Leeds United FC',
    'Liverpool FC', 'Manchester City FC', 'Manchester United FC', 'Newcastle United FC',
    'Nottingham Forest FC', 'Sunderland AFC', 'Tottenham Hotspur FC', 'West Ham United FC',
    'Wolverhampton Wanderers FC', 'AFC Bournemouth'
];

function populateTeams() {
    const clubSelect = document.getElementById('club');
    const opponentSelect = document.getElementById('opponent');
    clubSelect.innerHTML = '';
    opponentSelect.innerHTML = '';
    teams.forEach(team => {
        const option1 = document.createElement('option');
        option1.value = option1.text = team;
        clubSelect.appendChild(option1);
        const option2 = document.createElement('option');
        option2.value = option2.text = team;
        opponentSelect.appendChild(option2);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    populateTeams();

    document.getElementById('predict-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const venue = document.getElementById('venue').value;
        const club = document.getElementById('club').value;
        const opponent = document.getElementById('opponent').value;
        if (club === opponent) {
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').innerText = 'Please select two different teams.';
            return;
        }
        // Call backend API (Flask)
        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ venue, club, opponent })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').innerHTML =
                `<div class='chat-label'>Predicted Outcome</div><div><strong>${data.predicted_outcome}</strong></div><br>` +
                `<div class='chat-label'>Commentary</div><div>${data.commentary}</div>`;
        } catch (error) {
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').innerText = 'Error: Could not connect to prediction server.';
        }
    });
}); 