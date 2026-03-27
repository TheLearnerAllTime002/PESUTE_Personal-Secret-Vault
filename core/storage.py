import json
import os
from cryptography.fernet import Fernet
from config import REAL_VAULT_FILE, FAKE_VAULT_FILE
from core.crypto import encrypt, decrypt


def _path(fake: bool) -> str:
    return FAKE_VAULT_FILE if fake else REAL_VAULT_FILE


def load(cipher: Fernet, fake: bool = False) -> list[dict]:
    path = _path(fake)
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


def save(entries: list[dict], cipher: Fernet, fake: bool = False):
    path = _path(fake)
    with open(path, "w") as f:
        for entry in entries:
            f.write(encrypt(json.dumps(entry), cipher) + "\n")
