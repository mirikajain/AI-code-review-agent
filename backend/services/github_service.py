from config import STORAGE_FOLDER
import os
from git import Repo
import uuid

REPO_FOLDER = os.path.join(STORAGE_FOLDER, "repos")

os.makedirs(REPO_FOLDER, exist_ok=True)


def clone_repository(repo_url):

    try:

        # Generate a new ID for every clone
        repo_id = str(uuid.uuid4())

        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")

        repo_path = os.path.join(REPO_FOLDER, repo_id)

        Repo.clone_from(repo_url, repo_path)

        return {
            "success": True,
            "repo_id": repo_id,
            "message": "Repository cloned successfully.",
            "repository_name": repo_name,
            "repository_path": repo_path
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }