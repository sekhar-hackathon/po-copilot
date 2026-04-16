from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    # This should be replaced with a real user loading mechanism
    return User(user_id, 'operator')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'operator':
        return "Access Denied", 403
    # Mock data for demonstration
    bearings = [
        {'id': 1, 'score': 85, 'status': 'Green'},
        {'id': 2, 'score': 60, 'status': 'Yellow'},
        {'id': 3, 'score': 30, 'status': 'Red'}
    ]
    return render_template('dashboard.html', bearings=bearings)

@app.route('/bearing/<int:bearing_id>')
@login_required
def bearing_details(bearing_id):
    if current_user.role != 'operator':
        return "Access Denied", 403
    # Mock data for demonstration
    bearing = {'id': bearing_id, 'score': 85, 'status': 'Green', 'details': 'Detailed information about bearing'}
    return render_template('bearing_details.html', bearing=bearing)

if __name__ == '__main__':
    app.run(debug=True)