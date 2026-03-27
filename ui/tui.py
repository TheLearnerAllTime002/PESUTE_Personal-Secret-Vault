import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich.padding import Padding
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich import box

console = Console()

# ── palette ───────────────────────────────────────────────────────────────────
P = {
    "border"  : "bright_cyan",
    "title"   : "bold bright_white",
    "label"   : "bold cyan",
    "value"   : "bright_white",
    "dim"     : "dim white",
    "success" : "bold bright_green",
    "error"   : "bold bright_red",
    "warn"    : "bold yellow",
    "num"     : "bold yellow",
    "locked"  : "bold red",
    "badge_g" : "bold black on green",
    "badge_r" : "bold white on red",
    "badge_y" : "bold black on yellow",
    "badge_c" : "bold black on cyan",
    "section" : "bold cyan",
}

BANNER = r"""
  ____                 _       
 |  _ \ ___  ___ _   _| |_ ___ 
 | |_) / _ \/ __| | | | __/ _ \
 |  __/  __/\__ \ |_| | ||  __/
 |_|   \___||___/\__,_|\__\___|
"""

CATEGORY_COLORS = {
    "email"   : "cyan",
    "social"  : "magenta",
    "work"    : "blue",
    "finance" : "green",
    "gaming"  : "yellow",
    "none"    : "dim white",
}


def _cat_color(cat: str) -> str:
    return CATEGORY_COLORS.get(cat.lower(), "bright_white")


# ── screen helpers ────────────────────────────────────────────────────────────

def clear():
    console.clear()


def loading(message: str = "Loading vault..."):
    with Live(Spinner("dots", text=f"[cyan]{message}[/]"), console=console, transient=True):
        time.sleep(0.6)


# ── header ────────────────────────────────────────────────────────────────────

def header(is_fake: bool = False):
    console.clear()
    loading("Unlocking vault...")

    if is_fake:
        mode_line = Text("  ⚠  DECOY VAULT  ⚠  ", style="bold yellow on dark_orange", justify="center")
    else:
        mode_line = Text(
            "Personal Secret Vault  •  Secure. Private. Yours.",
            style="dim white", justify="center"
        )

    banner = Text(BANNER, style="bold cyan", justify="center")
    content = Text.assemble(banner, "\n", mode_line, "\n")

    console.print(Panel(
        Align.center(content),
        border_style=P["border"],
        padding=(0, 8),
        subtitle="[dim cyan]v2.0  •  AES-256 Encrypted[/]",
    ))
    console.print()


# ── timer bar ─────────────────────────────────────────────────────────────────

def _timer_bar(time_left: float):
    total  = 60.0
    pct    = max(0.0, time_left / total)
    filled = int(pct * 30)
    empty  = 30 - filled

    if time_left > 30:
        color, bg = "bright_green", "green"
    elif time_left > 15:
        color, bg = "yellow", "yellow"
    else:
        color, bg = "bright_red", "red"

    bar   = f"[{color}]{'█' * filled}[/][dim white]{'░' * empty}[/]"
    secs  = f"[{color}]{int(time_left)}s[/]"
    label = f"[dim white]Session expires in[/] {secs}"

    console.print(Align.center(f"{bar}  {label}"))
    console.print()


# ── main menu ─────────────────────────────────────────────────────────────────

def menu(time_left: float = None):
    if time_left is not None:
        _timer_bar(time_left)

    vault_rows = [
        ("1", "Add Entry",          "bright_green"),
        ("2", "View Entries",       "bright_green"),
        ("3", "Delete Entry",       "bright_red"),
        ("4", "Search",             "bright_cyan"),
        ("5", "Copy Secret",        "bright_cyan"),
        ("6", "List Categories",    "bright_cyan"),
        ("7", "Edit / History",     "bright_yellow"),
    ]
    manage_rows = [
        ("8",  "Export  (Decrypted)", "yellow"),
        ("9",  "Backup  (Encrypted)", "yellow"),
        ("10", "Import",              "yellow"),
        ("11", "Change Password",     "magenta"),
        ("12", "Remove Password",     "magenta"),
        ("13", "Exit",                "bright_red"),
    ]

    def _table(rows, title_color="cyan"):
        t = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), expand=True)
        t.add_column("n", width=5,    no_wrap=True)
        t.add_column("o", min_width=20)
        for num, label, color in rows:
            t.add_row(
                f"[bold {color}]{num}.[/]",
                f"[{color}]{label}[/]",
            )
        return t

    left  = Panel(_table(vault_rows),  title="[bold bright_green] Vault [/]",  border_style="bright_green",  padding=(0, 2))
    right = Panel(_table(manage_rows), title="[bold bright_yellow] Manage [/]", border_style="bright_yellow", padding=(0, 2))

    console.print(Columns([left, right], equal=True, expand=True))
    console.print()


# ── search menu ───────────────────────────────────────────────────────────────

def search_menu():
    t = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style=P["label"],
        padding=(0, 3),
        expand=False,
    )
    t.add_column("Key",  style=P["num"],   width=5,  justify="center")
    t.add_column("Mode", style=P["value"], width=14)
    t.add_column("Description", style=P["dim"])

    rows = [
        ("1", "Title",     "Search entry titles only"),
        ("2", "Category",  "Filter by category"),
        ("3", "Any field", "Title + category + tags"),
        ("4", "Regex",     "Full regular expression"),
    ]
    for k, m, d in rows:
        t.add_row(k, m, d)

    console.print(Panel(
        t,
        title="[bold cyan] Search [/]",
        border_style="cyan",
        expand=False,
        padding=(0, 2),
    ))


# ── entry card ────────────────────────────────────────────────────────────────

def entry_card(num: int, entry: dict, locked: bool = False):
    title    = entry.get("title", "Untitled")
    category = entry.get("category", "none")
    tags     = entry.get("tags", [])
    secret   = entry.get("secret", "")
    notes    = entry.get("notes", "")
    created  = entry.get("created_at", "—")
    modified = entry.get("last_modified", "—")
    history  = entry.get("history", [])

    # ── badge strip ───────────────────────────────────────────────────────────
    badge_parts = []
    if locked:
        badge_parts.append(f"[{P['badge_r']}] LOCKED [/]")
    if history:
        badge_parts.append(f"[{P['badge_c']}] {len(history)} ver. [/]")
    cat_color = _cat_color(category)
    badge_parts.append(f"[bold {cat_color}] {category.upper()} [/]")
    badges = "  " + "  ".join(badge_parts) if badge_parts else ""

    # ── secret display ────────────────────────────────────────────────────────
    if locked:
        secret_display = f"[{P['locked']}]●●●●●●●●  PIN REQUIRED[/]"
    else:
        secret_display = f"[bright_white]{secret}[/]"

    # ── tags display ──────────────────────────────────────────────────────────
    if tags:
        tags_display = "  ".join(f"[dim cyan]#{t}[/]" for t in tags)
    else:
        tags_display = "[dim white]—[/]"

    # ── grid ──────────────────────────────────────────────────────────────────
    grid = Table.grid(padding=(0, 3))
    grid.add_column(style=P["label"], width=11, no_wrap=True)
    grid.add_column()

    grid.add_row("[bold cyan]Secret[/]",   secret_display)
    grid.add_row("[bold cyan]Tags[/]",     tags_display)
    if notes:
        grid.add_row("[bold cyan]Notes[/]", f"[italic dim white]{notes}[/]")
    grid.add_row(
        "[dim]Created[/]",
        f"[dim white]{created}[/]  [dim]Modified[/]  [dim white]{modified}[/]",
    )
    if history:
        grid.add_row("[dim]History[/]", f"[dim white]{len(history)} previous version(s)[/]")

    console.print(Panel(
        grid,
        title=f"[bold yellow] #{num} [/][bold bright_white] {title} [/]{badges}",
        border_style="yellow",
        expand=False,
        padding=(0, 2),
    ))


# ── history table ─────────────────────────────────────────────────────────────

def history_table(history: list[dict]):
    t = Table(
        title="[bold cyan] Version History [/]",
        box=box.ROUNDED,
        border_style="cyan",
        header_style=P["label"],
        show_lines=True,
        expand=False,
    )
    t.add_column("#",          style=P["num"],   width=4,  justify="right")
    t.add_column("Old Secret", style=P["value"], min_width=24)
    t.add_column("Changed At", style=P["dim"],   min_width=22)

    for i, h in enumerate(reversed(history), 1):
        t.add_row(str(i), h.get("secret", ""), h.get("changed_at", "—"))

    console.print()
    console.print(Align.center(t))
    console.print()


# ── categories table ──────────────────────────────────────────────────────────

def categories_table(cats: list[tuple[str, int]]):
    t = Table(
        title="[bold cyan] Categories [/]",
        box=box.ROUNDED,
        border_style="cyan",
        header_style=P["label"],
        expand=False,
        padding=(0, 3),
    )
    t.add_column("Category", style=P["value"], min_width=16)
    t.add_column("Entries",  style=P["num"],   width=10, justify="right")
    t.add_column("Bar",      style=P["dim"],   min_width=20)

    max_count = max((c for _, c in cats), default=1)
    for name, count in cats:
        bar_len = int((count / max_count) * 20)
        color   = _cat_color(name)
        bar     = f"[{color}]{'█' * bar_len}[/][dim white]{'░' * (20 - bar_len)}[/]"
        t.add_row(f"[{color}]{name}[/]", str(count), bar)

    console.print()
    console.print(Align.center(t))
    console.print()


# ── status messages ───────────────────────────────────────────────────────────

def success(text: str):
    console.print()
    console.print(Panel(
        f"[{P['success']}]  ✓  {text}[/]",
        border_style="green",
        expand=False,
        padding=(0, 2),
    ))
    console.print()


def error(text: str):
    console.print()
    console.print(Panel(
        f"[{P['error']}]  ✗  {text}[/]",
        border_style="red",
        expand=False,
        padding=(0, 2),
    ))
    console.print()


def warn(text: str):
    console.print()
    console.print(Panel(
        f"[{P['warn']}]  ⚠  {text}[/]",
        border_style="yellow",
        expand=False,
        padding=(0, 2),
    ))
    console.print()


def info(text: str):
    console.print(f"  [cyan]›[/] [white]{text}[/]")


def section(title: str):
    console.print()
    console.print(Rule(
        f"[bold cyan]  {title}  [/]",
        style="cyan",
        characters="─",
    ))
    console.print()


def rule(title: str = ""):
    section(title)


# ── prompts ───────────────────────────────────────────────────────────────────

def prompt(text: str) -> str:
    return Prompt.ask(f"\n  [bold cyan]›[/] [cyan]{text}[/]")


def confirm(text: str) -> bool:
    return Confirm.ask(f"\n  [bold yellow]?[/] [yellow]{text}[/]")
