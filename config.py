"""Конфигурация бота из переменных окружения."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Telegram (на серверах часто используют TELEGRAM_BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "")

# Админы (Telegram ID через запятую)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in ADMIN_IDS_STR.split(",") if x.strip()]

# Лимиты
DAILY_DOWNLOAD_LIMIT = int(os.getenv("DAILY_DOWNLOAD_LIMIT", "3"))
FLOOD_DELAY_SECONDS = float(os.getenv("FLOOD_DELAY_SECONDS", "1.5"))

# Пути
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOWNLOADS_DIR = DATA_DIR / "downloads"
DB_PATH = DATA_DIR / "bot.db"

# Создаём директории
DATA_DIR.mkdir(exist_ok=True)
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Тексты (можно вынести в отдельный файл)
WELCOME_TEXT = (
    "👋 Привет! Я бот для скачивания видео и фото по ссылкам.\n\n"
    "📱 Поддерживаю: TikTok, YouTube (в т.ч. Shorts), Instagram (Reels, посты, Stories), Pinterest.\n\n"
    "⚠️ Для использования необходимо подписаться на наш канал.\n"
    "Нажмите кнопку ниже:"
)
SUBSCRIPTION_CHECKED_TEXT = (
    "✅ Спасибо! Теперь вы можете отправлять ссылки — я скачаю контент и пришлю файл.\n\n"
    "📌 Лимит: {limit} загрузок в сутки."
)
LIMIT_EXCEEDED_TEXT = (
    "⏳ Вы исчерпали дневной лимит ({limit} загрузок).\n"
    "Лимит обновится завтра."
)
INVALID_LINK_TEXT = "❌ Не удалось определить платформу по ссылке. Поддерживаются: TikTok, YouTube, Instagram, Pinterest."
DOWNLOAD_ERROR_TEXT = "❌ Не удалось скачать контент. Проверьте ссылку и доступность."
SEND_LINK_TEXT = "📎 Отправьте ссылку на видео или фото:"
