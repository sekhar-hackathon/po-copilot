from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Load bearing health scores from a data source
    health_scores = load_health_scores()
    return render_template('dashboard.html', health_scores=health_scores)


def load_health_scores() -> dict:
    # Placeholder for loading health scores from a real-time data source
    # This could be replaced with a call to a database or an API
    return {
        'Plant A': {'Bearing 1': 85, 'Bearing 2': 90},
        'Plant B': {'Bearing 1': 75, 'Bearing 2': 80}
    }

if __name__ == '__main__':
    app.run(debug=True)