# Inicia el servidor de desarrollo CPEH en http://127.0.0.1:8000
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Creando entorno virtual..."
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
}

$env:DJANGO_SETTINGS_MODULE = "config.settings.local"

if (-not (Test-Path ".\.env")) {
    Copy-Item .env.example .env
    Write-Host "Creado .env desde .env.example"
}

Write-Host ""
Write-Host "CPEH — servidor en http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Inscripcion: http://127.0.0.1:8000/inscripcion/" -ForegroundColor Cyan
Write-Host "Panel:       http://127.0.0.1:8000/panel/ (usuario admin)" -ForegroundColor Cyan
Write-Host "Deje esta ventana ABIERTA. Ctrl+C para detener." -ForegroundColor Yellow
Write-Host ""

.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000
