import os
import shutil
from git import Repo
import uuid
REPO_FOLDER = "Storage/repos"

os.makedirs(REPO_FOLDER, exist_ok=True)
repo_id=str(uuid.uuid4())

def clone_repository(repo_url):

    try:
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")

        repo_path = os.path.join(REPO_FOLDER, repo_id)

       
       

        # Clone repository
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