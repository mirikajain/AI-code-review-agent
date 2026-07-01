import os

# Directories that should never be scanned
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    ".next",
    ".idea",
    ".vscode",
    ".cache",
    "coverage",
    "target",
}

# File extensions to ignore
IGNORE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".zip",
    ".exe",
    ".dll",
    ".so",
    ".class",
    ".jar",
    ".pyc",
    ".mp4",
    ".mp3",
}


def scan_repository(repo_path):
    """
    Scan an extracted/cloned repository and return metadata
    for every useful file.
    """

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        # Skip unwanted folders
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for filename in filenames:

            ext = os.path.splitext(filename)[1].lower()

            if ext in IGNORE_EXTENSIONS:
                continue

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(full_path, repo_path)

            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0

            files.append(
                {
                    "name": filename,
                    "path": relative_path.replace("\\", "/"),
                    "extension": ext,
                    "size": size,
                }
            )

    return files