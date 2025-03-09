from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import shutil
import subprocess
import time
from werkzeug.utils import secure_filename


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
    folder_name = secure_filename(request.form['folder_name'])
    project_path = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(project_path, exist_ok=True)

    for file in request.files.getlist('files[]'):
        filepath = os.path.join(project_path, file.filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

    # Check project type
    if os.path.exists(os.path.join(project_path, 'app.py')):
        try:
            port = 5001
            subprocess.Popen(['python', 'app.py'], cwd=project_path)
            time.sleep(2)
            return jsonify({'status': 'flask', 'url': f'http://localhost:{port}'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    elif os.path.exists(os.path.join(project_path, 'index.html')):
        static_path = os.path.join(STATIC_SERVE_FOLDER, folder_name)
        if os.path.exists(static_path):
            shutil.rmtree(static_path)
        shutil.copytree(project_path, static_path)
        return jsonify({'status': 'static', 'url': f'/preview/{folder_name}/index.html'})
    else:
        return jsonify({'status': 'error', 'message': 'Unknown project type: No app.py or index.html found'})

@app.route('/preview/<project>/<path:filename>')
def preview_static(project, filename):
    return send_from_directory(os.path.join(STATIC_SERVE_FOLDER, project), filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
