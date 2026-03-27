import threading
import time

from config import CLIPBOARD_CLEAR
from core import storage
from core.logger import log
from features.entries import view, unlock_entry
import ui.prompts as prompts
import ui.tui as tui


def copy_secret(cipher, fake: bool = False):
    entries = storage.load(cipher, fake)
    if not entries:
        prompts.info("No entries found.")
        return

    tui.section("Copy Secret to Clipboard")
    view(cipher, fake)

    try:
        index = int(prompts.prompt("Entry number to copy")) - 1
    except ValueError:
        prompts.error("Invalid number.")
        return

    if not 0 <= index < len(entries):
        prompts.error("Invalid number.")
        return

    entry = entries[index]
    if not unlock_entry(entry):
        log(f"COPY: Failed PIN for '{entry['title']}'")
        return

    _copy_and_schedule_clear(entry["secret"], entry["title"])


def _copy_and_schedule_clear(text: str, title: str = ""):
    try:
        import pyperclip
        pyperclip.copy(text)
        prompts.success(f"'{title}' secret copied. Auto-clearing in {CLIPBOARD_CLEAR}s.")
        log("CLIPBOARD: Secret copied, auto-clear scheduled")

        def clear():
            time.sleep(CLIPBOARD_CLEAR)
            try:
                if pyperclip.paste() == text:
                    pyperclip.copy("")
                    tui.console.print(f"\n  [dim cyan]›[/] [dim]Clipboard cleared.[/]\n")
                    log("CLIPBOARD: Cleared")
            except Exception:
                pass

        threading.Thread(target=clear, daemon=True).start()
    except ImportError:
        prompts.error("pyperclip not installed. Run: pip install pyperclip")
