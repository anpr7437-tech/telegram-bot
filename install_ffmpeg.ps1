# Скачивание FFmpeg в папку проекта (не требует прав и PATH)
$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
$FfmpegDir = Join-Path $ProjectDir "ffmpeg"
$ZipUrl = "https://github.com/GyanD/codexffmpeg/releases/download/8.0.1/ffmpeg-8.0.1-essentials_build.zip"
$ZipPath = Join-Path $ProjectDir "ffmpeg_temp.zip"

try {
    if (Test-Path (Join-Path $FfmpegDir "bin\ffmpeg.exe")) {
        Write-Host "FFmpeg уже есть в папке ffmpeg\. Пропуск."
        exit 0
    }

    Write-Host "Скачиваю архив..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $ZipUrl -OutFile $ZipPath -UseBasicParsing

    Write-Host "Распаковываю..."
    $ExtractDir = Join-Path $ProjectDir "ffmpeg_extract"
    if (Test-Path $ExtractDir) { Remove-Item $ExtractDir -Recurse -Force }
    Expand-Archive -Path $ZipPath -DestinationPath $ExtractDir -Force

    $InnerDir = Get-ChildItem $ExtractDir -Directory | Select-Object -First 1
    if (-not $InnerDir) { throw "Не найден каталог в архиве" }

    if (Test-Path $FfmpegDir) { Remove-Item $FfmpegDir -Recurse -Force }
    Rename-Item $InnerDir.FullName $FfmpegDir

    Remove-Item $ExtractDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue

    $FfmpegExe = Join-Path $FfmpegDir "bin\ffmpeg.exe"
    if (Test-Path $FfmpegExe) {
        Write-Host "Готово. FFmpeg установлен в папку: $FfmpegDir"
        exit 0
    }
    throw "ffmpeg.exe не найден после распаковки"
}
catch {
    Write-Host "Ошибка: $_"
    exit 1
}
