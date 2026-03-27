from core import storage
import ui.prompts as prompts
import ui.tui as tui


def list_categories(cipher, fake: bool = False):
    tui.section("Categories")
    entries = storage.load(cipher, fake)
    cats    = sorted({e.get("category", "none") for e in entries})

    if not cats:
        prompts.info("No categories found.")
        return

    data = [(c, sum(1 for e in entries if e.get("category") == c)) for c in cats]
    tui.categories_table(data)
