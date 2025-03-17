import os
import esprima
import subprocess
from lxml import etree, html
import tinycss2

def check_html_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = html.fromstring(content)
        if tree.tag != 'html':
            return False

        head = tree.find('head')
        body = tree.find('body')
        if head is None or body is None:
            return False
        print(f"The file {file_path} is valid")
        return True
    except etree.XMLSyntaxError:
        print(f"XML syntax error in {file_path}")
        return False
    except Exception as e:
        print(f"Unexpected error in {file_path}: {e}")
        return False

def check_css_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        rules = tinycss2.parse_stylesheet(css_content, skip_comments=True, skip_whitespace=True)
        for rule in rules:
            if rule.type == "error":
                print(f"CSS syntax error in {file_path}")
                return False
        print(f"The file {file_path} is valid")
        return True
    except Exception as e:
        print(f"CSS check error in {file_path}: {e}")
        return False

def check_js_file(files):
    all_valid = True
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                js_code = f.read()
                esprima.parseScript(js_code)
        except Exception as e:
            print(f"JS Syntax Error in {file}: {e}")
            all_valid = False

    print(f"The file {files} is valid")
    return all_valid

def check_python_file(file_path):
    def is_python_code_valid(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            compile(source, file_path, 'exec')
            print(f"The file {file_path} is valid")
            return True
        except (SyntaxError, IndentationError) as e:
            print(f"Syntax Error in {file_path}: {e}")
            return False
        except Exception as e:
            print(f"Other Error in {file_path}: {e}")
            return False
    def is_python_file_runnable(file_path):
        try:
            result = subprocess.run(["python", "-m", "py_compile", file_path], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Runtime check error: {e}")
            return False

    is_valid = is_python_code_valid(file_path) and is_python_file_runnable(file_path)
    if is_valid:
      print(f"Python file {file_path} is stable and clear ✅")
    return is_valid

def collect_relevant_files(directory):
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
        ".docker", ".terraform", ".kitchen", "CMakeFiles", "build", "dist", "__pycache__"
    }

    file_types = {'.py': [], '.html': [], '.css': [], '.js': []}
    valid_extensions = set(file_types.keys())

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in valid_extensions and ext not in EXCLUDED_EXTENSIONS:
                file_types[ext].append(os.path.join(root, file))
    return file_types

def run_all_checks(directory):
    file_types = collect_relevant_files(directory)
    all_passed = True

    for py_file in file_types['.py']:
        if not check_python_file(py_file):
            all_passed = False

    if not check_js_file(file_types['.js']):
        all_passed = False

    for css_file in file_types['.css']:
        if not check_css_file(css_file):
            all_passed = False

    for html_file in file_types['.html']:
        if not check_html_file(html_file):
            all_passed = False

    return all_passed


def lint_project(path="."):
    path = os.path.abspath(path)
    print(f"\n📁 Scanning project at: {path}")
    if not os.path.exists(path):
        print(f"❌ The path '{path}' does not exist.")
        return False

    result = run_all_checks(path)
    if result:
        print("\n✅ All files passed checks successfully!")
    else:
        print("\n❌ Some files failed the checks.")

    return result


