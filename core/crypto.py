import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from config import get_user_paths

def _load_salt(username: str) -> bytes:
    paths = get_user_paths(username)
    with open(paths["salt_file"], "rb") as f:
        return f.read()

def get_cipher(username: str, password: str) -> Fernet:
    salt = _load_salt(username)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

def encrypt(text: str, cipher: Fernet) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt(text: str, cipher: Fernet) -> str:
    return cipher.decrypt(text.encode()).decode()