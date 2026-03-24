"""
Точка входа: опрос Telegram + раздача Mini App по HTTP.
"""
from __future__ import annotations

import asyncio
import errno
import logging
import sys
from pathlib import Path

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.db import init_db
from bot.handlers import router
from bot.miniapp_export import export_miniapp_static_json
from bot.seed import run_seed
from config import (
    AUTO_CLOUDFLARE_TUNNEL,
    BASE_DIR,
    BOT_TOKEN,
    HTTP_HOST,
    HTTP_PORT,
    effective_http_port,
    effective_web_app_url,
    mini_app_url_valid,
    set_bind_http_port,
    set_runtime_web_app_url,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("guitar-bot")

STATIC_DIR = BASE_DIR / "web" / "static"


async def _serve_index(_request: web.Request) -> web.FileResponse:
    return web.FileResponse(STATIC_DIR / "index.html")


async def _serve_style(_request: web.Request) -> web.FileResponse:
    return web.FileResponse(STATIC_DIR / "style.css")


async def _serve_app_js(_request: web.Request) -> web.FileResponse:
    return web.FileResponse(STATIC_DIR / "app.js")


def build_http_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", _serve_index)
    app.router.add_get("/style.css", _serve_style)
    app.router.add_get("/app.js", _serve_app_js)
    app.router.add_static("/static/", path=str(STATIC_DIR), name="static")
    data_dir = STATIC_DIR / "data"
    if data_dir.is_dir():
        app.router.add_static("/data/", path=str(data_dir), name="data")
    return app


async def run_http_server() -> web.AppRunner:
    app = build_http_app()
    runner = web.AppRunner(app)
    await runner.setup()
    set_bind_http_port(None)
    last_err: OSError | None = None
    bound: int | None = None
    for offset in range(32):
        port = HTTP_PORT + offset
        site = web.TCPSite(runner, host=HTTP_HOST, port=port)
        try:
            await site.start()
            bound = port
            break
        except OSError as e:
            last_err = e
            port_busy = getattr(e, "winerror", None) == 10048 or e.errno == errno.EADDRINUSE
            if not port_busy:
                await runner.cleanup()
                raise
    if bound is None:
        await runner.cleanup()
        log.error(
            "Порты %s–%s заняты (часто — уже открыто второе окно с ботом). "
            "Закройте лишнее окно или в .env укажите другой HTTP_PORT=8090",
            HTTP_PORT,
            HTTP_PORT + 31,
        )
        raise last_err or OSError("Не удалось занять порт для Mini App")
    set_bind_http_port(bound)
    if bound != HTTP_PORT:
        log.warning(
            "Порт %s занят — Mini App слушает %s (тюнер: http://127.0.0.1:%s/)",
            HTTP_PORT,
            bound,
            bound,
        )
    log.info(
        "Mini App: http://%s:%s/",
        HTTP_HOST,
        bound,
    )
    if mini_app_url_valid():
        log.info(
            "Mini App для Telegram (любое устройство): %s/",
            effective_web_app_url(),
        )
    else:
        log.info(
            "HTTPS для Mini App — HOSTED_MINI_APP_URL, авто-туннель Cloudflare или WEB_APP_URL. "
            "Локально: http://%s:%s/",
            HTTP_HOST if HTTP_HOST != "0.0.0.0" else "127.0.0.1",
            bound,
        )
    return runner


async def main() -> None:
    if not BOT_TOKEN:
        log.error("Создайте файл .env и укажите BOT_TOKEN=... (см. .env.example)")
        sys.exit(1)

    await init_db()
    await run_seed()
    try:
        export_miniapp_static_json()
    except OSError as e:
        log.warning("Не удалось обновить web/static/data: %s", e)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    runner = await run_http_server()
    tunnel = None
    try:
        if not mini_app_url_valid() and AUTO_CLOUDFLARE_TUNNEL:
            from bot.cloudflare_tunnel import CloudflareQuickTunnel, ensure_cloudflared

            exe = ensure_cloudflared(BASE_DIR)
            if exe:
                log.info(
                    "Поднимаю бесплатный HTTPS-туннель (Cloudflare). "
                    "Первый раз может скачаться cloudflared — подождите до ~1 мин."
                )
                await asyncio.sleep(0.8)
                tunnel = CloudflareQuickTunnel()
                url = await asyncio.to_thread(
                    tunnel.start, effective_http_port(), exe, 55.0
                )
                if url:
                    set_runtime_web_app_url(url)
                    log.info("Mini App для Telegram: %s/  (нажмите /start чтобы обновить кнопки)", url)
                else:
                    log.warning(
                        "Авто-туннель не поднялся (фаервол/антивирус?). "
                        "Тюнер: http://127.0.0.1:%s/ или ngrok в README.",
                        effective_http_port(),
                    )
                    tunnel.stop()
                    tunnel = None
            else:
                log.warning(
                    "cloudflared недоступен. Поставьте вручную или укажите WEB_APP_URL в .env"
                )

        log.info("Бот запущен (long polling). /start в Telegram.")
        await dp.start_polling(bot)
    finally:
        if tunnel:
            tunnel.stop()
            set_runtime_web_app_url(None)
        await bot.session.close()
        await runner.cleanup()


if __name__ == "__main__":
    # На Python 3.14+ политика SelectorLoop помечена устаревшей; Proactor по умолчанию ок.
    if sys.platform == "win32" and sys.version_info < (3, 14):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
