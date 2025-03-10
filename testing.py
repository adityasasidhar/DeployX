import os
import cssutils
import esprima
import subprocess

# HTML Linter
def run_html_linter(files):
    from tidylib import tidy_document
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                html = f.read()
                _, errors = tidy_document(html, options={"show-warnings": True})
                if not errors.strip():
                    return 1
                else:
                    return 0
        except Exception:
            return 0

# CSS Linter
def run_css_linter(files):
    cssutils.log.setLevel('FATAL')  # Suppress cssutils logs
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                css = f.read()
                parser = cssutils.CSSParser()
                parser.parseString(css)
                return 1
        except Exception:
            return 0

# JS Linter
def run_js_linter(files):
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                js_code = f.read()
                esprima.parseScript(js_code)
                return 1
        except Exception:
            return 0

# Generic Runner for Python linters
def run_command(cmd, name):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return 1
    else:
        return 0

def run_pylint(files):
    if files:
        run_command(f"pylint --disable=all --enable=errors {' '.join(files)}", "Pylint")

def run_flake8(files):
    if files:
        run_command(f"flake8 {' '.join(files)}", "Flake8")

def run_mypy(files):
    if files:
        run_command(f"mypy {' '.join(files)}", "Mypy")

def run_bandit(files):
    if files:
        run_command(f"bandit -r {' '.join(files)}", "Bandit")


def collect_relevant_files(directory):
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

    file_types = {'.py': [], '.html': [], '.css': [], '.js': []}
    valid_extensions = set(file_types.keys())

    for root, dirs, files in os.walk(directory):
        # Remove excluded dirs in-place for performance
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in valid_extensions and ext not in EXCLUDED_EXTENSIONS:
                file_types[ext].append(os.path.join(root, file))

    return file_types


def run_all_checks(directory):
    file_types = collect_relevant_files(directory)

    if file_types['.py']:
        run_pylint(file_types['.py'])
        run_flake8(file_types['.py'])
        run_mypy(file_types['.py'])
        run_bandit(file_types['.py'])

    if file_types['.js']:
        run_js_linter(file_types['.js'])

    if file_types['.css']:
        run_css_linter(file_types['.css'])

    if file_types['.html']:
        run_html_linter(file_types['.html'])


def lint_project(path="."):
    path = os.path.abspath(path)
    print(f"\n📁 Scanning project at: {path}")

    if not os.path.exists(path):
        print(f"❌ The path '{path}' does not exist.")
        return

    run_all_checks(path)

path = 'TestStaticSite'
run_all_checks(path)