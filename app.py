"""
app.py
------
Main Flask application entry point.

This file owns:
- App creation & configuration
- User authentication (register / login / logout) via Flask-Login
- Resume upload handling
- Calling Member 2's parser and Member 3's ML matcher
- Saving results to the database
- Rendering templates built by Member 4

INTEGRATION CONTRACT (do not change without telling the whole team):
    resume_data = parse_resume(file)              # from resume_parser package
    result = analyze_resume(resume_data["raw_text"], job_description)  # from ml package

    resume_data -> dict with keys: raw_text, name, email, phone, skills, education, experience
    result      -> dict with keys: match_score, matched_skills, missing_skills, recommendation
"""

import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from werkzeug.utils import secure_filename

from config import Config
from database.database import db, init_db
from database.models import User, Analysis

# These come from the other two members' modules.
# The app will raise an ImportError until those files exist --
# that's expected during parallel development.
from resume_parser.pdf_parser import parse_resume
from ml.predict import analyze_resume


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure instance folders exist before anything tries to write to them
    os.makedirs(os.path.join(Config.BASE_DIR, "instance"), exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    init_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    register_routes(app)
    return app


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


def register_routes(app):

    # ---------------------------------------------------------------
    # PUBLIC PAGES
    # ---------------------------------------------------------------

    @app.route("/")
    def index():
        return render_template("index.html")

    # ---------------------------------------------------------------
    # AUTH
    # ---------------------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("analyzer"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not name or not email or not password:
                flash("All fields are required.", "danger")
                return redirect(url_for("register"))

            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                return redirect(url_for("register"))

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("An account with this email already exists.", "danger")
                return redirect(url_for("register"))

            new_user = User(name=name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("analyzer"))

        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                login_user(user)
                flash(f"Welcome back, {user.name}!", "success")
                return redirect(url_for("analyzer"))

            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    # ---------------------------------------------------------------
    # CORE FEATURE: UPLOAD + ANALYZE
    # ---------------------------------------------------------------

    @app.route("/analyzer", methods=["GET"])
    @login_required
    def analyzer():
        return render_template("analyzer.html")

    @app.route("/analyze", methods=["POST"])
    @login_required
    def analyze():
        job_description = request.form.get("job_description", "").strip()
        resume_file = request.files.get("resume")

        if not job_description:
            flash("Please paste a job description.", "danger")
            return redirect(url_for("analyzer"))

        if not resume_file or resume_file.filename == "":
            flash("Please upload a resume PDF.", "danger")
            return redirect(url_for("analyzer"))

        if not allowed_file(resume_file.filename):
            flash("Only PDF files are supported.", "danger")
            return redirect(url_for("analyzer"))

        # Save the uploaded file temporarily
        safe_name = secure_filename(resume_file.filename)
        timestamped_name = f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{safe_name}"
        save_path = os.path.join(Config.UPLOAD_FOLDER, timestamped_name)
        resume_file.save(save_path)

        try:
            # ---- MEMBER 2's function ----
            resume_data = parse_resume(save_path)

            # ---- MEMBER 3's function ----
            result = analyze_resume(resume_data["raw_text"], job_description)

        except Exception as e:
            flash(f"Something went wrong while analyzing the resume: {e}", "danger")
            return redirect(url_for("analyzer"))
        finally:
            # Clean up the uploaded file — we only need the extracted text/result
            if os.path.exists(save_path):
                os.remove(save_path)

        # Save the analysis to history
        new_analysis = Analysis(
            user_id=current_user.id,
            resume_name=safe_name,
            job_description=job_description,
            match_score=result["match_score"],
            matched_skills=Analysis.skills_to_string(result["matched_skills"]),
            missing_skills=Analysis.skills_to_string(result["missing_skills"]),
            recommendation=result["recommendation"],
            candidate_name=resume_data.get("name"),
            candidate_email=resume_data.get("email"),
            candidate_phone=resume_data.get("phone"),
            education=Analysis.lines_to_string(resume_data.get("education", [])),
            experience=Analysis.lines_to_string(resume_data.get("experience", [])),
        )
        db.session.add(new_analysis)
        db.session.commit()

        return redirect(url_for("results", analysis_id=new_analysis.id))

    # ---------------------------------------------------------------
    # RESULTS & HISTORY
    # ---------------------------------------------------------------

    @app.route("/results/<int:analysis_id>")
    @login_required
    def results(analysis_id):
        analysis = db.session.get(Analysis, analysis_id)

        if analysis is None or analysis.user_id != current_user.id:
            abort(404)

        return render_template("results.html", analysis=analysis)

    @app.route("/history")
    @login_required
    def history():
        analyses = (
            Analysis.query.filter_by(user_id=current_user.id)
            .order_by(Analysis.created_at.desc())
            .all()
        )
        return render_template("history.html", analyses=analyses)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
