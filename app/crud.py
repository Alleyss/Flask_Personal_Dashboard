from .models import Task, Finance, Diary, Habit, Progress
from . import db

def add_task(task, user_id):
    new_task = Task(task=task, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

def get_tasks(user_id):
    return Task.query.filter_by(user_id=user_id).all()

# Add more CRUD functions for other models
