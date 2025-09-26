import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path

from .ui import brand_panel, templates_table, modules_table
from .templates import discover_templates, discover_modules
from .copier import copy_template, copy_module

app = typer.Typer(help="aiogrammer — Aiogram Template Generator")
console = Console()


@app.command("list-templates")
def list_templates():
    templates = discover_templates()
    console.print(brand_panel())
    if not templates:
        console.print("[yellow]No templates found.[/yellow]")
        raise typer.Exit(code=0)
    console.print(templates_table(templates))


@app.command("add-template")
def add_template(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Project folder name (defaults to template name)"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template name"),
    output: Path = typer.Option(Path.cwd(), "--output", "-o", help="Output directory"),
):
    templates = discover_templates()
    if not templates:
        console.print("[red]No templates available.[/red]")
        raise typer.Exit(1)

    if not template:
        console.print("Select a template:")
        names = [t["name"] for t in templates]
        template = Prompt.ask("Template", choices=names, default=names[0])

    chosen = next((t for t in templates if t["name"] == template), None)
    if not chosen:
        console.print(f"[red]Template not found:[/red] {template}")
        raise typer.Exit(1)

    folder_name = name or chosen["name"]
    target = output / folder_name
    copy_template(target, chosen)
    console.print(f"[green]Project initialized at:[/green] {target}")


@app.command("add-module")
def add_module(
    module: Optional[str] = typer.Option(None, "--module", "-m", help="Module name to add"),
    project_dir: Path = typer.Option(Path.cwd(), "--project", "-p", help="Project root to add a module to"),
):
    modules = discover_modules()
    if not modules:
        console.print("[red]No modules available.[/red]")
        raise typer.Exit(1)

    if not module:
        names = [m["name"] for m in modules]
        module = Prompt.ask("Module", choices=names, default=names[0])

    chosen = next((m for m in modules if m["name"] == module), None)
    if not chosen:
        console.print(f"[red]Module not found:[/red] {module}")
        raise typer.Exit(1)

    try:
        created = copy_module(project_dir, chosen)
        console.print(f"[green]Module added:[/green] {created}")
        console.print("\nTo include the module, import router in your app:\n\n    from modules.{0} import router\n    dp.include_router(router)\n".format(chosen["name"]))
    except FileExistsError as e:
        console.print(f"[yellow]{e}[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Failed to add module:[/red] {e}")
        raise typer.Exit(1)


@app.command("list-modules")
def list_modules():
    modules = discover_modules()
    console.print(brand_panel())
    if not modules:
        console.print("[yellow]No modules found.[/yellow]")
        raise typer.Exit(code=0)
    console.print(modules_table(modules))


if __name__ == "__main__":
    app()