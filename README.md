# BirdyPhillips Image Gallery

A professional Flask-based image gallery application with MySQL backend, user authentication, media management, and modern responsive design. Built following Flask best practices with modular architecture and blueprint-based routing.

**Live Site**: [https://birdyphillips.com](https://birdyphillips.com)

## Features

- 📸 **Image Gallery**: Beautiful grid layout with responsive design
- 🎬 **Auto-playing Slideshow**: Smooth transitions with lazy loading
- 🔐 **Admin Authentication**: Secure login system with password hashing
- ⬆️ **Image Upload**: Support for PNG, JPG, JPEG, GIF, WEBP, BMP (up to 50MB)
- 🗑️ **Image Management**: Delete and organize images with admin controls
- 📱 **Mobile Responsive**: Optimized for all devices and screen sizes
- 🗄️ **MySQL Database**: Persistent storage with SQLAlchemy ORM
- ⚡ **Performance**: Lazy loading, nginx caching, optimized delivery
- 🔒 **Security**: HTTPS, secure sessions, password hashing, input validation
- 🏗️ **Modular Architecture**: Flask blueprints, application factory pattern
- 🔄 **File Sync**: Automatic sync between filesystem and database
- 📊 **Statistics API**: RESTful endpoints for gallery data

## Project Structure (Flask Best Practices)

```
BirdyPhillips/
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
│
├── config/                     # Configuration files
│   ├── __init__.py
│   └── config.py              # App configuration (dev/prod)
│
├── app/                       # Main application package
│   ├── __init__.py           # App factory
│   ├── extensions.py         # Flask extensions (SQLAlchemy)
│   │
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   └── models.py         # User and Media models
│   │
│   ├── routes/               # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py          # Home and sync routes
│   │   ├── auth.py          # Login/logout routes
│   │   ├── media.py         # Upload/delete/serve routes
│   │   └── api.py           # API endpoints
│   │
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py       # File validation, formatting
│   │
│   ├── static/               # Static assets (CSS, JS)
│   ├── templates/            # Jinja2 templates
│   ├── uploads/              # User uploaded images
│   └── instance/             # Instance-specific data (database)
│
├── deploy/                    # Deployment configurations
│   ├── birdyphillips.service # Systemd service
│   ├── nginx_birdyphillips_updated.conf
│   └── README_SSL.md
│
└── tests/                     # Unit and integration tests
```

## Installation

### Prerequisites

- Python 3.9+
- MySQL Server
- nginx (for production)
- Git

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/birdyphillips/BirdyPhillips.git
   cd BirdyPhillips
   ```

2. **Install dependencies**:
   ```bash
   ./install_requirements.sh
   # or manually:
   pip3 install -r requirements.txt
   ```

3. **Configure database** (update `config/config.py` if needed):
   - Default: MySQL at `localhost/birdyphillips`
   - Update connection string in config file

4. **Run the application**:
   ```bash
   python3 run.py
   ```

5. **Access the application**:
   - Development: `http://localhost:5000`
   - Production: `https://birdyphillips.com`

## Configuration

Environment variables (optional, defaults in `config/config.py`):

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_SECRET` | Secret key for session management | `dev_secret_change_in_production` |
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://user:pass@localhost/birdyphillips` |
| `FLASK_ENV` | Environment (`development` or `production`) | `development` |
| `PORT` | Server port | `5000` |

**Default Admin Credentials**:
- Username: `admin`
- Password: `Andre4301$$`

⚠️ **Change these immediately in production!**

## Usage

### Admin Functions

**Login**: Click "Admin" → Enter credentials → Login

**Upload Images**:
1. Login as admin
2. Click "Upload" button
3. Select image file (PNG, JPG, JPEG, GIF, WEBP, BMP)
4. Upload (automatically saved to database)

**Delete Images**:
1. Login as admin
2. Hover over image in gallery
3. Click "Delete" button
4. Confirm deletion

**Sync Filesystem**: Visit `/sync` to sync physical files with database

### API Endpoints

- `GET /` - Home page (gallery)
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /logout` - Logout user
- `GET /upload` - Upload page
- `POST /upload` - Upload image
- `POST /delete/<filename>` - Delete image
- `GET /uploads/<filename>` - Serve uploaded image
- `GET /api/stats` - Gallery statistics (JSON)
- `GET /sync` - Sync filesystem with database

## Production Deployment

### Systemd Service

1. **Copy and configure service**:
   ```bash
   sudo cp deploy/birdyphillips.service /etc/systemd/system/
   sudo systemctl daemon-reload
   ```

2. **Manage service**:
   ```bash
   sudo systemctl start birdyphillips    # Start
   sudo systemctl stop birdyphillips     # Stop
   sudo systemctl restart birdyphillips  # Restart
   sudo systemctl status birdyphillips   # Check status
   ```

3. **View logs**:
   ```bash
   sudo journalctl -u birdyphillips.service -f
   # or use alias: birdylogs
   ```

### Nginx Configuration

1. **Install nginx config**:
   ```bash
   sudo cp deploy/nginx_birdyphillips_updated.conf /etc/nginx/sites-available/birdyphillips
   sudo ln -s /etc/nginx/sites-available/birdyphillips /etc/nginx/sites-enabled/
   ```

2. **Test and reload**:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

3. **SSL Setup**: See `deploy/README_SSL.md` for Let's Encrypt configuration

## Architecture

This application follows Flask best practices:

1. **Application Factory Pattern**: Configurable app creation in `app/__init__.py`
2. **Blueprints**: Modular route organization (main, auth, media, api)
3. **Configuration Objects**: Environment-specific configs in `config/`
4. **Extensions**: Centralized initialization (SQLAlchemy in `extensions.py`)
5. **Models**: Separate database models in `app/models/`
6. **Utils**: Reusable helper functions in `app/utils/`

## Security Features

- ✅ Password hashing with Werkzeug
- ✅ Secure session cookies (HTTPOnly, SameSite)
- ✅ HTTPS with Let's Encrypt SSL
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Secure filename handling
- ✅ File upload validation
- ✅ HSTS headers
- ✅ Input sanitization

## CLI Commands

```bash
# Initialize database
flask init-db

# Create new admin user
flask create-admin
```

## Development

### Running Tests
```bash
cd tests/
pytest
```

### Code Style
```bash
# Format code
black .

# Lint
flake8 app/
```

## Maintenance

### Backup Database
```bash
mysqldump -u birdyphillips -p birdyphillips > backup_$(date +%Y%m%d).sql
```

### Clean Python Cache
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Update Dependencies
```bash
pip3 install -r requirements.txt --upgrade
```

## Troubleshooting

**Service not starting**:
```bash
sudo systemctl status birdyphillips
sudo journalctl -u birdyphillips.service -n 50
```

**Database connection errors**:
- Check MySQL is running: `sudo systemctl status mysql`
- Verify credentials in `config/config.py`
- Test connection: `mysql -u birdyphillips -p`

**Nginx errors**:
```bash
sudo nginx -t                    # Test config
sudo systemctl status nginx      # Check status
sudo tail -f /var/log/nginx/error.log
```

**Permission issues**:
```bash
sudo chown -R pi:www-data /home/pi/Projects/BirdyPhillips/app/uploads/
chmod 755 /home/pi/Projects/BirdyPhillips/app/uploads/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

Private project © 2025 BirdyPhillips. All rights reserved.

## Contact

- **Website**: [https://birdyphillips.com](https://birdyphillips.com)
- **GitHub**: [birdyphillips/BirdyPhillips](https://github.com/birdyphillips/BirdyPhillips)

---

Built with ❤️ using Flask • Hosted on Raspberry Pi
