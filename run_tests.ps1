param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("smoke","smoke_10","baseline_25","baseline_50","baseline_100","standard","peak","stress400","stress500","spike")]
    [string]$scenario,

    [Parameter(Mandatory=$false)]
    [ValidateSet("TEST","PRE-PROD")]
    [string]$env="TEST",

    [Parameter(Mandatory=$false)]
    [ValidateSet("normal","step")]
    [string]$executionMode="normal",

    [Parameter(Mandatory=$false)]
    [ValidateSet("DEBUG","INFO","WARNING","ERROR","CRITICAL")]
    [string]$logLevel="WARNING"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$resultsFolder = "results\$scenario`_$timestamp"

Write-Host ""
Write-Host "-------------------------------------"
Write-Host "Running Locust Scenario: $scenario"
Write-Host "Environment: $env"
Write-Host "Execution Mode: $executionMode"
Write-Host "Log Level: $logLevel"
Write-Host "Results Folder: $resultsFolder"
Write-Host "-------------------------------------"
Write-Host ""

$env:APP_ENV = $env
$env:LOCUST_SCENARIO = $scenario
$env:LOCUST_EXECUTION_MODE = $executionMode

New-Item -ItemType Directory -Force -Path $resultsFolder | Out-Null

function Run-LocustScenario {
    param(
        [string]$users,
        [string]$spawnRate,
        [string]$duration,
        [string]$stopTimeout,
        [string]$csvPrefix
    )

    if ($executionMode -eq "step") {
        locust `
            -f locustfile.py,load_shapes/step_load_shape.py `
            --headless `
            --loglevel $logLevel `
            -t $duration `
            --stop-timeout $stopTimeout `
            --csv "$resultsFolder\$csvPrefix" `
            --csv-full-history
    }
    else {
        locust `
            -f locustfile.py `
            --headless `
            --loglevel $logLevel `
            -u $users `
            -r $spawnRate `
            -t $duration `
            --stop-timeout $stopTimeout `
            --csv "$resultsFolder\$csvPrefix" `
            --csv-full-history
    }
}

switch ($scenario) {

    "smoke" {
        Run-LocustScenario -users 5 -spawnRate 5 -duration "2m" -stopTimeout "15s" -csvPrefix "smoke"
    }

    "smoke_10" {
        Run-LocustScenario -users 10 -spawnRate 5 -duration "2m" -stopTimeout "15s" -csvPrefix "smoke_10"
    }

    "baseline_25" {
        Run-LocustScenario -users 25 -spawnRate 10 -duration "20m" -stopTimeout "15s" -csvPrefix "baseline_25"
    }

    "baseline_50" {
        Run-LocustScenario -users 50 -spawnRate 10 -duration "20m" -stopTimeout "15s" -csvPrefix "baseline_50"
    }

    "baseline_100" {
        Run-LocustScenario -users 100 -spawnRate 10 -duration "2m" -stopTimeout "15s" -csvPrefix "baseline_100"
    }

    "standard" {
        Run-LocustScenario -users 200 -spawnRate 10 -duration "2m" -stopTimeout "30s" -csvPrefix "standard_200"
    }

    "peak" {
        Run-LocustScenario -users 300 -spawnRate 10 -duration "6m" -stopTimeout "30s" -csvPrefix "peak_300"
    }

    "stress400" {
        Run-LocustScenario -users 400 -spawnRate 5 -duration "5m" -stopTimeout "30s" -csvPrefix "stress_400"
    }

    "stress500" {
        Run-LocustScenario -users 500 -spawnRate 5 -duration "6m" -stopTimeout "30s" -csvPrefix "stress_500"
    }

    "spike" {
        Run-LocustScenario -users 300 -spawnRate 50 -duration "2m" -stopTimeout "20s" -csvPrefix "spike_300"
    }
}

Write-Host ""
Write-Host "Generating HTML and PDF reports..."

python -c "from utils.report_generator import generate_html_report; generate_html_report(r'$resultsFolder', '$scenario', '$env', auto_open=True)"
python -c "from utils.pdf_report_generator import generate_pdf_summary; generate_pdf_summary(r'$resultsFolder', '$scenario', '$env')"

Write-Host ""
Write-Host "Test Completed."
Write-Host "Results saved in: $resultsFolder"
Write-Host ""