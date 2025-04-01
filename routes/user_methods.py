from flask import render_template, request, redirect, url_for, jsonify
from models.user import db, User  # Import db and User model

# Display all users
def index():
    # Query all users from the database
    users = User.query.all()

    # Convert all users to a list of dictionaries using the to_dict method
    users_list = [user.to_dict() for user in users]

    # Return the list as a JSON response
    return jsonify(users_list)


# Add a new user
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_user.html')

# Delete a user by ID
def delete_user(id):
    user = User.query.get_or_404(id)  # Get user by ID or return 404 if not found
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))
