from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.services.cv_analyzer import analyze_cv
from app.services.dashboard import dashboard_data, filtered_jobs, home_snapshot


main = Blueprint("main", __name__)


def allowed_file(filename):
    ext = Path(filename).suffix.lower().replace(".", "")
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@main.route("/")
def index():
    return render_template("index.html", data=home_snapshot())


@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", data=dashboard_data())


@main.route("/jobs")
def jobs():
    city = request.args.get("city", "")
    sector = request.args.get("sector", "")
    jobs_data, filters = filtered_jobs(city, sector)
    return render_template(
        "jobs.html",
        jobs=jobs_data,
        filters=filters,
        selected_city=city,
        selected_sector=sector,
    )


@main.route("/analyzer", methods=["GET", "POST"])
def analyzer():
    result = None

    if request.method == "POST":
        cv_file = request.files.get("cv_file")

        if not cv_file or cv_file.filename == "":
            flash("Please upload your CV first.")
            return redirect(url_for("main.analyzer"))

        if not allowed_file(cv_file.filename):
            flash("Only PDF, DOCX, and TXT files are allowed.")
            return redirect(url_for("main.analyzer"))

        filename = secure_filename(cv_file.filename)
        file_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
        cv_file.save(file_path)
        result = analyze_cv(file_path)

    return render_template("analyzer.html", result=result)


@main.route("/about")
def about():
    return render_template("about.html")
