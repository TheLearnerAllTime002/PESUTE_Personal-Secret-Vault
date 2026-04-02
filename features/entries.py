import time
import hashlib
from getpass import getpass
from core import storage
from core.logger import log
import ui.prompts as prompts
import ui.tui as tui

def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

def add(username: str, cipher, fake: bool = False):
    title    = prompts.prompt("Title")
    secret   = getpass("  Secret: ")
    category = prompts.prompt("Category (e.g. Finance, Work)")
    tags     = prompts.prompt("Tags (comma separated)")
    notes    = prompts.prompt("Notes (optional)")
    
    pin_hash = None
    if prompts.confirm("Protect this entry with a PIN?"):
        pin = getpass("  Enter PIN: ")
        pin_hash = _hash_pin(pin)

    entry = {
        "title": title,
        "secret": secret,
        "category": category,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "notes": notes,
        "added": time.time(),
        "last_modified": time.time(),
        "pin_hash": pin_hash,
        "history": []
    }
    
    # PASS USERNAME HERE
    entries = storage.load(username, cipher, fake)
    entries.append(entry)
    storage.save(username, entries, cipher, fake)
    
    prompts.success("Entry added.")
    log(f"ADD: {username} added entry '{title}'")

def unlock_entry(entry: dict) -> bool:
    if not entry.get("pin_hash"):
        return True
    pin = getpass("  Enter PIN for this entry: ")
    if _hash_pin(pin) == entry["pin_hash"]:
        return True
    prompts.error("Incorrect PIN.")
    return False

def view(username: str, cipher, fake: bool = False):
    entries = storage.load(username, cipher, fake)
    if not entries:
        prompts.error("Vault is empty.")
        return
        
    for i, e in enumerate(entries):
        tui.console.print(f"  [cyan]{i}[/] - {e['title']}")
        
    idx = prompts.prompt("Entry number")
    try:
        idx = int(idx)
        entry = entries[idx]
        if unlock_entry(entry):
            tui.entry_card(entry)
            log(f"VIEW: {username} viewed entry '{entry['title']}'")
    except (ValueError, IndexError):
        prompts.error("Invalid entry.")

def delete(username: str, cipher, fake: bool = False):
    entries = storage.load(username, cipher, fake)
    if not entries:
        prompts.error("Vault is empty.")
        return
        
    for i, e in enumerate(entries):
        tui.console.print(f"  [cyan]{i}[/] - {e['title']}")
        
    idx = prompts.prompt("Entry number to delete")
    try:
        idx = int(idx)
        entry = entries.pop(idx)
        if prompts.confirm(f"Delete '{entry['title']}'?"):
            storage.save(username, entries, cipher, fake)
            prompts.success("Deleted.")
            log(f"DELETE: {username} deleted entry '{entry['title']}'")
    except (ValueError, IndexError):
        prompts.error("Invalid entry.")