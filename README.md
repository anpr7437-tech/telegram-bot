# Гитарный бот для Telegram

Бот: поиск песен с аккордами, избранное, история, справочник аккордов с картинками.  
Mini App: тюнер по микрофону и метроном (стили GuitarTuna / тёмная тема из ТЗ).

## Что нужно

1. **Python 3.10+** — [python.org](https://www.python.org/downloads/)
2. Токен бота от [@BotFather](https://t.me/BotFather) в Telegram
3. Для тюнера в Telegram на **любом устройстве** — один раз разместите `web/static` на **GitHub Pages** (см. **[DEPLOY_MINI_APP.md](DEPLOY_MINI_APP.md)**) и пропишите `HOSTED_MINI_APP_URL` в `.env`. Иначе бот поднимет временный HTTPS с вашего ПК (Cloudflare Tunnel).

## Быстрый старт (Windows)

**Самый простой вариант:** откройте **`ЗАПУСК.txt`** и сделайте как там написано — или сразу дважды нажмите **`start_bot.bat`** (скрипт сам скачает библиотеки; при первом запуске без `.env` откроется блокнот для токена).

Или вручную в терминале:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Откройте файл `.env` в блокноте:

- Вставьте `BOT_TOKEN=...` от BotFather.
- Опционально: `HOSTED_MINI_APP_URL=https://ваш_ник.github.io/репо` — тюнер с телефона без туннеля (см. [DEPLOY_MINI_APP.md](DEPLOY_MINI_APP.md)).

Запуск:

```powershell
python run.py
```

Должны появиться строки про `Mini App: http://...` и `Бот запущен`. В Telegram напишите боту `/start`.

## HTTPS для Mini App (тюнер / метроном)

### Стабильно на всех устройствах (рекомендуется)

Файлы тюнера лежат в `web/static/` — их можно выложить на **GitHub Pages** бесплатно.
В репозитории включите Pages (источник: **GitHub Actions**), после деплоя в `.env`:

`HOSTED_MINI_APP_URL=https://ваш_ник.github.io/имя_репозитория`

Подробно: **[DEPLOY_MINI_APP.md](DEPLOY_MINI_APP.md)**. Тогда **не нужен** ни ngrok, ни облачный туннель с вашего ПК (`AUTO_CLOUDFLARE_TUNNEL=0`).

### Временный HTTPS с вашего компьютера

По умолчанию бот поднимает **Cloudflare Quick Tunnel** (`tools/cloudflared`). Подождите до минуты,
разрешите доступ в фаерволе, затем **`/start`** в Telegram.

В `.env`: `AUTO_CLOUDFLARE_TUNNEL=0` — отключить туннель.

### Ручной ngrok

Telegram открывает Mini App только по **https://**. Ручной вариант:

1. Установите [ngrok](https://ngrok.com/download), зарегистрируйтесь и добавьте токен (`ngrok config add-authtoken ...`).
2. Запустите бота (`python run.py`), затем в **втором** окне терминала:

   ```powershell
   ngrok http 8080
   ```

3. Скопируйте выданный URL вида `https://xxxx.ngrok-free.app` в `.env`:

   ```env
   WEB_APP_URL=https://xxxx.ngrok-free.app
   ```

4. Перезапустите `python run.py`. В [@BotFather](https://t.me/BotFather) можно при желании указать домен меню бота (Domain), совпадающий с ngrok.

Без ngrok остаются все функции бота **кроме** открытия веб-приложения внутри Telegram; страницу тюнера всё равно можно открыть в браузере по `http://localhost:8080/` (микрофон браузер обычно даст).

## Команды бота

| Команда       | Действие              |
|---------------|------------------------|
| `/start`      | Меню                   |
| `/search`     | Поиск песни            |
| `/chords`     | Справочник аккордов    |
| `/top`        | Популярное             |
| `/favorites`  | Избранное              |
| `/history`    | История просмотров     |

Данные хранятся в `data/bot.db`. Картинки аккордов — в `data/chord_images/`.

## Юридическое

Тексты песен в базе — только иллюстративные отрывки для демо. Для продакшена используйте лицензионные источники или собственный контент.
