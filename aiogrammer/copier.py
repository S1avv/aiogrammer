import shutil
import pathlib
from typing import Dict


def copy_template(target_dir: pathlib.Path, template: Dict) -> None:
    src = pathlib.Path(template["path"]).resolve()
    if not src.exists():
        raise FileNotFoundError(f"Template path not found: {src}")

    target_dir.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        if item.name in {"template.yaml", "module.yaml"}:
            continue
        dest = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)


def copy_module(project_dir: pathlib.Path, module: Dict) -> pathlib.Path:
    """Copy a module into project_dir/modules/<module_name>.

    Skips module.yaml manifest. Fails if target already exists.
    """
    src = pathlib.Path(module["path"]).resolve()
    if not src.exists():
        raise FileNotFoundError(f"Module path not found: {src}")

    name = module.get("name") or src.name
    modules_root = pathlib.Path(project_dir).resolve() / "modules"
    target = modules_root / name
    if target.exists():
        raise FileExistsError(f"Module '{name}' already exists at {target}")

    modules_root.mkdir(parents=True, exist_ok=True)

    init_file = modules_root / "__init__.py"
    if not init_file.exists():
        init_file.write_text("# namespace for project modules\n", encoding="utf-8")


    target.mkdir(parents=True, exist_ok=False)

    for item in src.iterdir():
        if item.name in {"module.yaml", "template.yaml"}:
            continue
        dest = target / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    return target