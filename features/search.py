import re

from core import storage
from core.logger import log
import ui.tui as tui
import ui.prompts as prompts
import ui.display as display
import ui.menus as menus


def search(cipher, fake: bool = False):
    tui.section("Search")
    menus.search_menu()
    mode  = prompts.prompt("Search mode: ").strip()
    query = prompts.prompt("Query: ").strip()

    entries = storage.load(cipher, fake)
    results = []

    for i, e in enumerate(entries):
        title    = e.get("title", "").lower()
        category = e.get("category", "").lower()
        tags     = " ".join(e.get("tags", [])).lower()
        combined = f"{title} {category} {tags}"

        if mode == "1":
            match = query.lower() in title
        elif mode == "2":
            match = query.lower() in category
        elif mode == "3":
            match = query.lower() in combined
        elif mode == "4":
            try:
                match = bool(re.search(query, combined, re.IGNORECASE))
            except re.error:
                prompts.error("Invalid regex.")
                return
        else:
            match = query.lower() in combined

        if match:
            results.append((i + 1, e))

    if not results:
        prompts.info("No matches found.")
        log(f"SEARCH: '{query}' - no results")
        return

    log(f"SEARCH: '{query}' - {len(results)} result(s)")
    for num, e in results:
        display.entry_card(num, e, locked=bool(e.get("pin_hash")))
