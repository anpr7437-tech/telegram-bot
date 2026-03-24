@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Гитарный бот Telegram

echo.
echo  ========================================
echo    Гитарный бот — скачивание и запуск
echo  ========================================
echo.

REM --- Какой Python есть в системе? ---
set "PY_CMD="
python --version >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD py -3 --version >nul 2>&1 && set "PY_CMD=py -3"

if not defined PY_CMD (
  echo  [X] Python не найден. Без него бот не запустится.
  echo.
  echo  Что сделать:
  echo  1. Откройте в браузере: https://www.python.org/downloads/
  echo  2. Скачайте Python 3.10 или новее и установите.
  echo  3. В установщике ОБЯЗАТЕЛЬНО включите галочку:
  echo     "Add python.exe to PATH" ^(добавить в PATH^)
  echo  4. Закройте это окно и снова дважды нажмите start_bot.bat
  echo.
  pause
  exit /b 1
)

echo  [ok] Найден: %PY_CMD%
echo.

REM --- Виртуальное окружение (папка .venv) ---
if not exist ".venv\Scripts\python.exe" (
  echo  [*] Первый раз: создаю папку .venv ^(это нормально^)...
  %PY_CMD% -m venv .venv
  if errorlevel 1 (
    echo  [X] Не удалось создать .venv. Запустите от имени обычного пользователя или проверьте антивирус.
    pause
    exit /b 1
  )
  echo  [ok] Готово.
) else (
  echo  [ok] Папка .venv уже есть — пропускаю создание.
)
echo.

REM --- Если в .venv нет pip (бывает на части установок Python) ---
".venv\Scripts\python.exe" -m pip --version >nul 2>&1
if errorlevel 1 (
  echo  [!] В виртуальном окружении нет pip — пробую восстановить ^(ensurepip^)...
  ".venv\Scripts\python.exe" -m ensurepip --upgrade --default-pip
  ".venv\Scripts\python.exe" -m pip --version >nul 2>&1
  if errorlevel 1 (
    echo  [!] ensurepip не сработал — удаляю старую папку .venv и создаю заново...
    rmdir /s /q ".venv" 2>nul
    %PY_CMD% -m venv .venv
    if errorlevel 1 (
      echo  [X] Не удалось создать .venv заново.
      pause
      exit /b 1
    )
    ".venv\Scripts\python.exe" -m ensurepip --upgrade --default-pip
  )
)
".venv\Scripts\python.exe" -m pip --version >nul 2>&1
if errorlevel 1 (
  echo  [X] pip так и не появился. Переустановите Python с сайта python.org
  echo      и при установке включите «pip» и «Add to PATH».
  pause
  exit /b 1
)
echo  [ok] pip на месте.
echo.

REM --- Скачивание библиотек из интернета ---
echo  [*] Скачиваю библиотеки ^(aiogram, aiohttp и др.^) — нужен интернет...
echo      Подождите 1--3 минуты при первом запуске.
echo.
".venv\Scripts\python.exe" -m pip install --upgrade pip -q
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo  [X] Не удалось установить пакеты. Проверьте интернет и VPN.
  pause
  exit /b 1
)
echo.
echo  [ok] Все библиотеки установлены.
echo.

REM --- Файл с токеном бота ---
if not exist ".env" (
  echo  [*] Файла .env нет — копирую из .env.example
  if exist ".env.example" (
    copy /Y ".env.example" ".env" >nul
  )
  echo  Откроется блокнот: вставьте токен от BotFather в строку BOT_TOKEN=...
  echo  Сохраните файл ^(Ctrl+S^) и закройте блокнот.
  timeout /t 3 >nul
  start "" notepad ".env"
  echo.
  echo  Когда сохраните .env, нажмите любую клавишу здесь...
  pause >nul
)

echo  ========================================
echo    Бот работает! Это окно не закрывайте.
echo    Первый раз подождите до 1 мин — может скачаться cloudflared
echo    и появится HTTPS для тюнера. Потом в Telegram: /start
echo    Остановка: Ctrl+C
echo  ========================================
echo.

".venv\Scripts\python.exe" run.py
echo.
if errorlevel 1 (
  echo  [X] Бот остановился с ошибкой. Чаще всего: неверный BOT_TOKEN в файле .env
  echo      или нет интернета. Откройте .env в блокноте и проверьте токен.
)
pause
