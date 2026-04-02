import secrets
import string
import ui.prompts as prompts
import ui.tui as tui

def generate_password(length: int = 12, include_upper: bool = True, include_lower: bool = True,
                     include_digits: bool = True, include_symbols: bool = True) -> str:
    """Generate a secure random password."""
    chars = ""
    if include_upper:
        chars += string.ascii_uppercase
    if include_lower:
        chars += string.ascii_lowercase
    if include_digits:
        chars += string.digits
    if include_symbols:
        chars += string.punctuation

    if not chars:
        return ""

    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

def password_generator_menu():
    """Menu for password generation options."""
    tui.clear()
    tui.console.print(tui.Panel("[bold cyan]Password Generator[/]", expand=False))
    tui.console.print("  [yellow]1.[/] Generate Random Password")
    tui.console.print("  [yellow]2.[/] Back to Main Menu\n")

    choice = prompts.prompt("Choose").strip()

    if choice == "1":
        try:
            length = int(prompts.prompt("Password length (default 12)", default="12"))
            include_upper = prompts.confirm("Include uppercase letters?")
            include_lower = prompts.confirm("Include lowercase letters?")
            include_digits = prompts.confirm("Include digits?")
            include_symbols = prompts.confirm("Include symbols?")

            password = generate_password(length, include_upper, include_lower, include_digits, include_symbols)
            if password:
                tui.console.print(f"\n[green]Generated Password:[/] {password}")
                if prompts.confirm("Copy to clipboard?"):
                    import pyperclip
                    pyperclip.copy(password)
                    prompts.success("Copied to clipboard.")
            else:
                prompts.error("No character types selected.")
        except ValueError:
            prompts.error("Invalid length.")
    elif choice == "2":
        return
    else:
        prompts.error("Invalid option.")

    input("\nPress Enter to continue...")
    password_generator_menu()