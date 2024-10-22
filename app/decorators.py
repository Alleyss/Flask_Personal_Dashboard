from flask import redirect, url_for, flash
from flask_login import current_user

def login_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You need to login first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap
