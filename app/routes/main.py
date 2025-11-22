"""Main application routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app.extensions import db
from app.models import Media
from app.utils import allowed_file, format_file_size

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Home page with image gallery."""
    # Get all media from database, ordered by newest first
    media_list = Media.query.order_by(Media.upload_time.desc()).all()
    
    # Build image data list
    images = []
    image_data = []
    total_size = 0
    
    from flask import current_app
    for media in media_list:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], media.filename)
        if os.path.exists(filepath):
            images.append(media.filename)
            image_data.append({
                'name': media.filename,
                'size': media.file_size,
                'size_mb': round(media.file_size / (1024 * 1024), 2),
                'modified': media.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': media.upload_time.timestamp()
            })
            total_size += media.file_size
    
    return render_template('index.html', 
                         images=images,
                         image_data=image_data,
                         total_images=len(images),
                         total_size=format_file_size(total_size))


@main.route('/sync')
def sync_filesystem():
    """Admin route to sync filesystem with database."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    from flask import current_app
    try:
        # Get all files from uploads folder
        files_in_folder = [f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) 
                          if allowed_file(f)]
        
        # Get all files from database
        files_in_db = [m.filename for m in Media.query.all()]
        
        added = 0
        # Add missing files to database
        for filename in files_in_folder:
            if filename not in files_in_db:
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file_size = os.path.getsize(filepath)
                file_type = filename.rsplit('.', 1)[1].lower()
                
                new_media = Media(
                    filename=filename,
                    original_filename=filename,
                    file_type=file_type,
                    file_size=file_size,
                    uploaded_by='system'
                )
                db.session.add(new_media)
                added += 1
        
        db.session.commit()
        flash(f'✓ Sync complete! Added {added} files to database.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Sync error: {str(e)}', 'error')
    
    return redirect(url_for('main.home'))
