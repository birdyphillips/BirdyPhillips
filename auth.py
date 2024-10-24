import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from extensions import db, login_manager  # Import the existing SQLAlchemy and LoginManager instances
from forms import LoginForm, RegistrationForm  # Import the forms from forms.py

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == register_form.username.data) | (User.email == register_form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            logger.warning(f"Attempt to register with existing username or email: {register_form.username.data}, {register_form.email.data}")
        else:
            user = User(username=register_form.username.data, email=register_form.email.data)
            user.set_password(register_form.password.data)
            db.session.add(user)
            try:
                db.session.commit()
                flash('Registration successful. Please log in.', 'success')
                logger.info(f"User registered: {user.username}")
                return redirect(url_for('auth.login'))
            except IntegrityError as e:
                db.session.rollback()
                flash('An error occurred during registration. Please try again.', 'danger')
                logger.error(f"IntegrityError during registration: {e}")
    return render_template('register.html', form=register_form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash('Login successful.', 'success')
            logger.info(f"User logged in: {user.username}")
            return redirect(url_for('photos'))  # Redirect to photos after login
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
            logger.warning(f"Failed login attempt for email: {login_form.email.data}")
    return render_template('login.html', login_form=login_form, register_form=RegistrationForm())

@auth_bp.route('/logout')
@login_required
def logout():
    logger.info(f"User logged out: {current_user.username}")
    logout_user()
    return redirect(url_for('auth.login'))  # Redirect to login page after logout