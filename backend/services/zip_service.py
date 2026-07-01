import os
import uuid
import zipfile
import shutil

from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER


def save_zip(file):
    """
    Saves the uploaded ZIP file temporarily.
    """

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    return filepath


def extract_zip(zip_path, repo_folder):
    """
    Extracts the ZIP into a unique repository folder.

    Returns:
        repo_id
        repo_path
    """

    os.makedirs(repo_folder, exist_ok=True)

    repo_id = str(uuid.uuid4())

    repo_path = os.path.join(repo_folder, repo_id)

    os.makedirs(repo_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(repo_path)

    normalize_repository(repo_path)

    return repo_id, repo_path


def normalize_repository(repo_path):
    """
    Removes the extra top-level folder that GitHub ZIPs usually contain.

    Before:
        repo_path/
            AI-code-review-agent-main/
                backend/
                frontend/

    After:
        repo_path/
            backend/
            frontend/
    """

    items = os.listdir(repo_path)

    if len(items) != 1:
        return

    first_item = os.path.join(repo_path, items[0])

    if not os.path.isdir(first_item):
        return

    for item in os.listdir(first_item):
        shutil.move(
            os.path.join(first_item, item),
            os.path.join(repo_path, item)
        )

    shutil.rmtree(first_item)