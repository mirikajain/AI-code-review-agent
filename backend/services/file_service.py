import os


def read_file(repo_path, relative_path):
    """
    Read a text file from a repository.
    """

    file_path = os.path.join(repo_path, relative_path)

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return None