# Aiogrammer

Aiogrammer is a powerful template-based generator for building Telegram bots with aiogram. This MVP provides a clean, professional, and simple file structure to kickstart development without any source code yet.

## Goals
- Create new projects instantly from curated templates
- Stay up to date with the latest aiogram versions
- Support database integrations, logging, admin tools, schedulers, and AI integrations

## Templates
- default — Professional Aiogram 3 starter scaffold. See details in the Templates Reference below → [jump to details](#templates-reference)

## Modules
- admin — Admin panel with access control and a basic inline menu. See details in the Modules Reference below → [jump to details](#modules-reference)

## Usage
- List templates:
  - aiogrammer list-templates
- Create a project from a template:
  - aiogrammer add-template -t default -n my-bot -o .
- List modules:
  - aiogrammer list-modules
- Add a module to a project:
  - aiogrammer add-module -m admin -p my-bot

## Installation

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

After installation, verify:
- aiogrammer --help

## Reference

### Templates Reference
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

### Modules Reference
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