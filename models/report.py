from db import db  # Import the db instance from db.py


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)

    # New fields
    longitude = db.Column(db.Float, nullable=True)  # Longitude field (float)
    latitude = db.Column(db.Float, nullable=True)  # Latitude field (float)
    category = db.Column(db.String(100), nullable=True)  # Category field (string)

    def __repr__(self):
        return f'<Report {self.name}>'

    # Method to serialize Report object to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'category': self.category,
        }
