# Minimal bot on Aiogram 3

## Launch

1) Create a virtual environment and install dependencies:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Create a `.env` file (you can copy it from `.env.example`) and specify `BOT_TOKEN`.

3) Launch:

```
python -m src.main
```

## What is inside

- Minimal `src/main.py` with /start handler only
- No extra configs or logging — pure basics
- `python-dotenv` used to load `.env`