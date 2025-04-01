from flask import Flask, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models.report import Report

from models.user import User
from routes import user_methods
from routes import report_methods

app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database in the same directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy with the app
db.init_app(app)

# Route to create the database tables
@app.before_request
def create_tables():
    db.create_all()  # Create all tables defined by SQLAlchemy models
    add_test_users()
    insert_test_reports()

def insert_test_reports():
    # Insert a bunch of test reports
    test_reports = [
        {"name": "Test Report 1", "description": "Test description 1", "longitude": 40.7128, "latitude": -74.0060, "category": "Incident"},
        {"name": "Test Report 2", "description": "Test description 2", "longitude": 34.0522, "latitude": -118.2437, "category": "Crime"},
        {"name": "Test Report 3", "description": "Test description 3", "longitude": 51.5074, "latitude": -0.1278, "category": "Accident"},
        {"name": "Test Report 4", "description": "Test description 4", "longitude": 48.8566, "latitude": 2.3522, "category": "Fire"}
    ]

    # Insert the test reports into the database
    for report in test_reports:
        new_report = Report(
            name=report["name"],
            description=report["description"],
            longitude=report["longitude"],
            latitude=report["latitude"],
            category=report["category"]
        )
        db.session.add(new_report)

    db.session.commit()  # Commit the changes to the database

def add_test_users():
    # List of test users with predefined usernames, emails, and passwords
    test_users = [
        {'username': 'testuser1', 'email': 'testuser1@example.com', 'password': 'testpassword1'},
        {'username': 'testuser2', 'email': 'testuser2@example.com', 'password': 'testpassword2'},
        {'username': 'testuser3', 'email': 'testuser3@example.com', 'password': 'testpassword3'},
        {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpassword'}
    ]
    # Loop through test users and add them to the database
    for user_data in test_users:
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        # Check if the user already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            hashed_password = generate_password_hash(password)  # Hash the password
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)  # Add the user to the session
            db.session.commit()  # Commit the transaction to the database
            print(f"Added test user: {username}")
        else:
            print(f"User {username} already exists.")


# Secret key for session management
app.secret_key = 'CYPRESS2025'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username exists and password is correct
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user_id in session
            session['username'] = user.username  # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # If the user is not logged in, redirect to login
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('home.html', username=session['username'])

@app.route('/page1')

def page1():
    # If the user is not logged in, redirect to login
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('page1.html')

@app.route('/page2')
def page2():
    # If the user is not logged in, redirect to login
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('page2.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#TEST METHODS
@app.route('/users', methods=['GET'])
def get_users():
    return user_methods.index()

@app.route('/reports', methods=['GET'])
def get_reports():
    return report_methods.index()

if __name__ == '__main__':
    app.run(debug=True)
