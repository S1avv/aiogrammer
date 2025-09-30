# Security Module

Helpers for secrets validation and log redaction to improve safety.

## Install into your project
1) Add module via CLI
```
aiogrammer add-module -m security -p <your-project>
```

## Usage
### Redact sensitive data in logs
Add a filter that masks token-like strings and bearer tokens.
```python
import logging
from modules.security import RedactFilter

logger = logging.getLogger()
logger.addFilter(RedactFilter())

logger.info("Starting bot with token %s", "123456789:ABCDEF...")
# -> message will be logged with ***REDACTED***
```

### Validate required environment variables
Fail-fast if critical variables are missing.
```python
import os
from modules.security import validate_env

validate_env(["BOT_TOKEN"])  # raises RuntimeError if not set
```

### Mask text manually
Sanitize strings before printing or exposing.
```python
from modules.security import mask_text

safe = mask_text("Bearer abc.def.ghi")  # -> "***REDACTED***"
```

## API
- `mask_text(text: str) -> str` — replace secrets with `***REDACTED***`
- `RedactFilter(logging.Filter)` — logging filter that redacts sensitive tokens
- `validate_env(keys: list[str]) -> None` — raise if any env var is missing

## Files
- `utils.py` — masking, filter, env validation
- `__init__.py` — exports `mask_text`, `RedactFilter`, `validate_env`
- `module.yaml` — manifest