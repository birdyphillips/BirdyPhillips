import os
from flask import Blueprint, render_template

slideshow_bp = Blueprint('slideshow', __name__)

def get_images():
    image_folder = 'uploads'  # Adjust the path if needed
    if not os.path.exists(image_folder):
        print(f"Directory '{image_folder}' does not exist.")
        return []  # Return an empty list if the directory does not exist
    images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found images: {images}")  # Debug output
    return images

@slideshow_bp.route('/slideshow')
def show_slideshow():
    images = get_images()
    return render_template('slideshow.html', images=images)
