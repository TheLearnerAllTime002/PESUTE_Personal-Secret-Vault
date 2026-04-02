import time
import os

from config import AUTO_LOCK_SECONDS, DATA_DIR
from core import auth, crypto
from features import entries, search, clipboard, categories, transfer, versioning, password_generator, export_import
import ui.tui as tui
import ui.prompts as prompts

def vault_menu(username: str, password: str, is_fake: bool):
    """The main interactive vault loop after a successful login."""
    cipher = crypto.get_cipher(username, password)
    tui.header(is_fake)
    last_activity = time.time()

    def refresh_activity():
        nonlocal last_activity
        last_activity = time.time()

    while True:
        time_left = AUTO_LOCK_SECONDS - (time.time() - last_activity)
        if time_left <= 0:
            prompts.error("Auto-locked due to inactivity.")
            return

        tui.menu(time_left)
        choice = prompts.prompt("Choose").strip()
        # Notice how `username` is now passed to every feature function
        if   choice == "1":  entries.add(username, cipher, is_fake)
        elif choice == "2":  entries.view(username, cipher, is_fake)
        elif choice == "3":  entries.delete(username, cipher, is_fake)
        elif choice == "4":  search.search(username, cipher, is_fake)
        elif choice == "5":  clipboard.copy_secret(username, cipher, is_fake)
        elif choice == "6":  categories.list_categories(username, cipher, is_fake)
        elif choice == "7":  versioning.versioning_menu(username, cipher, is_fake)
        elif choice == "8":  transfer.export(username, cipher, is_fake)
        elif choice == "9":  transfer.backup(username, is_fake)
        elif choice == "10": transfer.import_vault(username, cipher, is_fake)
        elif choice == "11":
            new_password = auth.change(username, password, cipher)
            if new_password:
                password = new_password
                cipher   = crypto.get_cipher(username, password)
        elif choice == "12":
            if auth.remove(username):
                return
        elif choice == "13":
            password_generator.password_generator_menu()
        elif choice == "14":
            export_import.export_import_menu(username, cipher, is_fake)
        elif choice == "15": break
        else:
            prompts.error("Invalid option.")
            refresh_activity()
            continue

        # Reset the inactivity timer after every handled command (except exiting)
        refresh_activity()

def landing_menu():
    """Pre-authentication menu for multi-user support."""
    os.makedirs(DATA_DIR, exist_ok=True)
    while True:
        tui.clear()
        tui.console.print(tui.Panel("[bold cyan]Welcome to PESUTE Secret Vault[/]\n[dim]Multi-User System . Created by[/] Arjun Mitra", expand=False))
        tui.console.print("  [yellow]1.[/] Login")
        tui.console.print("  [yellow]2.[/] Register New User")
        tui.console.print("  [yellow]3.[/] Exit\n")
        
        choice = prompts.prompt("Choose").strip()
        
        if choice == "1":
            username = prompts.prompt("Enter Username").strip()
            password, is_fake = auth.verify(username)
            if password:
                vault_menu(username, password, is_fake)
        elif choice == "2":
            username = prompts.prompt("Choose a Username").strip()
            auth.register_user(username)
        elif choice == "3":
            tui.console.print("[green]Goodbye![/]")
            break
        else:
            prompts.error("Invalid option.")

if __name__ == "__main__":
    try:
        landing_menu()
    except KeyboardInterrupt:
        # This catches the Ctrl+C command and exits cleanly
        print("\n\n  [bold cyan]›[/] [dim]Vault closed securely. Goodbye![/]")


        
