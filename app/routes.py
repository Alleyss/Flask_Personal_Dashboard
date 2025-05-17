from flask import Blueprint,render_template, redirect, url_for, flash, request, jsonify,session
from . import db
from .models import User, Task, Finance, Diary, Habit, Progress,Reminder
from werkzeug.security import generate_password_hash, check_password_hash
from .decorators import login_required
from datetime import datetime

bp = Blueprint('routes', __name__)
@bp.route('/')
def index():
    return redirect(url_for('routes.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('routes.login'))

        user = User.query.filter_by(username=username).first()

        #if user is None or not user.check_password(password):
        if user is None or not user.password_hash==password:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('routes.login'))

        # Successful login
        session['user_id'] = user.id
        session['username'] = user.username
        session['logged_in'] = True

        flash("User login successful!", 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password == confirm_password:
           # hashed_password = generate_password_hash(password)
            #new_user = User(username=username, email=email, password_hash=hashed_password)
            new_user = User(username=username, email=email, password_hash=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('routes.login'))
        else:
            flash('Passwords do not match!')
    return render_template('register.html')

@login_required
@bp.route('/dashboard')
def dashboard():
    username=session['username']
    #username=db.execute("SELECT username FROM users WHERE id=?",id)
    return render_template('dashboard.html',username=username)

# Other routes for todolist, finance, diary, etc.
##Calendar
@bp.route('/create_reminder', methods=['POST'])
def create_reminder():
    if request.method == 'POST':
        data = request.get_json()  # Fetch the data sent via JavaScript or a form
        title = data.get('title')
        description = data.get('description', '')
        reminder_date = datetime.strptime(data.get('reminder_date'), '%Y-%m-%d %H:%M:%S')

        # Create new reminder
        new_reminder = Reminder(
            user_id=session['user_id'],
            title=title,
            description=description,
            reminder_date=reminder_date
        )

        # Save to database
        db.session.add(new_reminder)
        db.session.commit()

        return jsonify({'message': 'Reminder created successfully!'}), 201
    
@bp.route('/api/reminders', methods=['GET'])
def get_reminders():
    user_id = session['user_id']
    reminders = Reminder.query.filter_by(user_id=user_id).all()

    # Convert reminders to a list of dictionaries
    reminders_list = [reminder.to_dict() for reminder in reminders]

    return jsonify(reminders_list), 200
