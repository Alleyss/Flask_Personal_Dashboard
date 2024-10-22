from . import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    total_amount = db.Column(db.Integer,nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10),nullable=False)#credit or debit
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    progress = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Assuming you have a users table
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    reminder_date = db.Column(db.DateTime, nullable=False)  # Date and time for the reminder
    
    user = db.relationship('User', backref='reminders')  # Establish relationship with User

    def to_dict(self):
        """This method will allow us to easily convert the Reminder object into a dictionary format."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'reminder_date': self.reminder_date.strftime('%Y-%m-%d %H:%M:%S')
        }