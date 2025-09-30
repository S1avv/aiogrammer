# Quiz/Trivia Bot (Aiogram 3 + SQLAlchemy + SQLite)

A minimal quiz bot that stores users and quiz questions in local SQLite using async SQLAlchemy 2.x.

## Features
- /start welcome and registration of user in DB
- /addq — add a question (admin/simple demo)
- /quiz — ask a random question, check answer, update score
- Clean async session management and models

## Setup
1) Create venv and install deps
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```
2) Create `.env` with BOT_TOKEN and DATABASE_URL
3) Run:
```
python -m src.main
```

Commands:
- /quiz — ask a random question
- /addq <question> | <answer> — add a question quickly

## Structure
```
.
├── src/
│   ├── main.py         # entry, handlers
│   ├── db.py           # engine, session, init
│   ├── models.py       # SQLAlchemy models
│   ├── repo.py         # simple repository helpers
│   ├── config.py       # pydantic-settings
│   └── logger.py       # logging
├── requirements.txt
├── .env.example
└── README.md
```