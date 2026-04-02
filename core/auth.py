import hashlib
import os
import time
from getpass import getpass

from config import get_user_paths, MAX_ATTEMPTS, LOCKOUT_DELAY, SELF_DESTRUCT_ATTEMPTS
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

def register_user(username: str):
    paths = get_user_paths(username)
    if os.path.exists(paths["password_file"]):
        prompts.error("User already exists!")
        return
        
    _prompt_and_write(f"Set master password for '{username}': ", paths["password_file"], paths["salt_file"])
    if prompts.confirm("Set up a decoy vault password?"):
        _prompt_and_write("Set decoy vault password: ", paths["decoy_password_file"], paths["decoy_salt_file"])
        prompts.success("Decoy vault configured.")
    prompts.success(f"User '{username}' registered successfully. You can now login.")
    log(f"SETUP: User {username} registered")

def verify(username: str) -> tuple[str | None, bool]:
    paths = get_user_paths(username)
    if not os.path.exists(paths["password_file"]):
        prompts.error("User not found. Please register first.")
        time.sleep(1)
        return None, False

    total_failures = 0
    for attempt in range(1, MAX_ATTEMPTS + 1):
        password = getpass("  Enter master password: ")

        if _check(password, paths["password_file"], paths["salt_file"]):
            log(f"LOGIN: {username} success (real vault)")
            return password, False

        if _check(password, paths["decoy_password_file"], paths["decoy_salt_file"]):
            log(f"LOGIN: {username} success (decoy vault)")
            return password, True

        total_failures += 1
        log(f"LOGIN: {username} failed attempt {attempt}/{MAX_ATTEMPTS}")
        remaining = MAX_ATTEMPTS - attempt

        if total_failures >= SELF_DESTRUCT_ATTEMPTS:
            from features.self_destruct import wipe
            wipe(username)
            prompts.error("SELF-DESTRUCT: Vault has been wiped.")
            return None, False

        if remaining > 0:
            prompts.error(f"Wrong password! {remaining} attempt(s) remaining.")
            time.sleep(LOCKOUT_DELAY)
        else:
            prompts.error("Too many failed attempts. Vault locked.")

    return None, False

def change(username: str, current_password: str, cipher) -> str | None:
    from core import storage
    from core.crypto import get_cipher
    paths = get_user_paths(username)

    if not _check(current_password, paths["password_file"], paths["salt_file"]):
        prompts.error("Current password is wrong.")
        return None

    new_password = getpass("  New master password: ")
    if new_password != getpass("  Confirm new password: "):
        prompts.error("Passwords do not match.")
        return None

    entries = storage.load(username, cipher, fake=False)
    _write_credentials(new_password, paths["password_file"], paths["salt_file"])
    storage.save(username, entries, get_cipher(username, new_password), fake=False)

    prompts.success("Master password changed and vault re-encrypted.")
    return new_password

def remove(username: str) -> bool:
    if not prompts.confirm(f"Delete account and auth for '{username}'?"):
        return False
    
    paths = get_user_paths(username)
    for key in ["password_file", "salt_file", "decoy_password_file", "decoy_salt_file"]:
        path = paths[key]
        if os.path.exists(path):
            os.remove(path)

    prompts.success(f"User '{username}' authentication removed.")
    return True