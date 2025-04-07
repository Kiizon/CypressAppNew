from db import db

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # New: Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Optional relationship to access report.user directly
    user = db.relationship('User', backref='Subscription')

    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

    report = db.relationship('Report', backref='Subscription')

    def __repr__(self):
        return f'<Subscription User {self.user_id} -> Report {self.report_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'report_id': self.report_id
        }
