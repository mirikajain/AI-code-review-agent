from services.embedding_service import generate_query_embedding
from services.faiss_service import load_index, search


def retrieve_chunks(repo_id, query, top_k=5):
    """
    Retrieve the most relevant chunks for a query.
    """

    # Load FAISS index
    index, metadata = load_index(repo_id)

    # Generate query embedding
    query_embedding = generate_query_embedding(query)

    # Search FAISS
    results = search(
        index,
        metadata,
        query_embedding,
        top_k
    )

    return results