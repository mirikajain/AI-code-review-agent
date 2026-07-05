import os
import json
import faiss
import numpy as np

from config import INDEX_FOLDER

os.makedirs(INDEX_FOLDER, exist_ok=True)
def create_index(embedded_chunks, repo_id):
    """
    Build and save a FAISS index for one repository.
    """
    
    if not embedded_chunks:
        return None

    vectors = np.array(
        [chunk["embedding"] for chunk in embedded_chunks],
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    index_path = os.path.join(
        INDEX_FOLDER,
        f"{repo_id}.index"
    )

    faiss.write_index(index, index_path)

    metadata = []

    for chunk in embedded_chunks:

        metadata.append({

            "file": chunk["file"],

            "namespace": chunk["namespace"],

            "classes": chunk["classes"],

            "chunk_id": chunk["chunk_id"],

            "start_line": chunk["start_line"],

            "end_line": chunk["end_line"],

            "content": chunk["content"]

        })

    metadata_path = os.path.join(
        INDEX_FOLDER,
        f"{repo_id}.json"
    )

    with open(metadata_path, "w", encoding="utf-8") as f:

        json.dump(metadata, f, indent=4)

    return {

        "index_path": index_path,

        "metadata_path": metadata_path,

        "total_chunks": len(metadata)

    }
def load_index(repo_id):

    index_path = os.path.join(
        INDEX_FOLDER,
        f"{repo_id}.index"
    )

    metadata_path = os.path.join(
        INDEX_FOLDER,
        f"{repo_id}.json"
    )

    index = faiss.read_index(index_path)

    with open(metadata_path, "r", encoding="utf-8") as f:

        metadata = json.load(f)

    return index, metadata
def search(index, metadata, query_embedding, k=5):

    distances, indices = index.search(
        np.array([query_embedding], dtype="float32"),
        k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        chunk = metadata[idx].copy()

        chunk["score"] = float(distance)

        results.append(chunk)
        