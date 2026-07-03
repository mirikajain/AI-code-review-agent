from services.repository_scanner import scan_repository
from services.dependency_parser import parse_dependencies
from services.parser_service import parse_repository
from services.chunk_service import chunk_repository
from services.embedding_service import generate_embeddings
from services.faiss_service import create_index

def analyze_repository(repo_id,repo_path):

    scan = scan_repository(repo_path)

    dependencies = parse_dependencies(
        repo_path,
        scan["metadata_files"]
    )

    parsed = parse_repository(
        repo_path,
        scan["code_files"]
    )

    chunks = chunk_repository(parsed)

    embedded_chunks = generate_embeddings(chunks)
   
    faiss_info   = create_index(embedded_chunks, repo_id)

    return {

        "scan": scan,

        "dependencies": dependencies,

        "parsed_repository": parsed,

        "chunks": embedded_chunks,

        "faiss": faiss_info
    }