# Multibot on Aiogram 3

Run multiple bots from one application with shared handlers.

## Launch

1) Create a virtual environment and install dependencies:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Create a `.env` file (you can copy it from `.env.example`) and specify `BOT_TOKENS` as a comma-separated list of tokens. Alternatively, set a single `BOT_TOKEN`.

3) Launch:

```
python -m src.main
```

## What is inside

- `src/main.py` — spins up multiple bots concurrently and registers shared handlers
- `requirements.txt` — dependencies
- `.env.example` — environment variables example
- `README.md` — brief template docs