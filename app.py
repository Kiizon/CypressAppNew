from flask import Flask, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import db, User
from routes.user_methods import index
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

# Sample user data (in practice, store this in a database)
users = {
    'user1': 'password123',
    'user2': 'mypassword'
}

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

@app.route('/users', methods=['GET'])
def get_users():
    return index()

if __name__ == '__main__':
    app.run(debug=True)
