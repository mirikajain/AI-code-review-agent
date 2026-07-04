from sentence_transformers import SentenceTransformer

# Load the model only once when Flask starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Generate embeddings for all code chunks.

    Args:
        chunks (list): List of chunk dictionaries.

    Returns:
        list: Chunks with embeddings attached.
    """

    embedded_chunks = []

    for chunk in chunks:

        embedding = model.encode(
            chunk["content"],
            convert_to_numpy=True
        )

        embedded_chunks.append({

            "file": chunk["file"],

            "namespace": chunk["namespace"],

            "classes": chunk["classes"],

            "chunk_id": chunk["chunk_id"],

            "start_line": chunk["start_line"],

            "end_line": chunk["end_line"],

            "content": chunk["content"],

            "embedding": embedding.tolist()
        })

    return embedded_chunks
def generate_query_embedding(query):
    """
    Generate embedding for a user query.
    """

    embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    return embedding