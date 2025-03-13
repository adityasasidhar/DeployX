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

