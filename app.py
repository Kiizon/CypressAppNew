import json
import random
from flask import Flask, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models.report import Report
from models.subscription import Subscription

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
@app.cli.command('init-db')
def init_db():
    """Create all tables and insert test data"""
    db.create_all()  # Create all tables defined by SQLAlchemy models
    add_test_users()  # Add test users if needed
    insert_test_reports()  # Insert test reports if needed
    print("Database initialized and test data added.")

def add_test_users():
    # List of test users with predefined usernames, emails, and passwords
    test_users = [
        {'username': 'testuser1', 'email': 'testuser1@example.com', 'password': 'testpassword1',
         'notifications': 1, 'user_type': 1, 'phone': '1234567890'},
        {'username': 'testuser2', 'email': 'testuser2@example.com', 'password': 'testpassword2',
         'notifications': 1, 'user_type': 1, 'phone': '2345678901'},
        {'username': 'testuser3', 'email': 'testuser3@example.com', 'password': 'testpassword3',
         'notifications': 1, 'user_type': 1, 'phone': '3456789012'},
        {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpassword',
         'notifications': 1, 'user_type': 0, 'phone': '9876543210'}
    ]
    # Loop through test users and add them to the database
    for user_data in test_users:
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        notifications = user_data['notifications']
        user_type = user_data['user_type']
        phone = user_data['phone']

        # Check if the user already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            hashed_password = generate_password_hash(password)  # Hash the password
            new_user = User(username=username, email=email, password=hashed_password, notifications=notifications, usertype=user_type, phone=phone)
            db.session.add(new_user)  # Add the user to the session
            db.session.commit()  # Commit the transaction to the database
            print(f"Added test user: {username}")
        else:
            print(f"User {username} already exists.")


def insert_test_reports():
    # Fetch all non-admin users
    users = User.query.filter_by(usertype=1).all()

    if not users:
        print("No non-admin users found. Please add users first.")
        return

    # Test reports to insert
    test_reports = [
        {"name": "Test Report 1", "description": "Test description 1", "longitude": 40.7128, "latitude": -74.0060, "category": "Incident"},
        {"name": "Test Report 2", "description": "Test description 2", "longitude": 34.0522, "latitude": -118.2437, "category": "Crime"},
        {"name": "Test Report 3", "description": "Test description 3", "longitude": 51.5074, "latitude": -0.1278, "category": "Accident"},
        {"name": "Test Report 4", "description": "Test description 4", "longitude": 48.8566, "latitude": 2.3522, "category": "Fire"}
    ]

    # Insert reports with random user assignment
    for report in test_reports:
        assigned_user = random.choice(users)  # Pick a random non-admin user
        new_report = Report(
            name=report["name"],
            description=report["description"],
            longitude=report["longitude"],
            latitude=report["latitude"],
            category=report["category"],
            user_id=assigned_user.id
        )
        db.session.add(new_report)

    db.session.commit()
    print("Test reports inserted with random user assignments.")

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
        return render_template('home_guestmode.html')


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
def reports():
    user_type = session.get('user_type')

    user_id = session.get('user_id')
    reportsAll = Report.query.all()  # Admin sees all reports
    reports = Report.query.filter_by(user_id=user_id).all()  # User sees only their reports

    return render_template('view_reports.html', user_type=user_type, reports=reports, reportsAll=reportsAll)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/create_report')
def create_report():
    return render_template('placeholder.html', page_title='CR')

@app.route('/settings')
def settings():
    return render_template('placeholder.html', page_title='Settings')

@app.route('/logs')
def logs():
    return render_template('placeholder.html', page_title='View Logs')

@app.route('/edit_report/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    report = Report.query.get_or_404(report_id)

    if session.get('user_type') == 0 or report.user_id == session.get('user_id'):
        if request.method == 'POST':
            # Update report details based on form input
            report.name = request.form['name']
            report.description = request.form['description']
            report.category = request.form['category']
            report.address = request.form['address']  # Saving the address (optional)
            report.longitude = request.form['longitude']
            report.latitude = request.form['latitude']

            db.session.commit()
            return redirect(url_for('reports'))

        return render_template('edit_report.html', report=report)

    else:
        return redirect(url_for('reports'))

@app.route('/confirm_delete/<int:report_id>', methods=['GET'])
def confirm_delete(report_id):
    report = Report.query.get(report_id)  # Find the report by ID
    if not report:
        flash('Report not found.', 'danger')
        return redirect(url_for('view_reports'))  # Redirect back if report not found
    return render_template('confirm_delete.html', report=report)


@app.route('/delete_report/<int:report_id>', methods=['GET'])
def delete_report(report_id):
    report = Report.query.get(report_id)  # Find the report by ID
    if report:
        db.session.delete(report)  # Delete the report
        db.session.commit()  # Commit the change to the database
        flash('Report deleted successfully.', 'success')  # Success message
    else:
        flash('Report not found.', 'danger')  # Handle case if the report doesn't exist
    return redirect(url_for('reports'))  # Redirect back to the list of reports


@app.route('/subscribe/<int:report_id>', methods=['GET'])
def subscribe_screen(report_id):
    # Fetch the specific report based on the report_id
    report = Report.query.get_or_404(report_id)

    # Check if the user is already subscribed to this report
    subscription = Subscription.query.filter_by(user_id=session.get('user_id'), report_id=report_id).first()

    # If subscribed, set the flag
    is_subscribed = subscription is not None

    return render_template('subscribe.html', report=report, is_subscribed=is_subscribed)

@app.route('/subscribe/<int:report_id>/subscribe', methods=['GET'])
def subscribe(report_id):
    # Check if the user is already subscribed to this report
    subscription = Subscription.query.filter_by(user_id=session.get('user_id'), report_id=report_id).first()

    if subscription:
        flash("You are already subscribed to this report.", 'warning')
        return redirect(url_for('subscribe_screen', report_id=report_id))

    # Add the subscription if not already subscribed
    new_subscription = Subscription(user_id=session.get('user_id'), report_id=report_id)
    db.session.add(new_subscription)
    db.session.commit()

    flash("You have successfully subscribed to this report.", 'success')
    return redirect(url_for('subscribe_screen', report_id=report_id))

if __name__ == '__main__':
    app.run(debug=True)
