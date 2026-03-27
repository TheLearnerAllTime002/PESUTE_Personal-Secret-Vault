import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from config import SALT_FILE


def _load_salt() -> bytes:
    with open(SALT_FILE, "rb") as f:
        return f.read()


def get_cipher(password: str) -> Fernet:
    salt = _load_salt()
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
