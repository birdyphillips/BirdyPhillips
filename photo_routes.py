import os
from flask import Blueprint, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = r'/static/uploads'  # Use raw string to handle backslashes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create Blueprint
photo_bp = Blueprint('photo_bp', __name__, template_folder='templates', static_folder='static')

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to display photos
@photo_bp.route('/photos', methods=['GET'])
def show_photos():
    try:
        photo_list = os.listdir(UPLOAD_FOLDER)
        return render_template('photos.html', photos=photo_list)
    except Exception as e:
        flash(f"Error retrieving photos: {str(e)}")
        return render_template('photos.html', photos=[])

# Route to upload photos
@photo_bp.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        flash('No file part')
        return redirect(url_for('photo_bp.show_photos'))

    file = request.files['photo']

    # Check if the file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('photo_bp.show_photos'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Save the file to the specified directory
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        flash('Photo uploaded successfully!')

        # Debugging line to print uploaded files
        print(f'Uploaded files: {os.listdir(UPLOAD_FOLDER)}')  

        return redirect(url_for('photo_bp.show_photos'))
    else:
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('photo_bp.show_photos'))

# Route to delete a photo
@photo_bp.route('/delete/<filename>', methods=['POST'])
def delete_photo(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'Photo {filename} deleted successfully!')
        else:
            flash(f'File {filename} not found!')
    except Exception as e:
        flash(f'Error deleting photo: {str(e)}')
    
    return redirect(url_for('photo_bp.show_photos'))

# Route to serve individual photos
@photo_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route to render the photo gallery as the homepage
@photo_bp.route('/')
def photo_gallery():
    return redirect(url_for('photo_bp.show_photos'))  # Redirect to the photos page

# Route to update a photo
@photo_bp.route('/update/<filename>', methods=['POST'])
def update_photo(filename):
    if 'photo' not in request.files:
        flash('No file part')
        return redirect(url_for('photo_bp.show_photos'))

    file = request.files['photo']

    # Check if the file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('photo_bp.show_photos'))

    if file and allowed_file(file.filename):
        new_filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(file_path):
            # Save the updated file, replacing the old one
            file.save(file_path)
            flash('Photo updated successfully!')
        else:
            flash(f'File {filename} not found! Cannot update.')
    else:
        flash('Invalid file type. Please upload an image file.')

    return redirect(url_for('photo_bp.show_photos'))

