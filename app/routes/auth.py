"""Authentication routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_admin:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user.id
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session.permanent = False
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    """Logout admin."""
    username = session.get('username', 'Admin')
    session.clear()
    flash(f'Goodbye {username}!', 'success')
    return redirect(url_for('main.home'))
