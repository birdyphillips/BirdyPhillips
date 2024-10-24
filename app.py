from flask import Flask, request, redirect, url_for, render_template
from extensions import db, login_manager  # Import the existing SQLAlchemy and LoginManager instances
from auth import LoginForm, RegistrationForm  # Import the forms from auth.py
import os

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the SQLAlchemy database instance
db.init_app(app)

# Initialize the Flask-Login manager
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Set the login view for unauthorized users

# Import and register blueprints
from photo_routes import photo_bp  # Import the photo routes blueprint
from about import about_bp  # Import the about routes blueprint
from auth import auth_bp  # Import the auth blueprint

# Register the blueprints
app.register_blueprint(photo_bp, url_prefix='/photos')
app.register_blueprint(about_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegistrationForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            # Handle login logic here
            pass
        elif register_form.validate_on_submit():
            # Handle registration logic here
            pass
    return render_template('login.html', login_form=login_form, register_form=register_form)  # Render the login.html template

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Make sure the app runs in debug mode for development, can switch off for production
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode)