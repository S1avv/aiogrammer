from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

BRAND = "Aiogrammer"
SLOGAN = "Aiogram Template Generator"


def brand_panel() -> Panel:
    return Panel(f"[bold cyan]{BRAND}[/bold cyan]\n[dim]{SLOGAN}[/dim]", title="🚀", border_style="cyan", box=box.ROUNDED)


def templates_table(templates: list[dict]) -> Table:
    table = Table(title="Available Templates", box=box.SIMPLE_HEAVY)
    table.add_column("Name", style="bold green")
    table.add_column("Category", style="magenta")
    table.add_column("Version", style="yellow")
    table.add_column("Summary", style="white")
    for t in templates:
        table.add_row(t.get("name", "-"), t.get("category", "-"), t.get("version", "-"), t.get("summary", "-"))
    return table

def modules_table(modules: list[dict]) -> Table:
    table = Table(title="Available Modules", box=box.SIMPLE_HEAVY)
    table.add_column("Name", style="bold green")
    table.add_column("Version", style="yellow")
    table.add_column("Summary", style="white")
    for m in modules:
        table.add_row(m.get("name", "-"), m.get("version", "-"), m.get("summary", "-"))
    return table