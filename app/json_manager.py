#json_manager.py
import os
import json

def save_json(file_path: str, data: dict):
    """Save arbitrary data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(file_path: str, default=None):
    """Load data from a JSON file, return default if missing or invalid."""
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        return default