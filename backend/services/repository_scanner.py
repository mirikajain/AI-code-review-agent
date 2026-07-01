import os

IGNORE_DIRS = {
    ".git",
    ".vs",
    ".vscode",
    "bin",
    "obj",
    "packages",
    "node_modules",
    "__pycache__",
}

CODE_EXTENSIONS = {
    ".cs",
    ".razor",
    ".cshtml"
}

METADATA_EXTENSIONS = {
    ".csproj",
    ".sln",
    ".json",
    ".xml",
    ".config",
    ".props",
    ".targets",
    ".editorconfig",
    ".md",
    ".yml",
    ".yaml"
}


def scan_repository(repo_path):
    code_files = []
    metadata_files = []


    for root, dirs, filenames in os.walk(repo_path):

        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for filename in filenames:

            ext = os.path.splitext(filename)[1].lower()

            # Ignore everything except supported files
            if ext not in CODE_EXTENSIONS and ext not in METADATA_EXTENSIONS:
                continue

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(full_path, repo_path)

            # Determine file type
            if ext in CODE_EXTENSIONS:
                file_type = "code"
            else:
                file_type = "metadata"

            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0

            file_info = {
                "name": filename,
                "path": relative_path.replace("\\", "/"),
                "extension": ext,
                "size": size
            }

            if ext in CODE_EXTENSIONS:
                code_files.append(file_info)
            else:
                metadata_files.append(file_info)

    return {
        "repository": os.path.basename(repo_path),
        "total_code_files": len(code_files),
        "total_metadata_files": len(metadata_files),
        "total_files": len(code_files) + len(metadata_files),
        "code_files": code_files,
        "metadata_files": metadata_files
    } 