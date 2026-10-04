"""
database/models.py
-------------------
Defines the two database tables used by the app:

1. User      -> registered accounts (password stored as a hash, never plain text)
2. Analysis  -> one row per resume-vs-JD analysis a user has run (history)

Both models use Flask-SQLAlchemy's declarative style.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user can have many analyses (one-to-many relationship)
    analyses = db.relationship(
        "Analysis",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        """Hashes and stores the password. Never store plain text."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """Verifies a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.email}>"


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    resume_name = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)

    match_score = db.Column(db.Float, nullable=False)

    # Stored as comma-separated strings since SQLite has no native array type.
    # Converted to/from Python lists using the helper properties below.
    matched_skills = db.Column(db.Text, default="")
    missing_skills = db.Column(db.Text, default="")

    recommendation = db.Column(db.String(100), nullable=False)

    # Parsed resume info (from Member 2's parse_resume output), stored here
    # so the results/history pages can display "Resume Information" without
    # needing to re-parse the PDF (which is deleted right after analysis).
    candidate_name = db.Column(db.String(150), nullable=True)
    candidate_email = db.Column(db.String(150), nullable=True)
    candidate_phone = db.Column(db.String(50), nullable=True)
    # education / experience are lists of lines -> stored newline-separated
    education = db.Column(db.Text, default="")
    experience = db.Column(db.Text, default="")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---- Convenience helpers so routes/templates work with real lists ----

    @property
    def matched_skills_list(self):
        return [s.strip() for s in self.matched_skills.split(",") if s.strip()]

    @property
    def missing_skills_list(self):
        return [s.strip() for s in self.missing_skills.split(",") if s.strip()]

    @property
    def education_list(self):
        return [line.strip() for line in self.education.split("\n") if line.strip()]

    @property
    def experience_list(self):
        return [line.strip() for line in self.experience.split("\n") if line.strip()]

    @staticmethod
    def skills_to_string(skills_list):
        """Converts a Python list of skills into the comma-separated string
        format used for storage. Used when SAVING a new Analysis row."""
        return ", ".join(skills_list) if skills_list else ""

    @staticmethod
    def lines_to_string(lines_list):
        """Converts a Python list of lines (education/experience entries)
        into the newline-separated string format used for storage."""
        return "\n".join(lines_list) if lines_list else ""

    def __repr__(self):
        return f"<Analysis {self.id} user={self.user_id} score={self.match_score}>"
