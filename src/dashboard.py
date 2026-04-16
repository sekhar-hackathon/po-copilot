from flask import Flask, render_template, jsonify
import time
import random

app = Flask(__name__)

# Simulated data source for bearing health scores
def get_bearing_health_scores() -> dict:
    # Simulating health scores for bearings
    return {
        'bearing_1': random.uniform(0, 100),
        'bearing_2': random.uniform(0, 100),
        'bearing_3': random.uniform(0, 100)
    }

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/health_scores')
def health_scores():
    start_time = time.time()
    scores = get_bearing_health_scores()
    response_time = time.time() - start_time
    return jsonify({'scores': scores, 'response_time': response_time})

if __name__ == '__main__':
    app.run(debug=True)
