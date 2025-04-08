import json
import random
from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models.report import Report
from models.subscription import Subscription

from models.user import User
from routes import user_methods
from routes import report_methods
from flask_graphql import GraphQLView

import graphene

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
        {"name": "Test Report 1", "description": "Test description 1", "latitude": 43.65457013324826, "longitude": -79.38077450452194, "category": "Incident"},
        {"name": "Test Report 2", "description": "Test description 2", "latitude": 43.6580165713743, "longitude": -79.38048482588174, "category": "Crime"},
        {"name": "Test Report 3", "description": "Test description 3", "latitude": 43.66004242578571, "longitude": -79.37972307851004, "category": "Accident"},
        {"name": "Test Report 4", "description": "Test description 4", "latitude": 43.657869092737954, "longitude": -79.37824249923946, "category": "Fire"},
        {"name": "Test Report 5", "description": "Test description 5", "latitude": 43.66136259947873, "longitude": -79.38333591925759, "category": "Fire"},
        {"name": "Test Report 6", "description": "Test description 6", "latitude": 43.66767544146261, "longitude": -79.38292014575401, "category": "Accident"},
        {"name": "Test Report 7", "description": "Test description 7", "latitude": 43.66854464216485, "longitude": -79.391267179834, "category": "Incident"},
        {"name": "Test Report 8", "description": "Test description 8", "latitude": 43.64056114119252, "longitude": -79.40079318339204, "category": "Incident"},
        {"name": "Test Report 9", "description": "Test description 9", "latitude": 43.64686758906263, "longitude": -79.36930262096327, "category": "Crime"},
        {"name": "Test Report 10", "description": "Test description 10", "latitude": 43.650123, "longitude": -79.377456, "category": "Fire"},
        {"name": "Test Report 11", "description": "Test description 11", "latitude": 43.652789, "longitude": -79.386543, "category": "Accident"},
        {"name": "Test Report 12", "description": "Test description 12", "latitude": 43.655321, "longitude": -79.390678, "category": "Incident"},
        {"name": "Test Report 13", "description": "Test description 13", "latitude": 43.659876, "longitude": -79.374112, "category": "Crime"},
        {"name": "Test Report 14", "description": "Test description 14", "latitude": 43.664234, "longitude": -79.384321, "category": "Fire"},
        {"name": "Test Report 15", "description": "Test description 15", "latitude": 43.662543, "longitude": -79.379432, "category": "Accident"},
        {"name": "Test Report 16", "description": "Test description 16", "latitude": 43.669001, "longitude": -79.371234, "category": "Crime"},
        {"name": "Test Report 17", "description": "Test description 17", "latitude": 43.670456, "longitude": -79.390321, "category": "Incident"},
        {"name": "Test Report 18", "description": "Test description 18", "latitude": 43.671890, "longitude": -79.375678, "category": "Fire"},
        {"name": "Test Report 19", "description": "Test description 19", "latitude": 43.673210, "longitude": -79.389012, "category": "Accident"},
        {"name": "Test Report 20", "description": "Test description 20", "latitude": 49.282729, "longitude": -123.120738, "category": "Incident"},
        {"name": "Test Report 21", "description": "Test description 21", "latitude": 49.276790, "longitude": -123.130680, "category": "Crime"},
        {"name": "Test Report 22", "description": "Test description 22", "latitude": 49.270877, "longitude": -123.115431, "category": "Accident"},
        {"name": "Test Report 23", "description": "Test description 23", "latitude": 49.263611, "longitude": -123.138611, "category": "Fire"},
        {"name": "Test Report 24", "description": "Test description 24", "latitude": 49.289347, "longitude": -123.123907, "category": "Fire"},
        {"name": "Test Report 25", "description": "Test description 25", "latitude": 49.261821, "longitude": -123.113175, "category": "Crime"},
        {"name": "Test Report 26", "description": "Test description 26", "latitude": 49.280075, "longitude": -123.104755, "category": "Incident"},
        {"name": "Test Report 27", "description": "Test description 27", "latitude": 49.268244, "longitude": -123.152498, "category": "Accident"},
        {"name": "Test Report 28", "description": "Test description 28", "latitude": 49.284401, "longitude": -123.121659, "category": "Fire"},
        {"name": "Test Report 29", "description": "Test description 29", "latitude": 49.277498, "longitude": -123.133181, "category": "Incident"},
        # Montreal, QC
        {"name": "Test Report 30", "description": "Test description 30", "latitude": 45.501689, "longitude": -73.567256, "category": "Incident"},
        {"name": "Test Report 31", "description": "Test description 31", "latitude": 45.508840, "longitude": -73.554123, "category": "Crime"},
        {"name": "Test Report 32", "description": "Test description 32", "latitude": 45.495321, "longitude": -73.578901, "category": "Accident"},
        {"name": "Test Report 33", "description": "Test description 33", "latitude": 45.512345, "longitude": -73.560789, "category": "Fire"},
        # Calgary, AB
        {"name": "Test Report 34", "description": "Test description 34", "latitude": 51.044733, "longitude": -114.071883, "category": "Incident"},
        {"name": "Test Report 35", "description": "Test description 35", "latitude": 51.038912, "longitude": -114.065432, "category": "Crime"},
        {"name": "Test Report 36", "description": "Test description 36", "latitude": 51.050123, "longitude": -114.080567, "category": "Accident"},
        # Halifax, NS
        {"name": "Test Report 37", "description": "Test description 37", "latitude": 44.648862, "longitude": -63.575320, "category": "Fire"},
        {"name": "Test Report 38", "description": "Test description 38", "latitude": 44.642345, "longitude": -63.580123, "category": "Incident"},
        {"name": "Test Report 39", "description": "Test description 39", "latitude": 44.655678, "longitude": -63.570987, "category": "Crime"},
        # Winnipeg, MB
        {"name": "Test Report 40", "description": "Test description 40", "latitude": 49.895136, "longitude": -97.138374, "category": "Accident"},
        {"name": "Test Report 41", "description": "Test description 41", "latitude": 49.887654, "longitude": -97.145678, "category": "Fire"},
        # Ottawa, ON
        {"name": "Test Report 42", "description": "Test description 42", "latitude": 45.421530, "longitude": -75.697193, "category": "Incident"},
        {"name": "Test Report 43", "description": "Test description 43", "latitude": 45.415678, "longitude": -75.690123, "category": "Crime"},
        # Edmonton, AB
        {"name": "Test Report 44", "description": "Test description 44", "latitude": 53.544389, "longitude": -113.490927, "category": "Accident"},
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
            user_id=assigned_user.id,
            last_updated=None
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
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/guest_login', methods=['POST'])


