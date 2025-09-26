import os
import pathlib
import yaml
from typing import List, Dict, Optional

try:
    from importlib.resources import files, as_file
except Exception:
    files = None
    as_file = None


def _env_templates_root() -> Optional[pathlib.Path]:
    env = os.getenv("AIOGRAMMER_TEMPLATES_DIR")
    if env:
        p = pathlib.Path(env).expanduser().resolve()
        if p.exists():
            return p
    return None


def _packaged_templates_root() -> Optional[pathlib.Path]:
    if files is None or as_file is None:
        return None
    try:
        pkg_dir = files("aiogrammer").joinpath("templates")
        with as_file(pkg_dir) as concrete:
            p = pathlib.Path(concrete)
            if p.exists():
                return p
    except Exception:
        return None
    return None


def _dev_templates_root() -> Optional[pathlib.Path]:
    project_root = pathlib.Path(__file__).resolve().parents[1]
    p = project_root / "templates"
    return p if p.exists() else None


def _resolve_templates_root() -> Optional[pathlib.Path]:
    return _env_templates_root() or _packaged_templates_root() or _dev_templates_root()


def discover_templates() -> List[Dict]:
    templates: List[Dict] = []
    root = _resolve_templates_root()
    if not root:
        return templates

    for manifest in root.rglob("template.yaml"):
        try:
            data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
            data["path"] = str(manifest.parent)
            templates.append(data)
        except Exception:
            templates.append({
                "name": manifest.parent.name,
                "version": "?",
                "summary": "Invalid manifest",
                "category": "?",
                "path": str(manifest.parent),
            })
    return sorted(templates, key=lambda x: (x.get("category", ""), x.get("name", "")))


def _env_modules_root() -> Optional[pathlib.Path]:
    env = os.getenv("AIOGRAMMER_MODULES_DIR")
    if env:
        p = pathlib.Path(env).expanduser().resolve()
        if p.exists():
            return p
    return None


def _packaged_modules_root() -> Optional[pathlib.Path]:
    if files is None or as_file is None:
        return None
    try:
        pkg_dir = files("aiogrammer").joinpath("modules")
        with as_file(pkg_dir) as concrete:
            p = pathlib.Path(concrete)
            if p.exists():
                return p
    except Exception:
        return None
    return None


def _dev_modules_root() -> Optional[pathlib.Path]:
    p = pathlib.Path(__file__).resolve().parent / "modules"
    return p if p.exists() else None


def _resolve_modules_root() -> Optional[pathlib.Path]:
    return _env_modules_root() or _packaged_modules_root() or _dev_modules_root()


def discover_modules() -> List[Dict]:
    """Discover available modules in modules root.

    Module manifest file is 'module.yaml'. Returns metadata dicts with 'path'.
    """
    modules: List[Dict] = []
    root = _resolve_modules_root()
    if not root:
        return modules

    for manifest in root.rglob("module.yaml"):
        try:
            data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
            data["path"] = str(manifest.parent)
            modules.append(data)
        except Exception:
            modules.append({
                "name": manifest.parent.name,
                "version": "?",
                "summary": "Invalid manifest",
                "path": str(manifest.parent),
            })
    return sorted(modules, key=lambda x: x.get("name", ""))