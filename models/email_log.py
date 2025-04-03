from db import db

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_id = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<EmailLog User {self.user_id} -> Report {self.report_id} at {self.date_time}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'date_time': self.date_time
        }
