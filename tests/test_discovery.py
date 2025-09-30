import pathlib

from aiogrammer.templates import discover_templates, discover_modules


def test_discover_templates_contains_known():
    templates = discover_templates()
    names = {t.get("name") for t in templates}
    assert {"default", "support", "quiz"}.issubset(names)

    for t in templates:
        p = pathlib.Path(t["path"]).resolve()
        assert p.exists()
        assert (p / "template.yaml").exists() or (p / "module.yaml").exists()


def test_discover_modules_contains_known():
    modules = discover_modules()
    names = {m.get("name") for m in modules}
    assert {"admin", "antispam", "pagination"}.issubset(names)

    for m in modules:
        p = pathlib.Path(m["path"]).resolve()
        assert p.exists()
        assert (p / "module.yaml").exists()