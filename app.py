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
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')  # Your blog page

@app.route('/news')
def news():
    return render_template('news.html')  # Render the news.html template

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Render the contact.html template

@app.route('/training')
def training():
    return render_template('training.html')  # Render the training.html template

@app.route('/services')
def services():
    return render_template('services.html')  # Render the services.html template

@app.route('/networks')
def networks():
    return render_template('networks.html')  # Render the networks.html template

@app.route('/testing-center')
def testing_center():
    return render_template('testing_center.html')  # Render the testing_center.html template

@app.route('/blog/post-1')
def post_1():
    return render_template('post-1.html')  # Render the post-1.html template

@app.route('/blog/post-2')
def post_2():
    return render_template('post-2.html')  # Render the post-2.html template

@app.route('/blog/post-3')
def post_3():
    return render_template('post-3.html')  # Render the post-3.html template


if __name__ == '__main__':
    # Make sure the app runs in debug mode for development, can switch off for production
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode)
