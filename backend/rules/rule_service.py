import json
import os

RULE_FILE = os.path.join(
    os.path.dirname(__file__),
    "custom_rules.json"
)

def load_custom_rules():
    try:
        with open(RULE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []