from datetime import datetime
from getpass import getpass

from config import MAX_HISTORY
from core import storage
from core.logger import log
from features.entries import unlock_entry
import ui.tui as tui
import ui.prompts as prompts


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def edit(cipher, fake: bool = False):
    all_entries = storage.load(cipher, fake)
    if not all_entries:
        prompts.info("No entries found.")
        return

    tui.section("Edit Entry")
    for i, e in enumerate(all_entries):
        tui.entry_card(i + 1, e, locked=bool(e.get("pin_hash")))

    try:
        index = int(prompts.prompt("Entry number to edit")) - 1
    except ValueError:
        prompts.error("Invalid number.")
        return

    if not 0 <= index < len(all_entries):
        prompts.error("Invalid number.")
        return

    entry = all_entries[index]
    if not unlock_entry(entry):
        return

    tui.section(f"Editing: {entry['title']}")
    tui.info("Leave blank to keep the current value.")
    tui.console.print()

    new_title    = prompts.prompt(f"Title [{entry['title']}]").strip()
    new_category = prompts.prompt(f"Category [{entry.get('category', 'none')}]").strip()
    new_tags     = prompts.prompt(f"Tags [{', '.join(entry.get('tags', []))}]").strip()
    new_notes    = prompts.prompt(f"Notes [{entry.get('notes', '')}]").strip()
    new_secret   = getpass("  New secret (blank = keep): ")

    changed = False

    if new_title:
        entry["title"] = new_title
        changed = True
    if new_category:
        entry["category"] = new_category.lower()
        changed = True
    if new_tags:
        entry["tags"] = [t.strip().lower() for t in new_tags.split(",") if t.strip()]
        changed = True
    if new_notes:
        entry["notes"] = new_notes
        changed = True
    if new_secret:
        history = entry.get("history", [])
        history.append({"secret": entry["secret"], "changed_at": _now()})
        entry["history"] = history[-MAX_HISTORY:]
        entry["secret"]  = new_secret
        changed = True

    if changed:
        entry["last_modified"] = _now()
        storage.save(all_entries, cipher, fake)
        prompts.success("Entry updated.")
        log(f"EDIT: '{entry['title']}'")
    else:
        prompts.info("No changes made.")


def view_history(cipher, fake: bool = False):
    all_entries = storage.load(cipher, fake)
    if not all_entries:
        prompts.info("No entries found.")
        return

    versioned = [(i, e) for i, e in enumerate(all_entries) if e.get("history")]
    if not versioned:
        prompts.info("No entries have version history yet.")
        return

    tui.section("Version History")
    for pos, (i, e) in enumerate(versioned, 1):
        tui.entry_card(pos, e, locked=bool(e.get("pin_hash")))

    try:
        pick = int(prompts.prompt("Entry number to view history")) - 1
    except ValueError:
        prompts.error("Invalid number.")
        return

    if not 0 <= pick < len(versioned):
        prompts.error("Invalid number.")
        return

    _, entry = versioned[pick]
    if not unlock_entry(entry):
        return

    tui.history_table(entry["history"])
    log(f"VIEW_HISTORY: '{entry['title']}'")


def versioning_menu(cipher, fake: bool = False):
    tui.section("Edit / Version History")
    tui.console.print("  [yellow]1.[/]  Edit entry")
    tui.console.print("  [yellow]2.[/]  View secret history")
    tui.console.print()
    choice = prompts.prompt("Choose").strip()

    if   choice == "1": edit(cipher, fake)
    elif choice == "2": view_history(cipher, fake)
    else: prompts.error("Invalid option.")
