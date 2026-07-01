import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Root storage directory
STORAGE_FOLDER = os.path.join(BASE_DIR, "storage")



UPLOAD_FOLDER = os.path.join(STORAGE_FOLDER, "uploads")

REPO_FOLDER = os.path.join(STORAGE_FOLDER, "repos")

INDEX_FOLDER = os.path.join(STORAGE_FOLDER, "indexes")