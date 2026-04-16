from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False)

class BearingHealth(db.Model):
    id = Column(Integer, primary_key=True)
    bearing_id = Column(String(50), unique=True, nullable=False)
    health_score = Column(Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Operator':
        return "Access Denied", 403
    bearings = BearingHealth.query.all()
    return render_template('dashboard.html', bearings=bearings)

@app.route('/bearing/<int:bearing_id>')
@login_required
def bearing_detail(bearing_id):
    if current_user.role != 'Operator':
        return "Access Denied", 403
    bearing = BearingHealth.query.get_or_404(bearing_id)
    return render_template('bearing_detail.html', bearing=bearing)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)