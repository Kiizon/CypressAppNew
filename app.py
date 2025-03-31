from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Sample user data (in practice, store this in a database)
users = {
    'user1': 'password123',
    'user2': 'mypassword'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password, please try again."

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # If the user is not logged in, redirect to login
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('home.html', username=session['username'])

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
