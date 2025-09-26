import pathlib

from aiogrammer.copier import copy_template, copy_module
from aiogrammer.templates import discover_templates, discover_modules


def _get_template_by_name(name: str):
    for t in discover_templates():
        if t.get("name") == name:
            return t
    raise AssertionError(f"Template '{name}' not found among: {[t.get('name') for t in discover_templates()]}")


def _get_module_by_name(name: str):
    for m in discover_modules():
        if m.get("name") == name:
            return m
    raise AssertionError(f"Module '{name}' not found among: {[m.get('name') for m in discover_modules()]}")


essential_template_files = (
    ("src", "main.py"),
)


essential_module_files = (
    "middleware.py",
    "handlers.py",
    "__init__.py",
)


def test_copy_template_copies_files(tmp_path):
    template = _get_template_by_name("quiz")

    dest = tmp_path / "mybot"
    copy_template(dest, template)

    assert dest.exists() and dest.is_dir()

    for parts in essential_template_files:
        assert (dest.joinpath(*parts)).exists()
    assert (dest / ".env.example").exists()
    assert (dest / "README.md").exists()
    assert not (dest / "template.yaml").exists()


def test_copy_module_copies_files(tmp_path):
    module = _get_module_by_name("antispam")

    project_root = tmp_path
    target = copy_module(project_root, module)

    assert target.exists() and target.is_dir()
    assert target.parent.name == "modules"

    assert not (target / "module.yaml").exists()

    assert any((target / fname).exists() for fname in essential_module_files)