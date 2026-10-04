"""
database/database.py
---------------------
Creates ONE shared SQLAlchemy() instance called `db`.

Why this file exists separately from models.py:
Flask-SQLAlchemy requires `db = SQLAlchemy()` to be created before the
Flask app exists, then "attached" to the app later with db.init_app(app).
Keeping it in its own file avoids circular imports between app.py and
models.py (both of them import `db` from here).
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Attaches the db instance to the Flask app and creates all tables
    if they don't already exist. Called once from app.py at startup.
    """
    db.init_app(app)
    with app.app_context():
        # Import models here (not at top of file) so that SQLAlchemy
        # knows about the User/Analysis tables before create_all() runs.
        from database import models  # noqa: F401
        db.create_all()
