#!/bin/bash

# Update package lists
sudo apt update

# Install Python3 and pip3 if they are not installed
sudo apt install -y python3 python3-pip

# Install Flask and its dependencies
pip3 install Flask Flask-Login Flask-Limiter Werkzeug bcrypt

# Install SQLite3 (if not already installed)
sudo apt install -y sqlite3

# Install any other required packages as needed
# Uncomment and add any additional packages here
# pip3 install <package_name>

echo "All required packages have been installed."
