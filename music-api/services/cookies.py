import atexit
import os
from pathlib import Path
import tempfile
import threading


APP_DIR = Path(__file__).resolve().parents[1]
_environment_cookie_path = None
_environment_cookie_lock = threading.Lock()


def _cleanup_environment_cookie_file():
    if _environment_cookie_path is not None:
        _environment_cookie_path.unlink(missing_ok=True)


atexit.register(_cleanup_environment_cookie_file)


def _get_environment_cookie_file():
    global _environment_cookie_path

    contents = os.environ.get("YOUTUBE_COOKIES")
    if not contents:
        return None
    if not contents.strip():
        raise ValueError("YOUTUBE_COOKIES is set but empty.")

    headers = {"# Netscape HTTP Cookie File", "# HTTP Cookie File"}
    if not any(line.strip() in headers for line in contents.splitlines()):
        raise ValueError(
            "YOUTUBE_COOKIES must contain a Netscape-format cookie file, "
            "including its Netscape cookie header."
        )

    with _environment_cookie_lock:
        if _environment_cookie_path is None:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                prefix="youtube-cookies-",
                suffix=".txt",
                delete=False,
            ) as cookie_file:
                cookie_file.write(contents)
                _environment_cookie_path = Path(cookie_file.name)

    return _environment_cookie_path


def cookie_options():
    """Resolve cookies on each request so a file can be added or replaced."""
    environment_path = _get_environment_cookie_file()
    if environment_path is not None:
        return {"cookiefile": str(environment_path)}

    for path in (APP_DIR / "cookis.txt", APP_DIR.parent / "cookis.txt"):
        if path.is_file():
            if path.stat().st_size == 0:
                raise ValueError("cookis.txt is empty. Provide valid Netscape-format YouTube cookies.")
            return {"cookiefile": str(path)}

    raise FileNotFoundError(
        "Missing cookis.txt. Place a Netscape-format YouTube cookie file "
        "in music-api/ or the project root."
    )