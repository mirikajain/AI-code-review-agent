from services.repository_scanner import scan_repository
from services.dependency_parser import parse_dependencies
from services.parser_service import parse_repository
from services.chunk_service import chunk_repository

def analyze_repository(repo_path):

    # Scan repository
    scan_result = scan_repository(repo_path)

    # Parse dependencies
    dependencies = parse_dependencies(
        repo_path,
        scan_result["metadata_files"]
    )

    # Parse source code
    parsed_repository = parse_repository(
        repo_path,
        scan_result["code_files"]
    )
    chunks = chunk_repository(parsed_repository)

    return {
        "scan": scan_result,
        "dependencies": dependencies,
        "parsed_repository": parsed_repository,
        "chunks": chunks
    }