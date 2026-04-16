from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Simulated data for bearings
bearings_data = {
    'plant_1': {
        'bearing_1': {'health_score': random.randint(0, 100)},
        'bearing_2': {'health_score': random.randint(0, 100)}
    },
    'plant_2': {
        'bearing_1': {'health_score': random.randint(0, 100)},
        'bearing_2': {'health_score': random.randint(0, 100)}
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bearings')
def get_bearings_data():
    # Return simulated bearing data as JSON
    return jsonify(bearings_data)

@app.route('/api/bearings/<plant>/<bearing>')
def get_bearing_details(plant, bearing):
    # Return details for a specific bearing
    return jsonify(bearings_data.get(plant, {}).get(bearing, {}))

if __name__ == '__main__':
    app.run(debug=True)