def guest_login():
    flash('You have signed in as a guest.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # If the user is not logged in, redirect to login
    if 'username' not in session:
        return render_template('home_guestmode.html')


    return render_template('home.html', username=session['username'], usertype=session.get('user_type'))

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

@app.route('/map_reports')
def rep():
    return report_methods.index()  # Admin sees all reports

@app.route('/map')
def map():
    return render_template('map.html')


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
    else:
        flash('Report not found.', 'danger')  # Handle case if the report doesn't exist
    return redirect(url_for('reports'))  # Redirect back to the list of reports


@app.route('/subscribe/<int:report_id>', methods=['GET'])
def subscribe_view(report_id):
    user_id = session.get('user_id')
    report = Report.query.get_or_404(report_id)

    # Check if subscription exists
    subscription = Subscription.query.filter_by(user_id=user_id, report_id=report_id).first()
    is_subscribed = subscription is not None

    return render_template('subscribe_view.html', report=report, is_subscribed=is_subscribed)

@app.route('/subscribe/<int:report_id>', methods=['POST'])
def subscribe_to_report(report_id):
    user_id = session.get('user_id')
    existing = Subscription.query.filter_by(user_id=user_id, report_id=report_id).first()

    if existing:
        print("You're already subscribed.")
    else:
        new_sub = Subscription(user_id=user_id, report_id=report_id)
        db.session.add(new_sub)
        db.session.commit()

    return redirect(url_for('subscribe_view', report_id=report_id))

@app.route('/unsubscribe/<int:report_id>', methods=['POST'])
def unsubscribe(report_id):
    user_id = session.get('user_id')
    subscription = Subscription.query.filter_by(user_id=user_id, report_id=report_id).first()

    if subscription:
        db.session.delete(subscription)
        db.session.commit()
        print("Unsubscribed successfully.")
    else:
        print("You're not subscribed to this report.")

    return redirect(url_for('subscribe_view', report_id=report_id))
# # map filtering using GraphQL

# GraphQL object Type
class ReportType(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()
    latitude = graphene.Float()  # Changed from Int to Float since your coordinates are decimals
    longitude = graphene.Float()  # Changed from Int to Float since your coordinates are decimals
    category = graphene.String()


# the filteringSystem

class Query(graphene.ObjectType):
    reports = graphene.List(ReportType, category=graphene.String())

    def resolve_reports(self, info, category=None):
        print("GraphQL received category:", category)
        if category == "Incident":
            return Report.query.filter(Report.category == "Incident").all()
        elif category == "Fire":
            return Report.query.filter(Report.category == "Fire").all()
        elif category == "Accident":
            return Report.query.filter(Report.category == "Accident").all()
        elif category == "Crime":
            return Report.query.filter(Report.category == "Crime").all()
        elif category == "All":
            return Report.query.all()
        else:
            return Report.query.all()

# Create the GraphQL schema
schema = graphene.Schema(query=Query)

# Add GraphQL endpoint to Flask app
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route('/create_report', methods=['GET'])
def create_report():
    return render_template('new_report.html')

@app.route('/create_report', methods=['POST'])
def insert_report():
    # Get the data from the form (not JSON, but form data)
    name = request.form.get('report-title')
    description = request.form.get('description')
    category = request.form.get('category')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    user_id = session.get('user_id')

    # Ensure the required fields are provided
    if not name or not description:
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new report object
    new_report = Report(
        name=name,
        description=description,
        category=category,
        latitude=latitude,
        longitude=longitude,
        user_id=user_id
    )

    # Add the new report to the database
    db.session.add(new_report)
    db.session.commit()

    # Redirect to the list of all reports (or you can redirect to a success page)
    return redirect(url_for('dashboard'))

@app.route('/view_users')
def view_users():
    usersAll = User.query.all()  # Admin sees all reports

    return render_template('view_users.html', users=usersAll)


if __name__ == '__main__':
    app.run(debug=True)
