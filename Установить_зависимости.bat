@echo off
chcp 65001 >nul
title Установка зависимостей бота
cd /d "%~dp0"

echo.
echo Устанавливаю пакеты из requirements.txt...
echo.

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Пробую команду py...
    py -m pip install -r requirements.txt
)

echo.
echo Готово. Если ошибок нет — можно запускать бота двойным щелчком по "Запустить_бота.bat"
echo.
pause
