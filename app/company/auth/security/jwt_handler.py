import os, json
from pathlib import Path
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
BLACKLIST_FILE = Path("data/blacklist.json")

def create_jwt(data: dict, expires_in: int = 3600) -> str:
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(seconds=expires_in)})
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str) -> dict:
    try:
        if is_token_blacklisted(token):
            return None
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None

def blacklist_token(token: str):
    if BLACKLIST_FILE.exists():
        with open(BLACKLIST_FILE, "r") as f:
            tokens = json.load(f)
    else:
        tokens = []

    if token not in tokens:
        tokens.append(token)

    with open(BLACKLIST_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

def is_token_blacklisted(token: str) -> bool:
    if not BLACKLIST_FILE.exists():
        return False
    with open(BLACKLIST_FILE, "r") as f:
        tokens = json.load(f)
    return token in tokens
