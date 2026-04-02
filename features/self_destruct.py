import os
from config import get_user_paths
from core.logger import log

def wipe(username: str):
    """Permanently delete a specific user's vault data files. Unrecoverable."""
    paths = get_user_paths(username)
    targets = [paths["real_vault"], paths["fake_vault"]]
    wiped   = []

    for path in targets:
        if os.path.exists(path):
            # overwrite with zeros before deleting to prevent forensic recovery
            size = os.path.getsize(path)
            with open(path, "wb") as f:
                f.write(b"\x00" * size)
            os.remove(path)
            wiped.append(path)

    log(f"SELF_DESTRUCT: {username}'s vault wiped after max failed login attempts")
    return wiped