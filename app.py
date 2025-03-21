import os
import shutil
import subprocess
from werkzeug.utils import secure_filename
from import_from_git import clone_github_repo
from language_task import get_lang_percentage
from flask import Flask, render_template, request, jsonify, send_from_directory
from testing import lint_project
from ai_utils import fix_a_project, analyze_all_code_files

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_projects'
STATIC_SERVE_FOLDER = 'static_projects'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_SERVE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_project():
    folder_name = secure_filename(request.form.get('folder_name', 'default_project'))
    repo_url = request.form.get('repo_url', '').strip()
    project_path = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(project_path, exist_ok=True)
    if repo_url:
        try:
            clone_github_repo(repo_url, clone_dir=UPLOAD_FOLDER)
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            project_path = os.path.join(UPLOAD_FOLDER, repo_name)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Failed to clone: {str(e)}'})
    else:
        for file in request.files.getlist('files[]'):
            filepath = os.path.join(project_path, file.filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

    lang_percentages = get_lang_percentage(project_path)
    print(lang_percentages)
    lint_project(project_path)

    if os.path.exists(os.path.join(project_path, 'app.py')):
        try:
            port = 5001
            subprocess.Popen(['python', 'app.py'], cwd=project_path)
            return jsonify({
                'status': 'flask',
                'url': f'http://localhost:{port}',
                'languages': lang_percentages
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

    elif os.path.exists(os.path.join(project_path, 'index.html')):
        static_path = os.path.join(STATIC_SERVE_FOLDER, folder_name)
        if os.path.exists(static_path):
            shutil.rmtree(static_path)
        shutil.copytree(project_path, static_path)
        return jsonify({
            'status': 'static',
            'url': f'/preview/{folder_name}/index.html',
            'languages': lang_percentages
        })

    elif os.path.exists(os.path.join(project_path, 'build')) or os.path.exists(os.path.join(project_path, 'dist')):
        static_path = os.path.join(STATIC_SERVE_FOLDER, folder_name)
        if os.path.exists(static_path):
            shutil.rmtree(static_path)
        shutil.copytree(
            os.path.join(project_path, 'build' if os.path.exists(os.path.join(project_path, 'build')) else 'dist'),
            static_path)
        return jsonify({
            'status': 'static',
            'url': f'/preview/{folder_name}/index.html',
            'languages': lang_percentages
        })
    else:
        return jsonify({'status': 'error', 'message': 'Unknown project type: No app.py or index.html found'})

@app.route('/preview/<project>/<path:filename>')
def preview_static(project, filename):
    return send_from_directory(os.path.join(STATIC_SERVE_FOLDER, project), filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)