"""Main entry point for BirdyPhillips application."""
import os
from app import create_app

# Determine configuration
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    config_name = 'production'
else:
    config_name = 'development'

# Create application
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = config_name == 'development'
    
    print("=" * 60)
    print("BirdyPhillips Image Gallery")
    print("=" * 60)
    print(f"Environment: {config_name}")
    print(f"Server: http://0.0.0.0:{port}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Debug mode: {debug}")
    print("=" * 60)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
