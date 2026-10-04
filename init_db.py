"""
init_db.py
----------
Run this ONCE (or any time you want a fresh database) to create the
SQLite tables defined in database/models.py.

Usage:
    python init_db.py
"""

from app import create_app
from database.database import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully at instance/resume_analyzer.db")
