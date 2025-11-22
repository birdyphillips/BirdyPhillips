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
        if 'files' not in request.files:
            flash('No files selected', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        
        if not files or all(f.filename == '' for f in files):
            flash('No files selected', 'error')
            return redirect(request.url)
        
        uploaded_files = []
        total_size = 0
        errors = []
        
        for file in files:
            if file.filename == '':
                continue
                
            if file and allowed_file(file.filename):
                try:
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
                    
                    uploaded_files.append({
                        'filename': filename,
                        'original_filename': original_filename,
                        'size': file_size
                    })
                    total_size += file_size
                except Exception as e:
                    errors.append(f"{file.filename}: {str(e)}")
            else:
                errors.append(f"{file.filename}: Invalid file type")
        
        # Commit all uploads
        if uploaded_files:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f'Database error: {str(e)}', 'error')
                return redirect(request.url)
        
        # Show results
        if uploaded_files:
            if len(uploaded_files) == 1:
                # Single file - redirect to splash page
                return redirect(url_for('media.upload_success', filename=uploaded_files[0]['filename']))
            else:
                # Multiple files - redirect to multi-upload success page
                filenames = ','.join([f['filename'] for f in uploaded_files])
                return redirect(url_for('media.upload_success_multi', filenames=filenames, count=len(uploaded_files), total_size=total_size))
        
        if errors:
            flash('Upload errors: ' + '; '.join(errors), 'error')
            
        if not uploaded_files:
            flash('No files were uploaded successfully', 'error')
            
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


@media.route('/upload/success/multi')
def upload_success_multi():
    """Show multi-upload success page."""
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    filenames_str = request.args.get('filenames', '')
    count = request.args.get('count', 0, type=int)
    total_size = request.args.get('total_size', 0, type=int)
    
    if not filenames_str:
        flash('No files uploaded', 'error')
        return redirect(url_for('main.admin_dashboard'))
    
    filenames = filenames_str.split(',')
    
    # Get media info from database
    uploaded_images = []
    for filename in filenames:
        media_item = Media.query.filter_by(filename=secure_filename(filename)).first()
        if media_item:
            uploaded_images.append({
                'filename': media_item.filename,
                'original_filename': media_item.original_filename,
                'file_size': format_file_size(media_item.file_size),
                'file_type': media_item.file_type.upper()
            })
    
    return render_template('upload_success_multi.html',
                         images=uploaded_images,
                         count=count,
                         total_size=format_file_size(total_size))


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
