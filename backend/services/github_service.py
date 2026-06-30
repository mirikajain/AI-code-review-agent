import os
import shutil
from git import Repo

REPO_FOLDER = "repositories"

os.makedirs(REPO_FOLDER, exist_ok=True)


def clone_repository(repo_url):

    try:
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")

        repo_path = os.path.join(REPO_FOLDER, repo_name)

        # Delete old copy if exists
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        # Clone repository
        Repo.clone_from(repo_url, repo_path)

        return {
            "success": True,
            "message": "Repository cloned successfully.",
            "repository_name": repo_name,
            "repository_path": repo_path
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }