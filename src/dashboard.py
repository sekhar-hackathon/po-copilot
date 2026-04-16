from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Simulate fetching real-time bearing health scores
    plants = ['Plant A', 'Plant B', 'Plant C']
    bearings = ['Bearing 1', 'Bearing 2', 'Bearing 3']
    health_scores = {
        plant: {bearing: random.randint(0, 100) for bearing in bearings} for plant in plants
    }
    
    # Determine color based on health score
    def get_color(score):
        if score > 75:
            return 'green'
        elif score > 50:
            return 'yellow'
        else:
            return 'red'

    # Prepare data for rendering
    data = {
        plant: {
            bearing: {'score': score, 'color': get_color(score)}
            for bearing, score in plant_scores.items()
        } for plant, plant_scores in health_scores.items()
    }

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)