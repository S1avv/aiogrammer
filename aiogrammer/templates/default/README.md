# Professional bot on Aiogram 3

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

## Structure

```.

├── src/
│   ├── main.py        # entry point, handler registration, launch
│   ├── config.py      # pydantic-settings for configuration
│   └── logger.py      # logging configuration
├── requirements.txt   # project dependencies
├── .env.example       # example environment variables
└── README.md          # brief documentation
```