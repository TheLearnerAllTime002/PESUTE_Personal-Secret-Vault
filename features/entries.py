import hashlib
from datetime import datetime
from getpass import getpass

from core import storage
from core.logger import log
import ui.prompts as prompts
import ui.display as display
import ui.tui as tui


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


def unlock_entry(entry: dict) -> bool:
    if not entry.get("pin_hash"):
        return True
    if _hash_pin(getpass("  Entry PIN: ")) == entry["pin_hash"]:
        return True
    prompts.error("Wrong entry PIN.")
    return False


def add(cipher, fake: bool = False):
    tui.section("Add New Entry")
    title    = prompts.prompt("Title").strip()
    secret   = getpass("  Secret: ")
    category = prompts.prompt("Category [none]").strip() or "none"
    tags     = prompts.prompt("Tags  (comma-separated, leave blank to skip)").strip()
    notes    = prompts.prompt("Notes (leave blank to skip)").strip()
    pin_hash = ""

    if prompts.confirm("Protect this entry with a PIN"):
        pin_hash = _hash_pin(getpass("  Set entry PIN: "))

    entry = {
        "title":         title,
        "secret":        secret,
        "category":      category.lower(),
        "tags":          [t.strip().lower() for t in tags.split(",") if t.strip()],
        "notes":         notes,
        "pin_hash":      pin_hash,
        "history":       [],
        "created_at":    _now(),
        "last_modified": _now(),
    }

    all_entries = storage.load(cipher, fake)
    all_entries.append(entry)
    storage.save(all_entries, cipher, fake)
    prompts.success(f"Entry '{title}' added.")
    log(f"ADD: '{title}' [{category}]")


def view(cipher, fake: bool = False):
    all_entries = storage.load(cipher, fake)
    if not all_entries:
        prompts.info("No entries found.")
        return
    tui.section("All Entries")
    for i, e in enumerate(all_entries):
        display.entry_card(i + 1, e, locked=bool(e.get("pin_hash")))


def delete(cipher, fake: bool = False):
    all_entries = storage.load(cipher, fake)
    if not all_entries:
        prompts.info("No entries to delete.")
        return
    tui.section("Delete Entry")
    view(cipher, fake)
    try:
        index = int(prompts.prompt("Entry number to delete")) - 1
    except ValueError:
        prompts.error("Invalid number.")
        return
    if not 0 <= index < len(all_entries):
        prompts.error("Invalid number.")
        return
    title = all_entries[index]["title"]
    if not prompts.confirm(f"Delete '{title}'? This cannot be undone"):
        prompts.info("Cancelled.")
        return
    all_entries.pop(index)
    storage.save(all_entries, cipher, fake)
    prompts.success(f"Entry '{title}' deleted.")
    log(f"DELETE: '{title}'")
