# Тюнер на всех устройствах (без туннеля с вашего ПК)

Mini App — папка `web/static/`: `index.html`, `style.css`, `app.js`, `library.js` и после сборки `data/songs.json`, `data/chords.json`. При деплое через GitHub Actions JSON создаётся автоматически. Разместите на **бесплатном HTTPS**, чтобы приложение открывалось **с любого устройства**.

## Вариант A — GitHub Pages (рекомендуется)

1. Залейте эту папку проекта в **новый репозиторий** на GitHub (кнопка New repository → загрузите файлы или через GitHub Desktop).
2. В репозитории: **Settings → Pages → Build and deployment → Source** выберите **GitHub Actions**.
3. Чуть измените любой файл в `web/static/` (например пробел в `index.html`) и сделайте **Commit** — запустится workflow **Deploy Mini App to Pages**.
4. Через 1–2 минуты сайт будет по адресу:
   - обычный репозиторий: `https://ВАШ_НИК.github.io/ИМЯ_РЕПО/`
5. Откройте файл **`.env`** на компьютере, где крутится бот, и добавьте **одну строку** (подставьте свой URL **без** слэша в конце):

```env
HOSTED_MINI_APP_URL=https://ВАШ_НИК.github.io/ИМЯ_РЕПО
```

6. Перезапустите `start_bot.bat`. В Telegram нажмите `/start` — кнопка **«Настройка гитары»** откроет тюнер с сервера GitHub.

При такой настройке **Cloudflare Tunnel при старте бота не нужен** (можно в `.env` поставить `AUTO_CLOUDFLARE_TUNNEL=0`).

## Вариант B — Netlify / Cloudflare Pages

Зайдите на [netlify.com](https://www.netlify.com/) или [pages.cloudflare.com](https://pages.cloudflare.com/), перетащите папку **`web/static`** в окно «Deploy». Скопируйте выданный `https://....` в `.env`:

```env
HOSTED_MINI_APP_URL=https://ваш-поддомен.netlify.app
```

## Важно

- В Telegram в настройках бота у [@BotFather](https://t.me/BotFather) иногда нужно указать домен меню (если Mini App не откроется): команда для Web App / домен сайта — укажите `github.io` или ваш хостинг.
- Репозиторий с Pages может быть **публичным** (бесплатный тариф так устроен).
