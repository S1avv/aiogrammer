import logging
import os
import re


_TOKEN_PATTERNS = [
    re.compile(r"\b\d{8,}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b", re.IGNORECASE),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
]


def mask_text(text: str) -> str:
    masked = text
    for pat in _TOKEN_PATTERNS:
        masked = pat.sub("***REDACTED***", masked)
    return masked


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if isinstance(record.msg, str):
                record.msg = mask_text(record.msg)
            if record.args:
                record.args = tuple(mask_text(str(a)) for a in record.args)
        except Exception:
            pass
        return True


def validate_env(keys: list[str]) -> None:
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")