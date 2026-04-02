import os
import shutil
import ui.prompts as prompts
import ui.tui as tui
from core import storage
from core.logger import log

def export_to_csv(username: str, cipher, fake: bool = False):
    """Export vault entries to CSV format."""
    entries = storage.load(username, cipher, fake)
    if not entries:
        prompts.error("Vault is empty.")
        return

    filename = prompts.prompt("CSV filename (without extension)", default="vault_export")
    filepath = f"{filename}.csv"

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            import csv
            fieldnames = ['title', 'secret', 'category', 'tags', 'notes', 'added', 'last_modified']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow({
                    'title': entry['title'],
                    'secret': entry['secret'],
                    'category': entry.get('category', ''),
                    'tags': ', '.join(entry.get('tags', [])),
                    'notes': entry.get('notes', ''),
                    'added': entry.get('added', ''),
                    'last_modified': entry.get('last_modified', '')
                })
        prompts.success(f"Exported to {filepath}.")
        log(f"EXPORT: {username} exported vault to CSV")
    except Exception as e:
        prompts.error(f"Export failed: {str(e)}")

def import_from_csv(username: str, cipher, fake: bool = False):
    """Import entries from CSV file."""
    filepath = prompts.prompt("CSV file path")
    if not os.path.exists(filepath):
        prompts.error("File not found.")
        return

    try:
        entries = storage.load(username, cipher, fake)
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            import csv
            reader = csv.DictReader(csvfile)
            imported_count = 0
            for row in reader:
                entry = {
                    'title': row['title'],
                    'secret': row['secret'],
                    'category': row.get('category', ''),
                    'tags': [t.strip() for t in row.get('tags', '').split(',') if t.strip()],
                    'notes': row.get('notes', ''),
                    'added': float(row.get('added', 0)),
                    'last_modified': float(row.get('last_modified', 0)),
                    'pin_hash': None,
                    'history': []
                }
                entries.append(entry)
                imported_count += 1

        storage.save(username, entries, cipher, fake)
        prompts.success(f"Imported {imported_count} entries.")
        log(f"IMPORT: {username} imported {imported_count} entries from CSV")
    except Exception as e:
        prompts.error(f"Import failed: {str(e)}")

def export_import_menu(username: str, cipher, fake: bool = False):
    """Menu for export/import operations."""
    tui.clear()
    tui.console.print(tui.Panel("[bold cyan]Export/Import[/]", expand=False))
    tui.console.print("  [yellow]1.[/] Export to CSV")
    tui.console.print("  [yellow]2.[/] Import from CSV")
    tui.console.print("  [yellow]3.[/] Back to Main Menu\n")

    choice = prompts.prompt("Choose").strip()

    if choice == "1":
        export_to_csv(username, cipher, fake)
    elif choice == "2":
        import_from_csv(username, cipher, fake)
    elif choice == "3":
        return
    else:
        prompts.error("Invalid option.")

    input("\nPress Enter to continue...")
    export_import_menu(username, cipher, fake)