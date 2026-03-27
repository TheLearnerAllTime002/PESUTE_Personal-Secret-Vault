import hashlib
import os
import time
from getpass import getpass

from config import (
    PASSWORD_FILE, SALT_FILE,
    DECOY_PASSWORD_FILE, DECOY_SALT_FILE,
    MAX_ATTEMPTS, LOCKOUT_DELAY, SELF_DESTRUCT_ATTEMPTS,
)
from core.logger import log
import ui.prompts as prompts


def _generate_salt() -> bytes:
    return os.urandom(16)


def _hash(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()


def _write_credentials(password: str, password_file: str, salt_file: str) -> str:
    salt = _generate_salt()
    with open(salt_file, "wb") as f:
        f.write(salt)
    with open(password_file, "w") as f:
        f.write(_hash(password, salt))
    return password


def _prompt_and_write(prompt_text: str, password_file: str, salt_file: str) -> str:
    password = getpass(f"  {prompt_text}")
    return _write_credentials(password, password_file, salt_file)


def _check(password: str, password_file: str, salt_file: str) -> bool:
    if not os.path.exists(password_file) or not os.path.exists(salt_file):
        return False
    with open(salt_file, "rb") as f:
        salt = f.read()
    with open(password_file, "r") as f:
        stored = f.read()
    return _hash(password, salt) == stored


def setup() -> str:
    password = _prompt_and_write("Set a master password: ", PASSWORD_FILE, SALT_FILE)
    if prompts.confirm("Set up a decoy vault password"):
        _prompt_and_write("Set decoy vault password: ", DECOY_PASSWORD_FILE, DECOY_SALT_FILE)
        prompts.success("Decoy vault configured.")
        log("SETUP: Decoy vault configured")
    log("SETUP: Master password configured")
    return password


def verify() -> tuple[str | None, bool]:
    if not os.path.exists(PASSWORD_FILE):
        return setup(), False

    total_failures = 0

    for attempt in range(1, MAX_ATTEMPTS + 1):
        password = getpass("  Enter master password: ")

        if _check(password, PASSWORD_FILE, SALT_FILE):
            log("LOGIN: Success (real vault)")
            return password, False

        if _check(password, DECOY_PASSWORD_FILE, DECOY_SALT_FILE):
            log("LOGIN: Success (decoy vault)")
            return password, True

        total_failures += 1
        log(f"LOGIN: Failed attempt {attempt}/{MAX_ATTEMPTS}")
        remaining = MAX_ATTEMPTS - attempt

        if total_failures >= SELF_DESTRUCT_ATTEMPTS:
            from features.self_destruct import wipe
            wipe()
            prompts.error("SELF-DESTRUCT: Vault has been wiped.")
            return None, False

        if remaining > 0:
            prompts.error(f"Wrong password! {remaining} attempt(s) remaining.")
            time.sleep(LOCKOUT_DELAY)
        else:
            prompts.error("Too many failed attempts. Vault locked.")
            log("LOGIN: Vault locked after max failed attempts")

    return None, False


def change(current_password: str, cipher) -> str | None:
    from core import storage
    from core.crypto import get_cipher

    if not _check(current_password, PASSWORD_FILE, SALT_FILE):
        prompts.error("Current password is wrong.")
        log("CHANGE_PASSWORD: Failed - wrong current password")
        return None

    new_password = getpass("  New master password: ")
    if new_password != getpass("  Confirm new password: "):
        prompts.error("Passwords do not match.")
        return None

    entries = storage.load(cipher, fake=False)
    _write_credentials(new_password, PASSWORD_FILE, SALT_FILE)
    storage.save(entries, get_cipher(new_password), fake=False)

    prompts.success("Master password changed and vault re-encrypted.")
    log("CHANGE_PASSWORD: Success")
    return new_password


def remove() -> bool:
    if not prompts.confirm("Remove master password and reset all auth"):
        prompts.info("Cancelled.")
        return False

    for path in [PASSWORD_FILE, SALT_FILE, DECOY_PASSWORD_FILE, DECOY_SALT_FILE]:
        if os.path.exists(path):
            os.remove(path)

    prompts.success("Master password removed. Set a new one on next launch.")
    log("REMOVE_PASSWORD: Auth files deleted")
    return True
