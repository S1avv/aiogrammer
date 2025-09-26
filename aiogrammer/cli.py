import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path
import shutil
import yaml

from .ui import brand_panel, templates_table, modules_table
from .templates import discover_templates, discover_modules
from .copier import copy_template, copy_module

app = typer.Typer(help="aiogrammer — Aiogram Template Generator")
console = Console()


@app.command("list-templates", help="List available templates")
def list_templates():
    templates = discover_templates()
    console.print(brand_panel())
    if not templates:
        console.print("[yellow]No templates found.[/yellow]")
        raise typer.Exit(code=0)
    console.print(templates_table(templates))


@app.command("add-template", help="Create a new project from a template")
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


@app.command("add-module", help="Add a ready-to-use module into a project")
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


# New commands: create custom template/module from a source folder into local repo
@app.command("new-template", help="Register a custom template from a local folder")
def new_template(
    source: Path = typer.Option(..., "--source", "-s", help="Path to the source template folder"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Template name (defaults to source folder name)"),
    force: bool = typer.Option(False, "--force", help="Overwrite if target already exists"),
):
    if not source.exists() or not source.is_dir():
        console.print(f"[red]Source folder not found or not a directory:[/red] {source}")
        raise typer.Exit(1)

    repo_root = Path(__file__).resolve().parents[1]
    templates_root = repo_root / "templates"
    templates_root.mkdir(parents=True, exist_ok=True)

    template_name = name or source.name
    dest = templates_root / template_name

    if dest.exists():
        if not force:
            console.print(f"[red]Template '{template_name}' already exists at {dest}. Use --force to overwrite.[/red]")
            raise typer.Exit(1)
        shutil.rmtree(dest)

    shutil.copytree(source, dest)

    version = Prompt.ask("Version", default="0.1.0")
    summary = Prompt.ask("Summary", default=f"Custom template: {template_name}")

    manifest = {
        "name": template_name,
        "version": version,
        "summary": summary,
        "category": "custom",
    }
    (dest / "template.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")

    console.print(f"[green]Custom template created at:[/green] {dest}")


@app.command("new-module", help="Register a custom module from a local folder")
def new_module(
    source: Path = typer.Option(..., "--source", "-s", help="Path to the source module folder"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Module name (defaults to source folder name)"),
    force: bool = typer.Option(False, "--force", help="Overwrite if target already exists"),
):
    if not source.exists() or not source.is_dir():
        console.print(f"[red]Source folder not found or not a directory:[/red] {source}")
        raise typer.Exit(1)

    pkg_root = Path(__file__).resolve().parent
    modules_root = pkg_root / "modules"
    modules_root.mkdir(parents=True, exist_ok=True)

    module_name = name or source.name
    dest = modules_root / module_name

    if dest.exists():
        if not force:
            console.print(f"[red]Module '{module_name}' already exists at {dest}. Use --force to overwrite.[/red]")
            raise typer.Exit(1)
        shutil.rmtree(dest)

    shutil.copytree(source, dest)

    version = Prompt.ask("Version", default="0.1.0")
    summary = Prompt.ask("Summary", default=f"Custom module: {module_name}")

    manifest = {
        "name": module_name,
        "version": version,
        "summary": summary,
    }
    (dest / "module.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")

    console.print(f"[green]Custom module created at:[/green] {dest}")


@app.command("list-modules", help="List available modules")
def list_modules():
    modules = discover_modules()
    console.print(brand_panel())
    if not modules:
        console.print("[yellow]No modules found.[/yellow]")
        raise typer.Exit(code=0)
    console.print(modules_table(modules))


if __name__ == "__main__":
    app()