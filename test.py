import os
import shutil
import subprocess
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_from_directory
from src.language_task import get_lang_percentage
from testing import lint_project
import os
import re
from git import Repo, GitCommandError
from github import Github, GithubException


def clone_github_repo(repo_input, clone_dir=".", use_github_api=False, github_token=None):
    """
    Clone a GitHub repository (supports various formats) using GitPython.

    Supported formats:
    - https://github.com/user/repo.git
    - https://github.com/user/repo
    - git@github.com:user/repo.git
    - user/repo (shorthand)

    Parameters:
    - repo_input: GitHub repo in any format
    - clone_dir: Directory where the repo will be cloned
    - use_github_api: Whether to verify existence via GitHub API
    - github_token: Optional GitHub token (for private repos or API check)
    """
    try:
        # Normalize repo URL
        if repo_input.startswith(("https://github.com", "git@github.com")):
            repo_url = repo_input if repo_input.endswith(".git") else repo_input + ".git"
        elif re.match(r'^[\w-]+/[\w.-]+$', repo_input):
            repo_url = f"https://github.com/{repo_input}.git"
        else:
            raise ValueError("Unsupported GitHub repository format.")

        # Get repo name from URL
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        dest_path = os.path.join(clone_dir, repo_name)

        # GitHub API check (optional)
        if use_github_api:
            try:
                g = Github(github_token) if github_token else Github()
                owner, name = repo_input.split('/')[-2:] if '/' in repo_input else (None, None)
                if owner and name:
                    g.get_repo(f"{owner}/{name}")
                    print(f"✅ GitHub API check passed for {owner}/{name}")
            except GithubException as ge:
                print(f"❌ GitHub API error: {ge}")
                return

        # Clone if not already exists
        if os.path.exists(dest_path):
            print(f"⚠️ Repo already exists at {dest_path}. Skipping clone.")
            return

        print(f"🔗 Cloning from: {repo_url}")
        Repo.clone_from(repo_url, dest_path)
        print("✅ Cloned successfully to:", dest_path)

    except GitCommandError as ge:
        print(f"❌ Git error: {ge}")
    except Exception as e:
        print(f"⚠️ Error: {e}")


"""


                                                       Flow of Program:
                                                               |
                                                  Upload the directory/files either
                                                through drag and drop or by github url
                                                               |
                                                figure out the language percentage
                                                               |
                                                    check for syntax errors
                                                     |                  |
                                        error is found                 error is not found
                        {                                              {
                        clear the uploaded folder                       continue with the emulation and 
                        and reprompt for the correctness                display the website
                                                        }                                        }
                                                        |
                                            restart the Flow of Program              



"""
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

    if repo_url:  # 📥 GitHub URL Upload
        try:
            clone_github_repo(repo_url, clone_dir=UPLOAD_FOLDER)
            # Set project_path to cloned repo directory
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            project_path = os.path.join(UPLOAD_FOLDER, repo_name)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Failed to clone: {str(e)}'})
    else:  # 📥 File Upload
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
    else:
        return jsonify({'status': 'error', 'message': 'Unknown project type: No app.py or index.html found'})



@app.route('/preview/<project>/<path:filename>')
def preview_static(project, filename):
    return send_from_directory(os.path.join(STATIC_SERVE_FOLDER, project), filename)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
