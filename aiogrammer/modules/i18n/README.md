# I18n Module

Simple localization middleware with JSON locales and fallback.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m i18n -p <your-project>
```
2) Prepare locales
- Put JSON files under `modules/i18n/locales/`, e.g. `en.json`, `ru.json`
- Each file is a flat key-value dictionary: `{ "start.welcome": "Welcome, {name}!" }`

3) Wire middleware
- Load locales and attach middleware to Dispatcher
```python
from pathlib import Path
from modules.i18n import I18n, I18nMiddleware, load_locales

locales_dir = Path(__file__).resolve().parent / "modules" / "i18n" / "locales"
translations = load_locales(locales_dir)
i18n = I18n(translations, fallback="en")
dp.message.middleware(I18nMiddleware(i18n))
```

4) Use in handlers
- Access `i18n` from handler `data` and translate keys
```python
from aiogram import Router

router = Router()

@router.message()
async def start(message, i18n):
    await message.answer(i18n.t("start.welcome", name=message.from_user.first_name))
```

## API
- `load_locales(root: Path) -> dict[str, dict[str, str]]` — load JSON dictionaries
- `I18n.for_locale(locale) -> I18nLocale` — pick table by language code
- `I18nLocale.t(key, **kwargs) -> str` — translate and format

## Files
- `middleware.py` — middleware and translation utilities
- `locales/*.json` — language dictionaries
- `__init__.py` — exports `I18n`, `I18nMiddleware`, `load_locales`
- `module.yaml` — manifest