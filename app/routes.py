# routes.py

import os
from flask import render_template, request, session, redirect, url_for, send_from_directory
from app.planner import generate_study_plan, generate_pdf
from app.utils import sanitize_input, validate_date

print("Registering routes...")  # Debug log

# Ensure this file does not redefine 'app' — it should come from __init__.py
from app import app

# Define export directory
EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

@app.route("/")
def home():
    print("Home route triggered")
    return render_template("home.html")

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    print("Form submitted!")  # This should appear in terminal
    exam_date = sanitize_input(request.form.get("exam_date"))
    subjects = sanitize_input(request.form.get("subjects"))
    hours_per_day = int(request.form.get("hours_per_day", 2))
    intensity = sanitize_input(request.form.get("intensity"))

    valid, msg = validate_date(exam_date)
    if not valid:
        return render_template("home.html", error=msg)

    if not subjects:
        return render_template("home.html", error="Please enter at least one subject.")

    try:
        study_plan = generate_study_plan(subjects, exam_date, hours_per_day, intensity)
        session['study_plan'] = study_plan
        return render_template("result.html", study_plan=study_plan)
    except Exception as e:
        return render_template("home.html", error=str(e))

@app.route("/download-pdf")
def download_pdf():
    study_plan = session.get('study_plan')
    if not study_plan:
        return redirect(url_for("home"))

    filename = "study_plan.pdf"
    exports_dir = os.path.join(os.getcwd(), "exports")
    os.makedirs(exports_dir, exist_ok=True)  # Ensure exports folder exists
    filepath = os.path.join(exports_dir, filename)

    # Generate PDF only if it doesn't exist, or always regenerate
    generate_pdf(study_plan, filename)  # Make sure this writes to exports/

    return send_from_directory(directory=exports_dir, path=filename, as_attachment=True)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404: Page Not Found</h1>", 404