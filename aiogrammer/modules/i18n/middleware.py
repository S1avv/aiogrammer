import json
import pathlib
from typing import Dict, Any

try:
    from aiogram import BaseMiddleware
except Exception:
    from aiogram.dispatcher.middlewares.base import BaseMiddleware


class I18n:
    def __init__(self, translations: Dict[str, Dict[str, str]], fallback: str = "en") -> None:
        self.translations = translations
        self.fallback = fallback

    def for_locale(self, locale: str | None) -> "I18nLocale":
        lang = (locale or self.fallback).split("-", 1)[0]
        table = self.translations.get(lang) or self.translations.get(self.fallback, {})
        return I18nLocale(table)


class I18nLocale:
    def __init__(self, table: Dict[str, str]) -> None:
        self.table = table

    def t(self, key: str, **kwargs: Any) -> str:
        value = self.table.get(key, key)
        try:
            return value.format(**kwargs)
        except Exception:
            return value


def load_locales(root: pathlib.Path) -> Dict[str, Dict[str, str]]:
    """Load JSON locale files from a directory into translations mapping.

    Returns dict like {"en": {"key": "value"}, "ru": {...}}.
    Invalid files are skipped silently.
    """
    translations: Dict[str, Dict[str, str]] = {}
    try:
        for file in root.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                translations[file.stem] = data if isinstance(data, dict) else {}
            except Exception:
                pass
    except Exception:
        pass
    return translations


def load_locales(root: pathlib.Path) -> Dict[str, Dict[str, str]]:
    translations: Dict[str, Dict[str, str]] = {}
    for lang_file in (root / "locales").glob("*.json"):
        try:
            translations[lang_file.stem] = json.loads(lang_file.read_text(encoding="utf-8"))
        except Exception:
            translations[lang_file.stem] = {}
    return translations


class I18nMiddleware(BaseMiddleware):
    def __init__(self, i18n: I18n) -> None:
        super().__init__()
        self.i18n = i18n

    async def __call__(self, handler, event, data):
        lang_code = None
        try:
            user = getattr(event, "from_user", None)
            if user is not None:
                lang_code = getattr(user, "language_code", None)
        except Exception:
            pass

        data["i18n"] = self.i18n.for_locale(lang_code)
        return await handler(event, data)