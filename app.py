from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the secret key for session management
# Use environment variables for stronger security
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_default_fallback_secret_key')

# Configure the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Configure the upload folder for storing uploaded files
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Initialize the Flask-Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Set the login view for unauthorized users

# Import and register blueprints
from photo_routes import photo_bp  # Import the photo routes blueprint
from about import about_bp  # Import the about routes blueprint
from auth import auth_bp, login_manager as auth_login_manager  # Import the auth blueprint and related instances

# Register the blueprints
app.register_blueprint(photo_bp, url_prefix='/photos')
app.register_blueprint(about_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

# Initialize extensions
auth_login_manager.init_app(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure after-request caching headers
@app.after_request
def add_header(response):
    """
    Add headers to force the browser to always fetch the latest content,
    avoiding cached versions.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Core Routes
@app.route('/')
def home():
    image_folder = 'static/uploads'  # Path to your images
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')  # Render the services.html template

@app.route('/networks')
def networks():
    return render_template('networks.html')  # Render the networks.html template

@app.route('/testing-center')
def testing_center():
    return render_template('testing_center.html')  # Render the testing_center.html template

@app.route('/blog')
def blog():
    return render_template('blog.html')  # Render the blog.html template

@app.route('/blog/post-1')
def post_1():
    return render_template('post-1.html')  # Render the post-1.html template

@app.route('/blog/post-2')
def post_2():
    return render_template('post-2.html')  # Render the post-2.html template

@app.route('/blog/post-3')
def post_3():
    return render_template('post-3.html')  # Render the post-3.html template

@app.route('/training')
def training():
    return render_template('training.html')  # Render the training.html template

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Render the contact.html template

@app.route('/news')
def news():
    return render_template('news.html')  # Render the news.html template

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Make sure the app runs in debug mode for development, can switch off for production
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode)