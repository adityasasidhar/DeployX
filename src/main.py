from language_task import *
from css_task import *
from python_tasks import *
from js_tasks import *
from html_task import *
from flask import Flask, request, jsonify

file_types = {'.py': [], '.html': [], '.css': [], '.js': []}

EXCLUDED_EXTENSIONS = {
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

EXCLUDED_DIRS = {
    ".venv", "env", "node_modules", "vendor", "target", "bin",

    ".git", ".idea", ".vscode", ".metadata", ".gradle", ".mvn",

    ".docker", ".terraform", ".kitchen",

    "CMakeFiles", "build", "dist", "__pycache__"
}

def collect_files(directory):
    for root, _, files in os.walk(directory):
        if any(excluded in root for excluded in EXCLUDED_DIRS):
            continue
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in EXCLUDED_EXTENSIONS:
                continue
            file_types.setdefault(ext, []).append(os.path.join(root, file))

def run_command(command, name):
    print(f"\n🔍 Running {name}...")
    subprocess.run(command, shell=True)

def run_all_checks():
    run_pylint(file_types['.py'])
    run_flake8(file_types['.py'])
    run_mypy(file_types['.py'])
    run_bandit(file_types['.py'])
    run_js_linter(file_types['.js'])
    run_css_linter(file_types['.css'])
    run_htmlhint(file_types['.html'])

if __name__ == "__main__":
    print("You are in this directory:",os.getcwd())
    directory = input("Enter the directory to scan: ").strip()
    if not os.path.isdir(directory):
        print("❌ Error: Invalid directory!")
        exit(1)

    print(f"\n🔍 Scanning directory: {directory}...")
    collect_files(directory)
    run_all_checks()
    get_lang_percentage(directory)

