

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(BASE_DIR, "storage")
UPLOAD_FOLDER = os.path.join(STORAGE_FOLDER, "uploads")
REPO_FOLDER = os.path.join(STORAGE_FOLDER, "repos")
INDEX_FOLDER = os.path.join(STORAGE_FOLDER, "indexes")
HISTORY_FOLDER = os.path.join(STORAGE_FOLDER, "history")

os.makedirs(STORAGE_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPO_FOLDER, exist_ok=True)
os.makedirs(INDEX_FOLDER, exist_ok=True)
os.makedirs(HISTORY_FOLDER, exist_ok=True)

UPLOAD_FOLDER = os.path.join(STORAGE_FOLDER, "uploads")

REPO_FOLDER = os.path.join(STORAGE_FOLDER, "repos")

INDEX_FOLDER = os.path.join(STORAGE_FOLDER, "indexes")

HISTORY_FOLDER = os.path.join(STORAGE_FOLDER, "history")

os.makedirs(HISTORY_FOLDER, exist_ok=True)


# Neo4j Configuration

NEO4J_URI = "neo4j://127.0.0.1:7687"

NEO4J_USER = "neo4j"

NEO4J_PASSWORD = "12345678"