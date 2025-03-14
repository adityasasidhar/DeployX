import os
from src.css_task import run_css_linter
from src.python_tasks import run_mypy, run_bandit, run_pylint, run_command, run_flake8
from src.js_tasks import run_js_linter
from src.html_task import run_htmlhint

def collect_files(directory):
    """

    I added everything within the same function, assuming we don't care much about importing and code throttling

    """
    excluded_extensions = {
        ".pyc", ".pyo", ".pyd", ".class", ".o", ".obj", ".so", ".dll", ".dylib", ".exe",
        ".a", ".lib", ".jar", ".war", ".rlib", ".nupkg", ".kt", ".kts", ".scala", ".sbt",
        ".swiftmodule", ".hmap", ".dSYM", ".pm", ".gem", ".rbc",

        ".log", ".trace", ".dmp", ".bak", ".ini", ".cfg", ".toml", ".properties",
        ".lock", ".tmp", ".swp", ".swo", ".old", ".zip", ".tar", ".gz", ".bz2", ".xz",
        ".rar", ".7z",

        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
        ".mp3", ".wav", ".ogg", ".mp4", ".mkv", ".avi", ".mov",
        ".pdf", ".docx", ".xlsx", ".pptx", ".csv", ".tsv",

        ".db", ".sqlite", ".sqlite3", ".mdb", ".vmdk", ".qcow2", ".vdi", ".iso",
        ".bin", ".dat", ".dump"
    }
    excluded_dirs = {
        ".venv", "env", "node_modules", "vendor", "target", "bin",

        ".git", ".idea", ".vscode", ".metadata", ".gradle", ".mvn",

        ".docker", ".terraform", ".kitchen",

        "CMakeFiles", "build", "dist", "__pycache__"
    }

    file_types = {'.py': [], '.html': [], '.css': [], '.js': []}


    for root, _, files in os.walk(directory):
        if any(excluded in root for excluded in excluded_dirs):
            continue
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in excluded_extensions:
                continue
            file_types.setdefault(ext, []).append(os.path.join(root, file))


def run_all_checks():
    file_types = {'.py': [], '.html': [], '.css': [], '.js': []}
    run_pylint(file_types['.py'])
    run_flake8(file_types['.py'])
    run_mypy(file_types['.py'])
    run_bandit(file_types['.py'])
    run_js_linter(file_types['.js'])
    run_css_linter(file_types['.css'])
    run_htmlhint(file_types['.html'])


