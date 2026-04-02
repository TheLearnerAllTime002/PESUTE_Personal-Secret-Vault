import json
import os
from cryptography.fernet import Fernet
from config import get_user_paths
from core.crypto import encrypt, decrypt

def _path(username: str, fake: bool) -> str:
    paths = get_user_paths(username)
    return paths["fake_vault"] if fake else paths["real_vault"]

def load(username: str, cipher: Fernet, fake: bool = False) -> list[dict]:
    path = _path(username, fake)
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(decrypt(line, cipher)))
            except Exception:
                continue
    return entries

def save(username: str, entries: list[dict], cipher: Fernet, fake: bool = False):
    path = _path(username, fake)
    with open(path, "w") as f:
        for entry in entries:
            f.write(encrypt(json.dumps(entry), cipher) + "\n")