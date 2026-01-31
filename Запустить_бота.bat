@echo off
chcp 65001 >nul
title Telegram-бот
cd /d "%~dp0"

:: Если FFmpeg установлен в папку проекта — подставляем в PATH
if exist "%~dp0ffmpeg\bin\ffmpeg.exe" set "PATH=%PATH%;%~dp0ffmpeg\bin"

echo Запуск бота...
echo Чтобы остановить — закройте это окно или нажмите Ctrl+C
echo.

python main.py

pause
