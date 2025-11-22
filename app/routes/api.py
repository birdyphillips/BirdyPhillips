"""API routes."""
from flask import Blueprint, jsonify, current_app

from app.extensions import db
from app.models import Media
from app.utils import format_file_size

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/stats')
def stats():
    """API endpoint for gallery statistics."""
    try:
        total_images = Media.query.count()
        total_size = db.session.query(db.func.sum(Media.file_size)).scalar() or 0
        
        return jsonify({
            'success': True,
            'total_images': total_images,
            'total_size': total_size,
            'total_size_formatted': format_file_size(total_size),
            'allowed_formats': list(current_app.config['ALLOWED_EXTENSIONS'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
