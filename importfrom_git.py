from git import Repo
import os

def clone_github_repo(repo_url, clone_dir="."):
    try:
        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
        Repo.clone_from(repo_url, os.path.join(clone_dir, repo_url.split('/')[-1].replace('.git', '')))
        print(f" Clone {repo_url} at {clone_dir}")
    except Exception as e:
        print(f"❌ Error: {e}")
