@echo off
chcp 65001 >nul
title Установка FFmpeg
cd /d "%~dp0"

echo.
echo ═══ Установка FFmpeg для скачивания видео ═══
echo.

:: Способ 1: через winget (Windows 10/11)
where winget >nul 2>nul
if %errorlevel% equ 0 (
    echo Способ 1: устанавливаю через winget...
    winget install --id Gyan.FFmpeg.Essentials -e --accept-package-agreements --accept-source-agreements
    if %errorlevel% equ 0 (
        echo.
        echo FFmpeg установлен через winget.
        echo Если бот потом не найдёт ffmpeg — перезапустите компьютер или откройте новое окно терминала.
        goto :ok
    )
    echo winget не смог установить, пробую способ 2...
    echo.
)

:: Способ 2: скачать в папку проекта (бот подхватит при запуске)
echo Способ 2: скачиваю FFmpeg в папку проекта...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_ffmpeg.ps1"
if %errorlevel% equ 0 goto :ok

echo.
echo Не удалось установить автоматически.
echo Установите вручную: https://www.gyan.dev/ffmpeg/builds/
echo Скачайте ffmpeg-release-essentials, распакуйте и добавьте папку bin в PATH.
echo.
goto :finish

:ok
echo.
echo Готово. Можно запускать бота.
echo.

:finish
pause
