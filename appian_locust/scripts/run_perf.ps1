param(
    [string] $Host = $(Read-Host "PERF_HOST (e.g. https://preprod.example.com)"),
    [string] $User = $(Read-Host "PERF_USER"),
    [string] $Pass = $(Read-Host "PERF_PASS"),
    [int] $Users = 200,
    [int] $HatchRate = 10,
    [string] $Duration = "60m",
    [string] $CsvPrefix = "perf_run"
)

# try to activate venv if present (repo root .venv)
$venvActivate = Join-Path $PSScriptRoot "..\.venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating venv: $venvActivate"
    . $venvActivate
} else {
    Write-Host "No .venv found at repo root; ensure Locust is installed and on PATH or use python -m locust"
}

# set env vars for Appian locustfile
$env:PERF_HOST = $Host
$env:PERF_USER = $User
$env:PERF_PASS = $Pass

Write-Host "Starting Locust headless: users=$Users rate=$HatchRate duration=$Duration host=$Host"

$locustFile = Join-Path $PSScriptRoot "..\examples\perf_locustfile.py"

# prefer locust cli if available, otherwise fallback to python -m locust
if (Get-Command locust -ErrorAction SilentlyContinue) {
    & locust -f $locustFile --headless -u $Users -r $HatchRate -t $Duration --host $Host --csv $CsvPrefix
} else {
    & python -m locust -f $locustFile --headless -u $Users -r $HatchRate -t $Duration --host $Host --csv $CsvPrefix
}