# Aiogrammer ✨

![Demo](data/demo.gif)

A powerful template-based generator for building Telegram bots with aiogram

## Goals 🚀
- Create new projects instantly from curated templates
- Stay up to date with the latest aiogram versions
- Support database integrations, logging, admin tools, schedulers, and AI integrations

## Templates 🧰
- default — Professional Aiogram 3 starter scaffold. See details in the Templates Reference below → [jump to details](#templates-reference)
- support — Simple helpdesk bot with ticket capture and forwarding to a support chat → [jump to details](#templates-reference)
- quiz — Quiz/Trivia bot with async SQLAlchemy ORM and local SQLite database → [jump to details](#templates-reference)
- minimal — Minimal Aiogram 3 starter without extra boilerplate → [jump to details](#templates-reference)

## Modules 🧩
- admin — Admin panel with access control and a basic inline menu. See details in the Modules Reference below → [jump to details](#modules-reference)
- antispam — Simple anti-spam middleware limiting messages per time window → [jump to details](#modules-reference)
- pagination — Inline pagination helpers and demo with navigation extras → [jump to details](#modules-reference)
- i18n — Simple localization middleware with JSON locales and fallback → [jump to details](#modules-reference)
- security — Helpers for secrets validation and log redaction → [jump to details](#modules-reference)

## Usage 🧭
- List templates:
  - aiogrammer list-templates
- Create a project from a template:
  - aiogrammer add-template -t default -n my-bot -o .
- List modules:
  - aiogrammer list-modules
- Add a module to a project:
  - aiogrammer add-module -m admin -p my-bot

## Installation 💾

Clone the repository

```bash
git clone https://github.com/S1avv/aiogrammer.git

# Go to your project folder
cd aiogrammer

# Create a virtual environment
poetry shell

# Install the required dependencies
poetry install
```

You can install and run from local sources using pipx.

- Linux/macOS:
  - chmod +x ./install_and_run.sh
  - ./install_and_run.sh

- Windows (PowerShell):
  - Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  - .\install_and_run.ps1

After installation, verify: ✅
- aiogrammer --help

## Reference 📚

### Templates Reference 📦
#### default
- Summary: Basic professionally designed bot template on Aiogram 3
- Entrypoint: src.main:main
- Includes:
  - src/main.py — entry point, handler registration, launch
  - src/config.py — configuration via pydantic-settings
  - src/logger.py — logging configuration
  - requirements.txt — dependencies
  - .env.example — environment variables example
  - README.md — brief template docs

#### support
- Summary: Simple helpdesk bot that collects a short ticket and forwards it to SUPPORT_CHAT_ID
- Entrypoint: src.main:main
- Env:
  - BOT_TOKEN — bot token
  - SUPPORT_CHAT_ID — target chat ID where the ticket is forwarded
- Includes:
  - src/main.py — start, inline button, FSM flow (topic, description), forwarding
  - src/config.py — pydantic-settings (BOT_TOKEN, SUPPORT_CHAT_ID)
  - src/logger.py — logging configuration
  - requirements.txt — dependencies
  - .env.example — env variables example
  - README.md — template docs

#### quiz
- Summary: Quiz/Trivia bot template with async SQLAlchemy ORM and local SQLite db
- Entrypoint: src.main:main
- Env:
  - BOT_TOKEN — bot token
  - DATABASE_URL — database DSN (default sqlite+aiosqlite:///./quiz.db)
- Includes:
  - src/main.py — commands /start, /quiz, /addq; FSM for answering; score update
  - src/db.py — async engine, session factory, init_models
  - src/models.py — SQLAlchemy models (User, Question)
  - src/repo.py — simple repository helpers
  - src/config.py — pydantic-settings (BOT_TOKEN, DATABASE_URL)
  - src/logger.py — logging configuration
  - requirements.txt — dependencies
  - .env.example — env variables example
  - README.md — template docs

#### minimal
- Summary: Minimal Aiogram 3 starter without extra boilerplate
- Entrypoint: src.main:main
- Env:
  - BOT_TOKEN — bot token
- Includes:
  - src/main.py — minimal entry point and /start handler
  - requirements.txt — dependencies
  - .env.example — env variables example
  - README.md — template docs

### Modules Reference 🧩
#### admin
- Summary: Admin module with access control and basic menu
- Provides:
  - /admin command with ADMIN_IDS check
  - Inline keyboard with sections: Dashboard, Users, Settings
  - Callback handling for admin:<section>
- Files:
  - handlers.py — handlers with access check
  - keyboards.py — inline keyboard factory
  - config.py — ADMIN_IDS configuration
  - __init__.py — exports router

#### antispam
- Summary: Simple anti-spam middleware limiting messages per user in a short time window
- Provides:
  - Middleware AntiSpamMiddleware to plug into Dispatcher
- Files:
  - middleware.py — core rate-limiting logic
  - __init__.py — exports middleware and router
  - module.yaml — manifest

#### pagination
- Summary: Inline pagination helpers and demo with various navigation extras
- Provides:
  - /pagination_demo command with inline pagination over a demo list
  - Utility builder paginate_keyboard(page, total_pages, prefix, extra_buttons)
- Files:
  - handlers.py — demo command and callbacks
  - utils.py — paginate_keyboard, chunks, clamp
  - __init__.py — exports router and utils
  - module.yaml — manifest

#### i18n
- Summary: Simple localization middleware with JSON locales and fallback
- Provides:
  - I18nMiddleware to attach to Dispatcher
  - load_locales utility to load JSON dictionaries
  - `i18n` in handler data for translations
- Files:
  - middleware.py — middleware and translation utilities
  - locales/*.json — language dictionaries
  - __init__.py — exports I18n, I18nMiddleware, load_locales
  - module.yaml — manifest

#### security
- Summary: Helpers for secrets validation and log redaction
- Provides:
  - RedactFilter to mask tokens in logs
  - validate_env([VARS]) for required environment variables
  - mask_text(text) utility for manual sanitization
- Files:
  - utils.py — masking, filter, env validation
  - __init__.py — exports mask_text, RedactFilter, validate_env
  - module.yaml — manifest

## Custom local templates and modules 🧑‍💻

You can add your own local templates and modules to Aiogrammer.

- Register a template from a local folder:
  - aiogrammer new-template -s /path/to/template -n my-template
- Register a module from a local folder:
  - aiogrammer new-module -s /path/to/module -n my-module

What these commands do:
- Copy the specified folder into the project directory: `aiogrammer/templates/<name>` or `aiogrammer/modules/<name>`
- Create a manifest file (template.yaml or module.yaml) and prompt you to enter a short Summary and a Version
- After that, the item appears in the lists: aiogrammer list-templates or aiogrammer list-modules
- Use the --force flag to overwrite an existing template/module

Tip 💡: if you use aiogrammer installed via pipx from local sources, reinstall the package so the CLI sees new files:
- pipx reinstall aiogrammer