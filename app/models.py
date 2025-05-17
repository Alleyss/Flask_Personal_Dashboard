from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  # Explicitly name the table 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    
    tasks = db.relationship('Task', backref='users', lazy=True)
    finances = db.relationship('Finance', backref='users', lazy=True)
    diaries = db.relationship('Diary', backref='users', lazy=True)
    habits = db.relationship('Habit', backref='users', lazy=True)
    progress = db.relationship('Progress', backref='users', lazy=True)
    reminders = db.relationship('Reminder', backref='users', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct reference to 'users' table


class Finance(db.Model):
    __tablename__ = 'finances'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.Enum('credit', 'debit', name='transaction_type'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct reference to 'users' table
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Diary(db.Model):
    __tablename__ = 'diaries'
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct reference to 'users' table


class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct reference to 'users' table


class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    progress = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct reference to 'users' table


class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct reference to 'users' table
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    reminder_date = db.Column(db.DateTime, nullable=False)
