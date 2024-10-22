from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user
from . import db
from .models import User, Task, Finance, Diary, Habit, Progress,Reminder
from werkzeug.security import generate_password_hash, check_password_hash
from .decorators import login_required
from datetime import datetime

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match!')
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Other routes for todolist, finance, diary, etc.
##Calendar
@app.route('/create_reminder', methods=['POST'])
def create_reminder():
    if request.method == 'POST':
        data = request.get_json()  # Fetch the data sent via JavaScript or a form
        title = data.get('title')
        description = data.get('description', '')
        reminder_date = datetime.strptime(data.get('reminder_date'), '%Y-%m-%d %H:%M:%S')

        # Create new reminder
        new_reminder = Reminder(
            user_id=current_user.id,
            title=title,
            description=description,
            reminder_date=reminder_date
        )

        # Save to database
        db.session.add(new_reminder)
        db.session.commit()

        return jsonify({'message': 'Reminder created successfully!'}), 201
    
@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    user_id = current_user.id
    reminders = Reminder.query.filter_by(user_id=user_id).all()

    # Convert reminders to a list of dictionaries
    reminders_list = [reminder.to_dict() for reminder in reminders]

    return jsonify(reminders_list), 200
