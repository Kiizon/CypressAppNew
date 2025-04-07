from db import db

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(100), nullable=True)

    # New: Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Optional relationship to access report.user directly
    user = db.relationship('User', backref='reports')

    def __repr__(self):
        return f'<Report {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'category': self.category,
            'user_id': self.user_id
        }
