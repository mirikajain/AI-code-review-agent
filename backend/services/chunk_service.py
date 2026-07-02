from math import ceil


CHUNK_SIZE = 100      # lines


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

    content = file_data["content"]

    lines = content.splitlines()

    chunks = []

    total_chunks = ceil(len(lines) / CHUNK_SIZE)

    for i in range(total_chunks):

        start = i * CHUNK_SIZE

        end = start + CHUNK_SIZE

        chunk_text = "\n".join(lines[start:end])

        chunks.append({

            "file": file_data["path"],

            "namespace": file_data["namespace"],

            "classes": file_data["classes"],

            "chunk_id": i + 1,

            "start_line": start + 1,

            "end_line": min(end, len(lines)),

            "content": chunk_text

        })

    return chunks