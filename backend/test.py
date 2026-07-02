import os

from config import REPO_FOLDER

from services.repository_scanner import scan_repository
from services.parser_service import parse_repository
from services.chunk_service import chunk_repository
from services.embedding_service import generate_embeddings

repo_id = "0348feb4-2873-4e84-b348-3eb22caa3662"

repo_path = os.path.join(REPO_FOLDER, repo_id)

scan = scan_repository(repo_path)

parsed = parse_repository(
    repo_path,
    scan["code_files"]
)

chunks = chunk_repository(parsed)

embedded = generate_embeddings(chunks)

print("Total Chunks:", len(embedded))

print()

print("Embedding Dimension:", len(embedded[0]["embedding"]))

print()

print("First 10 Values:")

print(embedded[0]["embedding"][:10])