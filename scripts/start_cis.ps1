
<#
.SYNOPSIS
    Curriculum Intelligence System (CIS) - Windows Service Launcher.
.DESCRIPTION
    Launches:
    1. FastAPI Backend       - Port 8000
    2. Official MCP Server   - Port 8001
    3. OpenClaw Gateway      - Port 18789
    4. React Vite Frontend   - Port 5173
#>

param (
    [switch]$BackendOnly,
    [switch]$FrontendOnly,
    [switch]$McpOnly,
    [switch]$OpenClawOnly,
    [switch]$Seed
)

$ErrorActionPreference = "Stop"

# Resolve project root
$Root = Split-Path -Parent $PSScriptRoot

# Set window title safely
try {
    $Host.UI.RawUI.WindowTitle = "CIS Service Launcher"
} catch {}

# Display banner
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       CURRICULUM INTELLIGENCE SYSTEM - LAUNCHER" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan

# Environment setup
$env:PYTHONPATH = "$Root\backend;$Root"

# Database seeding
if ($Seed) {
    Write-Host "[*] Seeding CIS database..." -ForegroundColor Yellow

    Set-Location $Root
    python scripts/seed_db.py

    if ($LASTEXITCODE -ne 0) {
        throw "Database seeding failed."
    }

    Write-Host "[+] Database seeded successfully!" -ForegroundColor Green
    exit 0
}

# Individual service launch options
if ($BackendOnly) {
    Write-Host "[*] Starting FastAPI Backend..." -ForegroundColor Green
    Set-Location "$Root\backend"
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    exit $LASTEXITCODE
}

if ($McpOnly) {
    Write-Host "[*] Starting MCP Server..." -ForegroundColor Green
    Set-Location $Root
    python mcp_server/server.py
    exit $LASTEXITCODE
}

if ($OpenClawOnly) {
    Write-Host "[*] Starting OpenClaw Gateway..." -ForegroundColor Green
    Set-Location $Root
    python openclaw/gateway_service.py
    exit $LASTEXITCODE
}

if ($FrontendOnly) {
    Write-Host "[*] Starting React Frontend..." -ForegroundColor Green
    Set-Location "$Root\frontend"
    npm run dev
    exit $LASTEXITCODE
}

# Launch all services in separate PowerShell windows
Write-Host "[1/4] Launching OpenClaw Gateway..." -ForegroundColor Yellow

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$Root'; `$env:PYTHONPATH='$Root\backend;$Root'; python openclaw/gateway_service.py"
)

Write-Host "[2/4] Launching MCP Server..." -ForegroundColor Yellow

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$Root'; `$env:PYTHONPATH='$Root\backend;$Root'; python mcp_server/server.py"
)

Write-Host "[3/4] Launching FastAPI Backend..." -ForegroundColor Yellow

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$Root\backend'; `$env:PYTHONPATH='$Root\backend;$Root'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
)

Write-Host "[4/4] Launching React Frontend..." -ForegroundColor Yellow

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$Root\frontend'; npm run dev"
)

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "CIS SERVICES LAUNCHED" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:       http://localhost:5173" -ForegroundColor Green
Write-Host "Backend Docs:   http://localhost:8000/docs" -ForegroundColor Green
Write-Host "MCP Server:     http://localhost:8001/mcp/tools" -ForegroundColor Green
Write-Host "OpenClaw:       http://localhost:18789/health" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
