import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHORDS_DIR = DATA_DIR / "chord_images"

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
# Свой HTTPS (ngrok, свой домен) — перекрывает остальное, если указан и валиден
WEB_APP_URL = (os.getenv("WEB_APP_URL", "") or "").strip().rstrip("/")
# Статический Mini App на GitHub Pages / Netlify — работает с телефона без вашего ПК
HOSTED_MINI_APP_URL = (os.getenv("HOSTED_MINI_APP_URL", "") or "").strip().rstrip("/")
HTTP_HOST = os.getenv("HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8080"))

# 1 = при пустом WEB_APP_URL поднять бесплатный туннель Cloudflare (без ngrok)
_auto = (os.getenv("AUTO_CLOUDFLARE_TUNNEL", "1") or "1").strip().lower()
AUTO_CLOUDFLARE_TUNNEL = _auto not in ("0", "false", "no", "off")

DATABASE_PATH = DATA_DIR / "bot.db"

# Если выбран другой порт (8080 занят), задаётся в run.py
_BIND_HTTP_PORT: int | None = None

# Подставляется при старте run.py (quick tunnel)
_RUNTIME_WEB_APP_URL: str | None = None


def set_bind_http_port(port: int | None) -> None:
    global _BIND_HTTP_PORT
    _BIND_HTTP_PORT = int(port) if port is not None else None


def effective_http_port() -> int:
    return _BIND_HTTP_PORT if _BIND_HTTP_PORT is not None else HTTP_PORT


def set_runtime_web_app_url(url: str | None) -> None:
    global _RUNTIME_WEB_APP_URL
    if url:
        _RUNTIME_WEB_APP_URL = str(url).strip().rstrip("/") or None
    else:
        _RUNTIME_WEB_APP_URL = None


def _mini_app_https_ok(url: str) -> bool:
    """Telegram Mini App: только https, без заглушек и localhost."""
    u = (url or "").strip().lower()
    if len(u) < 12 or not u.startswith("https://"):
        return False
    blocked = (
        "example.com",
        "example.org",
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
    )
    return not any(b in u for b in blocked)


def effective_web_app_url() -> str:
    """Приоритет: WEB_APP_URL → размещённый HOSTED → временный туннель с ПК."""
    for c in (WEB_APP_URL, HOSTED_MINI_APP_URL, _RUNTIME_WEB_APP_URL):
        if c and _mini_app_https_ok(c):
            return c.strip().rstrip("/")
    return ""


def mini_app_url_valid() -> bool:
    return bool(effective_web_app_url())
