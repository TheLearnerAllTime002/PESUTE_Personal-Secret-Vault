import time

from config import AUTO_LOCK_SECONDS
from core import auth, crypto
from features import entries, search, clipboard, categories, transfer, versioning
import ui.tui as tui
import ui.prompts as prompts


def main():
    password, is_fake = auth.verify()
    if not password:
        return

    cipher = crypto.get_cipher(password)
    tui.header(is_fake)
    last_activity = time.time()

    while True:
        time_left = AUTO_LOCK_SECONDS - (time.time() - last_activity)
        if time_left <= 0:
            prompts.error("Auto-locked due to inactivity.")
            return

        tui.menu(time_left)
        choice = prompts.prompt("Choose").strip()
        last_activity = time.time()

        if   choice == "1":  entries.add(cipher, is_fake)
        elif choice == "2":  entries.view(cipher, is_fake)
        elif choice == "3":  entries.delete(cipher, is_fake)
        elif choice == "4":  search.search(cipher, is_fake)
        elif choice == "5":  clipboard.copy_secret(cipher, is_fake)
        elif choice == "6":  categories.list_categories(cipher, is_fake)
        elif choice == "7":  versioning.versioning_menu(cipher, is_fake)
        elif choice == "8":  transfer.export(cipher, is_fake)
        elif choice == "9":  transfer.backup(is_fake)
        elif choice == "10": transfer.import_vault(cipher, is_fake)
        elif choice == "11":
            new_password = auth.change(password, cipher)
            if new_password:
                password = new_password
                cipher   = crypto.get_cipher(password)
        elif choice == "12":
            if auth.remove():
                return
        elif choice == "13": break
        else:
            prompts.error("Invalid option.")


if __name__ == "__main__":
    main()
