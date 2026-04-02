import os

AUTO_LOCK_SECONDS      = 60
MAX_ATTEMPTS           = 3
SELF_DESTRUCT_ATTEMPTS = 5
LOCKOUT_DELAY          = 5
CLIPBOARD_CLEAR        = 10
MAX_HISTORY            = 10

# Create a secure data directory
DATA_DIR = "data"
LOG_FILE = f"{DATA_DIR}/log.txt"

# Ensure the directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def get_user_paths(username: str) -> dict:
    """Dynamically generate file paths for a specific user."""
    return {
        "password_file": f"{DATA_DIR}/{username}_password.txt",
        "salt_file": f"{DATA_DIR}/{username}_salt.bin",
        "decoy_password_file": f"{DATA_DIR}/{username}_decoy_password.txt",
        "decoy_salt_file": f"{DATA_DIR}/{username}_decoy_salt.bin",
        "real_vault": f"{DATA_DIR}/{username}_vault.dat",
        "fake_vault": f"{DATA_DIR}/{username}_decoy_vault.dat",
    }