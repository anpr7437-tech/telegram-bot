@echo off
chcp 65001 >nul
title Сборка архива для сервера
cd /d "%~dp0"

set ZIPNAME=бот_для_сервера.zip
if exist "%ZIPNAME%" del "%ZIPNAME%"

echo Собираю архив для загрузки на JustRunMy.App...
echo (в архив не входят: data, .env, __pycache__, .bat-файлы)
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"Add-Type -AssemblyName System.IO.Compression.FileSystem; ^
$root = (Get-Location).Path; ^
$zipPath = Join-Path $root 'бот_для_сервера.zip'; ^
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, 'Create'); ^
Get-ChildItem -Path . -Recurse -File | Where-Object { ^
  $_.FullName -notmatch '\\data\\' -and ^
  $_.FullName -notmatch '\\__pycache__\\' -and ^
  $_.FullName -notmatch '\\.git\\' -and ^
  $_.Name -ne '.env' -and ^
  $_.Extension -ne '.bat' -and ^
  $_.Name -ne 'install_ffmpeg.ps1' ^
} | ForEach-Object { ^
  $rel = $_.FullName.Substring($root.Length).TrimStart('\'); ^
  [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $rel.Replace('\','/')) | Out-Null ^
}; ^
$zip.Dispose(); ^
Write-Host 'Архив создан: бот_для_сервера.zip'"

if exist "%ZIPNAME%" (
    echo.
    echo Готово. Загрузите файл на https://justrunmy.app
    echo В настройках укажите: BOT_TOKEN и ADMIN_IDS
    echo.
    start "" "%ZIPNAME%"
) else (
    echo Ошибка создания архива.
)

pause
