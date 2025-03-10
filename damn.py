import os
import time
import subprocess
import shutil
import json
from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploaded_projects"
STATIC_PROJECTS_FOLDER = "static_projects"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_PROJECTS_FOLDER, exist_ok=True)


# === Helper Functions ===

def get_lang_percentage(project_folder):
    """Analyzes the project files and calculates the percentage of each language used."""
    file_types = {
        "html": 0, "css": 0, "js": 0, "py": 0
    }
    total_files = 0

    for root, _, files in os.walk(project_folder):
        for file in files:
            ext = file.split(".")[-1].lower()
            if ext in file_types:
                file_types[ext] += 1
                total_files += 1

    if total_files == 0:
        return {}

    return {lang: round((count / total_files) * 100, 2) for lang, count in file_types.items()}


def run_command(command):
    """Executes a shell command and returns success (1) or failure (0)."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return 1 if result.returncode == 0 else 0
    except Exception as e:
        return 0


def run_linters(project_folder):
    """Runs linters on project files and returns a linting summary."""
    lint_results = {"html": None, "css": None, "js": None, "python": None}

    # HTML Lint
    html_files = [os.path.join(root, f) for root, _, files in os.walk(project_folder) for f in files if
                  f.endswith(".html")]
    if html_files:
        lint_results["html"] = run_command(f"htmlhint {' '.join(html_files)}")

    # CSS Lint
    css_files = [os.path.join(root, f) for root, _, files in os.walk(project_folder) for f in files if
                 f.endswith(".css")]
    if css_files:
        lint_results["css"] = run_command(f"stylelint {' '.join(css_files)}")

    # JS Lint
    js_files = [os.path.join(root, f) for root, _, files in os.walk(project_folder) for f in files if f.endswith(".js")]
    if js_files:
        lint_results["js"] = run_command(f"eslint {' '.join(js_files)}")

    # Python Linters
    py_files = [os.path.join(root, f) for root, _, files in os.walk(project_folder) for f in files if f.endswith(".py")]
    if py_files:
        lint_results["python"] = run_command(f"pylint {' '.join(py_files)}")

    return lint_results


def manage_flask_process(project_folder):
    """Starts the Flask app from the uploaded project and ensures it runs properly."""
    env = os.environ.copy()
    env["FLASK_APP"] = os.path.join(project_folder, "app.py")

    # Run Flask app
    process = subprocess.Popen(["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"], cwd=project_folder,
                               env=env)
    time.sleep(2)  # Allow time for the app to start

    return process


# === Flask Routes ===

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_project():
    """Handles file uploads and processes the project."""
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    project_name = request.form.get("project_name")
    if not project_name:
        return jsonify({"error": "Project name is required"}), 400

    project_name = secure_filename(project_name)
    project_folder = os.path.join(UPLOAD_FOLDER, project_name)

    if os.path.exists(project_folder):
        shutil.rmtree(project_folder)  # Remove any previous uploads with the same name

    os.makedirs(project_folder, exist_ok=True)

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(project_folder, filename))

    # Analyze language usage
    lang_stats = get_lang_percentage(project_folder)

    # Run linters
    lint_results = run_linters(project_folder)

    # Check for execution method
    if "app.py" in os.listdir(project_folder):
        process = manage_flask_process(project_folder)
        return jsonify({
            "message": "Flask app is running",
            "preview_url": "http://127.0.0.1:5001",
            "lang_stats": lang_stats,
            "lint_results": lint_results
        })

    elif "index.html" in os.listdir(project_folder):
        static_path = os.path.join(STATIC_PROJECTS_FOLDER, project_name)
        shutil.move(project_folder, static_path)
        return jsonify({
            "message": "Static site is ready",
            "preview_url": f"/preview/{project_name}",
            "lang_stats": lang_stats,
            "lint_results": lint_results
        })

    else:
        return jsonify({"error": "No valid entry point found"}), 400


@app.route("/preview/<project_name>")
def preview_static(project_name):
    """Serves static files for preview."""
    project_path = os.path.join(STATIC_PROJECTS_FOLDER, project_name)
    if not os.path.exists(project_path):
        return jsonify({"error": "Project not found"}), 404

    return send_from_directory(project_path, "index.html")


# === Run Flask App ===
if __name__ == "__main__":
    app.run(debug=True, port=5000)
