"""Flask application factory."""
import os
from flask import Flask, render_template

from config import config
from app.extensions import db


def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main, auth, media, api, blog
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(media)
    app.register_blueprint(api)
    app.register_blueprint(blog)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', error_code=404, 
                             error_message='Page not found'), 404

    @app.errorhandler(413)
    def too_large(e):
        from flask import flash, redirect, url_for
        flash('File too large! Maximum size is 50MB.', 'error')
        return redirect(url_for('media.upload'))

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html', error_code=500, 
                             error_message='Internal server error'), 500
    
    # Register template filters
    from app.utils import format_file_size
    
    @app.template_filter('filesize')
    def filesize_filter(size_bytes):
        return format_file_size(size_bytes)
    
    # Register CLI commands
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print("Database tables created.")

    @app.cli.command()
    def create_admin():
        """Create admin user."""
        from app.models import User
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists!")
            return
        
        admin = User(username=username, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully!")
    
    # Ensure upload directory exists
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Create tables if they don't exist
        db.create_all()
        
        # Create default admin if no users exist
        from app.models import User
        if User.query.count() == 0:
            default_admin = User(username='admin', is_admin=True)
            default_admin.set_password('Andre4301$$')
            db.session.add(default_admin)
            db.session.commit()
            print("Default admin user created: admin / Andre4301$$")
    
    return app
