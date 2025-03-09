import os
import subprocess
from flask import Flask, request, jsonify, render_template

# Excluded file extensions and directories
EXCLUDED_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".class", ".o", ".obj", ".so", ".dll", ".dylib", ".exe",
    ".a", ".lib", ".jar", ".war", ".rlib", ".nupkg", ".kt", ".kts", ".scala", ".sbt",
    ".swiftmodule", ".hmap", ".dSYM", ".pm", ".gem", ".rbc",
    ".log", ".trace", ".dmp", ".bak", ".ini", ".cfg", ".toml", ".properties",
    ".lock", ".tmp", ".swp", ".swo", ".old", ".zip", ".tar", ".gz", ".bz2", ".xz",
    ".rar", ".7z", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".mp3", ".wav", ".ogg", ".mp4", ".mkv", ".avi", ".mov",
    ".pdf", ".docx", ".xlsx", ".pptx", ".csv", ".tsv",
    ".db", ".sqlite", ".sqlite3", ".mdb", ".vmdk", ".qcow2", ".vdi", ".iso",
    ".bin", ".dat", ".dump"
}

EXCLUDED_DIRS = {
    ".venv", "env", "node_modules", "vendor", "target", "bin",
    ".git", ".idea", ".vscode", ".metadata", ".gradle", ".mvn",
    ".docker", ".terraform", ".kitchen",
    "CMakeFiles", "build", "dist", "__pycache__"
}

# File categories
file_types = {'.py': [], '.html': [], '.css': [], '.js': []}

app = Flask(__name__, template_folder="templates")
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def collect_files(directory):
    """Scans a directory and filters files based on allowed types."""
    global file_types
    file_types = {'.py': [], '.html': [], '.css': [], '.js': []}

    for root, _, files in os.walk(directory):
        if any(excluded in root for excluded in EXCLUDED_DIRS):
            continue
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in EXCLUDED_EXTENSIONS:
                continue
            file_types.setdefault(ext, []).append(os.path.join(root, file))

def run_command(command, name):
    """Runs a shell command and prints the result."""
    print(f"\n🔍 Running {name}...")
    subprocess.run(command, shell=True)

def run_all_checks():
    """Runs linting tools on the scanned files."""
    if file_types[".py"]:
        run_command("pylint " + " ".join(file_types[".py"]), "Pylint")
        run_command("flake8 " + " ".join(file_types[".py"]), "Flake8")
        run_command("mypy " + " ".join(file_types[".py"]), "Mypy")
        run_command("bandit -r " + " ".join(file_types[".py"]), "Bandit")

    if file_types[".js"]:
        run_command("eslint " + " ".join(file_types[".js"]), "ESLint")

    if file_types[".css"]:
        run_command("stylelint " + " ".join(file_types[".css"]), "StyleLint")

    if file_types[".html"]:
        run_command("htmlhint " + " ".join(file_types[".html"]), "HTMLHint")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_files():
    """Handles folder upload and scans files."""
    directory = request.form.get("directory")

    if not directory or not os.path.isdir(directory):
        return jsonify({"error": "Invalid directory!"}), 400

    print(f"\n🔍 Scanning directory: {directory}...")
    collect_files(directory)
    run_all_checks()

    return jsonify({
        "message": "Scan complete!",
        "files": {ext: len(file_list) for ext, file_list in file_types.items()}
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
