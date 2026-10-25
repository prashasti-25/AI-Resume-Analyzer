"""
config.py
---------
Central configuration for the Flask app.
Keeps all settings (secret key, database path, upload rules) in ONE place
so other members don't need to touch app.py to know these values.
"""

import os

# Absolute path to the project root (folder containing this file)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Exposed so other files (e.g. app.py) can build paths off the project root
    BASE_DIR = BASE_DIR

    # Used by Flask to sign session cookies. In a real deployment this
    # should come from an environment variable, not be hardcoded.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # SQLite database file will be created inside /instance/
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "resume_analyzer.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder where uploaded resume PDFs are temporarily stored
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "instance", "uploads")
    ALLOWED_EXTENSIONS = {"pdf"}

    # Max upload size: 5 MB (prevents huge file uploads crashing the app)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
