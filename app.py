from flask import Flask, request, redirect, url_for, render_template
from photo_routes import photo_bp  # Import the photo routes blueprint
from about import about_bp
import os

app = Flask(__name__)

# Stronger secret key, using environment variables
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_fallback_secret_key')

# Define the upload folder at the application level
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads') 

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Register the blueprints
app.register_blueprint(photo_bp, url_prefix='/photos')
app.register_blueprint(about_bp)

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
    images = os.listdir(image_folder)  # List all files in the uploads directory
    return render_template('home.html', images=images)

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

@app.route('/blog')
def blog():
    """Render the blog page."""
    return render_template('blog.html')

@app.route('/news')
def news():
    """Render the news page."""
    return render_template('news.html')

@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')

@app.route('/training')
def training():
    """Render the training page."""
    return render_template('training.html')

@app.route('/services')
def services():
    """Render the services page."""
    return render_template('services.html')

@app.route('/networks')
def networks():
    """Render the networks page."""
    return render_template('networks.html')

@app.route('/testing-center')
def testing_center():
    """Render the testing center page."""
    return render_template('testing_center.html')

@app.route('/blog/post-1')
def post_1():
    """Render the first blog post."""
    return render_template('post-1.html')

@app.route('/blog/post-2')
def post_2():
    """Render the second blog post."""
    return render_template('post-2.html')

@app.route('/blog/post-3')
def post_3():
    return render_template('post-3.html')  # Render the post-3.html template

if __name__ == '__main__':
    # Make sure the app runs in debug mode for development, can switch off for production
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode)
