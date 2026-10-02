from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "database" / "music.db"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"

APP_NAME = "WLZBI Music API"
VERSION = "1.0.0"

HOST = "0.0.0.0"
PORT = 8000

CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
DATABASE_PATH.parent.mkdir(exist_ok=True)