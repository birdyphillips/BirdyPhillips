from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager  # Import the existing SQLAlchemy and LoginManager instances

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Define the login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the user's password
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # Create a new user instance
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        # Flash a success message
        flash('Your account has been created!', 'success')
        # Redirect to the login page
        return redirect(url_for('auth.login'))
    # Render the registration template with the form
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        # Query the database for the user by email
        user = User.query.filter_by(email=form.email.data).first()
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, form.password.data):
            # Log the user in and remember the session
            login_user(user, remember=True)
            # Redirect to the home page after successful login
            return redirect(url_for('home'))
        else:
            # Flash an error message if login is unsuccessful
            flash('Login Unsuccessful. Please check email and password', 'danger')
    # Render the login template with the form
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    # Log the user out
    logout_user()
    # Redirect to the login page after logout
    return redirect(url_for('auth.login'))