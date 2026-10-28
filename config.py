import os
from pathlib import Path

ENV_FILE = Path.home() / ".agents" / "env"

if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

BASE_URL = os.environ.get("BASE_URL", "http://localhost:30000/v1")
API_KEY = os.environ.get("API_KEY", "EMPTY")
MODEL = os.environ.get("MODEL", "Qwen/Qwen3-0.6B")

CONTEXT_WINDOW = int(os.environ.get("CONTEXT_WINDOW", 4096))
COMPACT_AT = 0.85
COMPACT_TO = 0.35