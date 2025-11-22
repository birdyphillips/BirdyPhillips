# BirdyPhillips Image Gallery

A modern Flask-based image gallery with slideshow functionality, admin authentication, and responsive design.

## Features

- 📸 **Image Gallery**: Grid layout with responsive design
- 🎬 **Auto-playing Slideshow**: 5-second transitions between images
- 🔐 **Admin Authentication**: Secure login system for image management
- ⬆️ **Image Upload**: Support for PNG, JPG, JPEG, GIF, and WEBP (up to 50MB)
- 🗑️ **Image Management**: Delete images when logged in as admin
- 📱 **Mobile Responsive**: Works seamlessly on all devices
- ⚡ **Performance**: Lazy loading images, optimized CSS
- 🔒 **Security**: Environment-based secrets, secure session cookies, CSRF protection

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone or navigate to the project**:
   ```bash
   cd /home/pi/projects/birdyphillips
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set environment variables** (create a `.env` file or export):
   ```bash
   export FLASK_SECRET="your-secure-random-secret-key"
   export ADMIN_USERNAME="admin"
   export ADMIN_PASSWORD="your-secure-password"
   export FLASK_ENV="development"  # or "production"
   export FLASK_DEBUG="1"  # or "0" for production
   export PORT="5000"
   ```

4. **Run the application**:
   ```bash
   python3 app.py
   ```

5. **Access the application**:
   - Open browser to `http://localhost:5000`
   - Or from network: `http://your-ip-address:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_SECRET` | Secret key for session management | `dev_secret_change_in_production` |
| `ADMIN_USERNAME` | Admin username for login | `admin` |
| `ADMIN_PASSWORD` | Admin password | `changeme` |
| `FLASK_ENV` | Environment (`development` or `production`) | `development` |
| `FLASK_DEBUG` | Enable debug mode (`1` or `0`) | `1` |
| `PORT` | Port to run the application | `5000` |

## Usage

### Uploading Images

1. Click "Admin Login" (if not already logged in)
2. Enter admin credentials
3. Click "Upload Image"
4. Select an image file (PNG, JPG, JPEG, GIF, or WEBP)
5. Click "Upload Image"

### Deleting Images

1. Login as admin
2. Hover over any image in the gallery
3. Click the "Delete" button
4. Confirm deletion

### Viewing Gallery

- Images are displayed in a grid layout
- Slideshow plays automatically at the top
- Images are sorted by upload time (newest first)
- Click on images to view full size (in browser)

## Project Structure

```
birdyphillips/
├── app.py                  # Main Flask application
├── routes.py              # Additional API routes (optional blueprint)
├── models.py              # Database models (User, Media)
├── auth.py                # Authentication helpers (if needed)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Gallery homepage
│   ├── login.html        # Admin login page
│   ├── upload.html       # Image upload page
│   └── dashboard.html    # Admin dashboard (future)
├── static/               # Static assets
│   └── styles.css        # CSS styles
├── uploads/              # Uploaded images (auto-created)
└── deploy/               # Deployment configurations
    ├── birdyphillips.service    # systemd service
    ├── nginx_birdyphillips.conf # nginx config
    └── README_SSL.md            # SSL setup guide
```

## Production Deployment

### Using systemd

1. **Copy the service file**:
   ```bash
   sudo cp deploy/birdyphillips.service /etc/systemd/system/
   ```

2. **Edit the service file** with your settings:
   ```bash
   sudo nano /etc/systemd/system/birdyphillips.service
   ```

3. **Set environment variables** in the service file:
   ```ini
   Environment="FLASK_SECRET=your-production-secret"
   Environment="ADMIN_PASSWORD=your-secure-password"
   Environment="FLASK_ENV=production"
   Environment="FLASK_DEBUG=0"
   ```

4. **Enable and start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable birdyphillips
   sudo systemctl start birdyphillips
   sudo systemctl status birdyphillips
   ```

### Using nginx

1. **Copy nginx config**:
   ```bash
   sudo cp deploy/nginx_birdyphillips.conf /etc/nginx/sites-available/birdyphillips
   sudo ln -s /etc/nginx/sites-available/birdyphillips /etc/nginx/sites-enabled/
   ```

2. **Test and reload nginx**:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Security Recommendations

- [ ] Change default admin password immediately
- [ ] Use a strong, random `FLASK_SECRET` (32+ characters)
- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=0` in production
- [ ] Use HTTPS (see `deploy/README_SSL.md`)
- [ ] Implement rate limiting for login attempts
- [ ] Regular backups of `uploads/` directory
- [ ] Consider implementing Flask-WTF for CSRF protection

## Future Enhancements

- [ ] Database-backed user management (use `models.py`)
- [ ] Image compression and thumbnail generation
- [ ] Pagination for large galleries
- [ ] Image tagging and search
- [ ] Bulk upload
- [ ] Image metadata (EXIF) display
- [ ] Social sharing features
- [ ] API endpoints for mobile apps

## Troubleshooting

**Port already in use**:
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill it or use a different port
export PORT=8080
```

**Permission denied on uploads**:
```bash
sudo chown -R $USER:$USER uploads/
chmod 755 uploads/
```

**Module not found errors**:
```bash
pip3 install -r requirements.txt --upgrade
```

## License

Private project. All rights reserved.

## Support

For issues or questions, contact the development team.
