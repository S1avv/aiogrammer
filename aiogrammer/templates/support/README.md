# Support Bot (Aiogram 3)

A minimal support bot that collects user requests ("tickets") via a short dialog, stores context in FSM, and forwards the final ticket to a dedicated support chat.

## Features
- /start welcome and quick intro
- "Contact support" flow via FSM: ask for topic and description
- Attachments: if user sends a photo/document during the flow, bot includes a link/note
- Forward the final ticket to SUPPORT_CHAT_ID
- Simple logging and clean project structure

## Setup
1) Create venv and install dependencies:
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

2) Create `.env` with:
- BOT_TOKEN
- SUPPORT_CHAT_ID (chat ID for forwarding tickets)

3) Run:
```
python -m src.main
```

## Structure
```
.
├── src/
│   ├── main.py        # entry point, handlers, FSM flow
│   ├── config.py      # pydantic-settings config (BOT_TOKEN, SUPPORT_CHAT_ID)
│   └── logger.py      # logging
├── requirements.txt   # dependencies
├── .env.example       # env sample
└── README.md          # this file
```