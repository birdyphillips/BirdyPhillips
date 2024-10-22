from flask import Blueprint, render_template, request, redirect, url_for
import os

about_bp = Blueprint('about', __name__)

# Set the upload folder globally
UPLOAD_FOLDER = 'static/images'

@about_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@about_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(url_for('about.about'))  # Redirect if no file is selected
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('about.about'))  # Redirect if no file is selected
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))  # Use the global variable here
        return redirect(url_for('about.about'))  # Redirect back to the About page
