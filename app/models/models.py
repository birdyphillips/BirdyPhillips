"""Database models for BirdyPhillips application."""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    """User model for authentication."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hash and set the password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Media(db.Model):
    """Media model for uploaded images."""
    
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    original_filename = db.Column(db.String(255))
    file_type = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.String(80))
    
    def __repr__(self):
        return f'<Media {self.filename}>'
