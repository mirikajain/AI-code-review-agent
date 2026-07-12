import os
import json
import uuid
from datetime import datetime

from config import HISTORY_FOLDER


def save_history(repo_id, repo_path, query, review):

    history = {
        "history_id": str(uuid.uuid4()),
        "repo_id": repo_id,
        "repo_path": repo_path,
        "query": query,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "review": review
    }

    filename = history["history_id"] + ".json"

    with open(
        os.path.join(HISTORY_FOLDER, filename),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(history, f, indent=4)

    return history["history_id"]


def get_all_history():

    histories = []

    for file in os.listdir(HISTORY_FOLDER):

        if file.endswith(".json"):

            with open(
                os.path.join(HISTORY_FOLDER, file),
                encoding="utf-8"
            ) as f:

                histories.append(json.load(f))

    histories.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )

    return histories


def get_history(history_id):

    path = os.path.join(
        HISTORY_FOLDER,
        history_id + ".json"
    )

    if not os.path.exists(path):
        return None

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def delete_history(history_id):

    path = os.path.join(
        HISTORY_FOLDER,
        history_id + ".json"
    )

    if os.path.exists(path):
        os.remove(path)
        return True

    return False


def clear_history():

    for file in os.listdir(HISTORY_FOLDER):

        if file.endswith(".json"):
            os.remove(
                os.path.join(HISTORY_FOLDER, file)
            )

    return True