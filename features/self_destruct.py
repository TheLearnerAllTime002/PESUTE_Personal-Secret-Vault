import os
from config import REAL_VAULT_FILE, FAKE_VAULT_FILE, LOG_FILE
from core.logger import log


def wipe():
    """Permanently delete all vault data files. Unrecoverable."""
    targets = [REAL_VAULT_FILE, FAKE_VAULT_FILE]
    wiped   = []

    for path in targets:
        if os.path.exists(path):
            # overwrite with zeros before deleting
            size = os.path.getsize(path)
            with open(path, "wb") as f:
                f.write(b"\x00" * size)
            os.remove(path)
            wiped.append(path)

    log("SELF_DESTRUCT: Vault wiped after max failed login attempts")
    return wiped
