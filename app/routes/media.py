"""Media upload and management routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app.extensions import db
from app.models import Media
from app.utils import allowed_file, format_file_size

media = Blueprint('media', __name__)


@media.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload new images."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first to upload images.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            original_filename = file.filename
            filename = secure_filename(file.filename)
            
            # Check if filename already exists in database
            existing_media = Media.query.filter_by(filename=filename).first()
            if existing_media:
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{name}_{timestamp}{ext}"
            
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get file info
            file_size = os.path.getsize(filepath)
            file_type = filename.rsplit('.', 1)[1].lower()
            
            # Save to database
            new_media = Media(
                filename=filename,
                original_filename=original_filename,
                file_type=file_type,
                file_size=file_size,
                uploaded_by=session.get('username')
            )
            db.session.add(new_media)
            db.session.commit()
            
            # Redirect to splash page with uploaded image info
            return redirect(url_for('media.upload_success', filename=filename))
        else:
            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP, BMP', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')


@media.route('/upload/success/<filename>')
def upload_success(filename):
    """Show upload success splash page."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    # Get media info from database
    media_item = Media.query.filter_by(filename=secure_filename(filename)).first()
    
    if not media_item:
        flash('Image not found', 'error')
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('upload_success.html', 
                         filename=media_item.filename,
                         original_filename=media_item.original_filename,
                         file_size=format_file_size(media_item.file_size),
                         file_type=media_item.file_type.upper(),
                         upload_time=media_item.upload_time.strftime('%B %d, %Y at %I:%M %p'))


@media.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    """Delete an image."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first to delete images.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Find in database
        media_item = Media.query.filter_by(filename=secure_filename(filename)).first()
        
        if media_item:
            # Delete physical file
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], media_item.filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Delete from database
            file_size = media_item.file_size
            db.session.delete(media_item)
            db.session.commit()
            
            flash(f'✓ "{filename}" deleted successfully ({format_file_size(file_size)} freed)', 'success')
        else:
            flash('Image not found in database', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting image: {str(e)}', 'error')
    
    return redirect(url_for('main.home'))


@media.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
