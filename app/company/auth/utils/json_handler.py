import json
from pathlib import Path

def read_json(file_path: Path):
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def write_json(file_path: Path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
