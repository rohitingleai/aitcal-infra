import json
from pathlib import Path

USER_FILE = Path("data/users.json")

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def get_user_by_email(email: str):
    users = load_users()
    for user in users:
        if user["email"].lower() == email.lower():
            return user
    return None
