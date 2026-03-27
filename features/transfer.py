import json
import os
from datetime import datetime

from config import REAL_VAULT_FILE, FAKE_VAULT_FILE
from core import storage
from core.logger import log
import ui.prompts as prompts
import ui.tui as tui


def _vault_path(fake: bool) -> str:
    return FAKE_VAULT_FILE if fake else REAL_VAULT_FILE


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export(cipher, fake: bool = False):
    tui.section("Export Vault")
    tui.warn("This will write DECRYPTED data to a plain JSON file.")
    if not prompts.confirm("Are you sure you want to export"):
        prompts.info("Export cancelled.")
        return
    entries = storage.load(cipher, fake)
    path = f"data/export_{_stamp()}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    prompts.success(f"Exported {len(entries)} entries to {path}")
    log(f"EXPORT: {len(entries)} entries -> {path}")


def backup(fake: bool = False):
    tui.section("Backup Vault")
    src = _vault_path(fake)
    if not os.path.exists(src):
        prompts.info("Nothing to back up.")
        return
    dst = f"data/backup_{_stamp()}.dat"
    with open(src, "r") as f:
        data = f.read()
    with open(dst, "w") as f:
        f.write(data)
    prompts.success(f"Encrypted backup saved to {dst}")
    log(f"BACKUP: {src} -> {dst}")


def import_vault(cipher, fake: bool = False):
    tui.section("Import Vault")
    path = prompts.prompt("Path to JSON export file").strip()
    if not os.path.exists(path):
        prompts.error("File not found.")
        return
    with open(path, "r", encoding="utf-8") as f:
        imported = json.load(f)
    entries  = storage.load(cipher, fake)
    existing = {e["title"] for e in entries}
    added    = 0
    for e in imported:
        if e.get("title") not in existing:
            e["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entries.append(e)
            added += 1
    storage.save(entries, cipher, fake)
    prompts.success(f"Imported {added} new entry/entries.")
    log(f"IMPORT: {added} entries from {path}")
