from db import db  # Import the db instance from db.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    # Method to serialize User object to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }
