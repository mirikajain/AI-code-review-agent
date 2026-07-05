from services.repository_scanner import scan_repository
from services.dependency_parser import parse_dependencies
from services.parser_service import parse_repository
from services.chunk_service import chunk_repository
from services.embedding_service import generate_embeddings
from services.faiss_service import create_index

from services.embedding_service import generate_query_embedding
from services.retriever_service import retrieve_chunks
from services.llm_service import generate_review


def analyze_repository(repo_id,repo_path):

    print("Scanning repository...")
    scan = scan_repository(repo_path)

    print("Parsing dependencies...")
    dependencies = parse_dependencies(repo_path, scan["metadata_files"])

    print("Parsing source code...")
    parsed = parse_repository(repo_path, scan["code_files"])

    print("Total parsed files:", len(parsed))

    print("Chunking...")
    chunks = chunk_repository(parsed)

    print("Total chunks:", len(chunks))

    print("Generating embeddings...")
    embedded_chunks = generate_embeddings(chunks)

    print("Total embeddings:", len(embedded_chunks))

    print("Creating FAISS index...")
    faiss_info = create_index(embedded_chunks, repo_id)

    print("FAISS:", faiss_info)

    return {

        "scan": scan,

        "dependencies": dependencies,

        "parsed_repository": parsed,

        "chunks": embedded_chunks,

        "faiss": faiss_info
    }



def review_repository(repo_id, query):
    """
    Retrieve relevant code chunks and generate a review.
    """

    

    # Retrieve relevant chunks from FAISS
    retrieved_chunks = retrieve_chunks(
        repo_id=repo_id,
        query=query,
        top_k=5
    )

    # Generate review using Gemini
    review = generate_review(
        query=query,
        retrieved_chunks=retrieved_chunks
    )

    return {
        "review": review,
        "retrieved_chunks": retrieved_chunks
    }