from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Simulated data for demonstration purposes
def get_bearing_health_scores():
    return [
        {'plant': 'Plant A', 'bearing_id': 1, 'score': random.randint(0, 100)},
        {'plant': 'Plant A', 'bearing_id': 2, 'score': random.randint(0, 100)},
        {'plant': 'Plant B', 'bearing_id': 1, 'score': random.randint(0, 100)},
        {'plant': 'Plant B', 'bearing_id': 2, 'score': random.randint(0, 100)}
    ]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('initial_data', get_bearing_health_scores())

@socketio.on('request_update')
def handle_request_update():
    emit('update_data', get_bearing_health_scores())

if __name__ == '__main__':
    socketio.run(app, debug=True)
