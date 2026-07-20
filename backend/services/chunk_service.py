


CHUNK_SIZE = 100   
CHUNK_OVERLAP = 20   # lines


def chunk_repository(parsed_repository):
    """
    Create chunks from parsed repository.
    """

    chunks = []

    for file in parsed_repository:

        chunks.extend(
            chunk_file(file)
        )

    return chunks

def chunk_file(file_data):
    """
    Split a file into overlapping chunks.
    """

    content = file_data["content"]
    lines = content.splitlines()

    chunks = []

    if not lines:
        return chunks

    step = CHUNK_SIZE - CHUNK_OVERLAP
    chunk_id = 1

    for start in range(0, len(lines), step):

        end = start + CHUNK_SIZE

        chunk_text = "\n".join(lines[start:end])

        chunks.append({

            "file": file_data["path"],

            "namespace": file_data["namespace"],

            "classes": file_data["classes"],

            "chunk_id": chunk_id,

            "start_line": start + 1,

            "end_line": min(end, len(lines)),

            "content": chunk_text

        })

        chunk_id += 1

        # Stop when the last chunk reaches the end of the file
        if end >= len(lines):
            break

    return chunks