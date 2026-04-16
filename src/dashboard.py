from flask import Flask, render_template, request
from typing import Dict, Any

app = Flask(__name__)

# Mock data for demonstration purposes
bearings_data = {
    'Plant A': {
        'Bearing 1': {'health_score': 85, 'details': 'Normal operation'},
        'Bearing 2': {'health_score': 70, 'details': 'Requires maintenance'},
    },
    'Plant B': {
        'Bearing 3': {'health_score': 90, 'details': 'Optimal performance'},
        'Bearing 4': {'health_score': 60, 'details': 'Critical condition'},
    }
}

@app.route('/')
def index() -> str:
    plant = request.args.get('plant', 'Plant A')
    bearings = bearings_data.get(plant, {})
    return render_template('dashboard.html', plant=plant, bearings=bearings)

@app.route('/details/<plant>/<bearing>')
def details(plant: str, bearing: str) -> str:
    bearing_info = bearings_data.get(plant, {}).get(bearing, {})
    return render_template('details.html', plant=plant, bearing=bearing, info=bearing_info)

if __name__ == '__main__':
    app.run(debug=True)