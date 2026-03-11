param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("smoke","baseline","standard","peak","stress400","stress500","spike")]
    [string]$scenario,

    [Parameter(Mandatory=$false)]
    [ValidateSet("TEST","PRE-PROD")]
    [string]$env="TEST"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$resultsFolder = "results\$scenario`_$timestamp"

Write-Host ""
Write-Host "-------------------------------------"
Write-Host "Running Locust Scenario: $scenario"
Write-Host "Environment: $env"
Write-Host "Results Folder: $resultsFolder"
Write-Host "-------------------------------------"
Write-Host ""

$env:APP_ENV = $env
New-Item -ItemType Directory -Force -Path $resultsFolder | Out-Null

switch ($scenario) {

    "smoke" {
        locust -f locustfile.py --headless -u 1 -r 1 -t 1m --stop-timeout 15s --csv "$resultsFolder\smoke"
    }

    "baseline" {
        locust -f locustfile.py --headless -u 5 -r 1 -t 30m --stop-timeout 15s --csv "$resultsFolder\baseline"
    }

    "standard" {
        locust -f locustfile.py --headless -u 200 -r 10 -t 60m --stop-timeout 30s --csv "$resultsFolder\standard_200"
    }

    "peak" {
        locust -f locustfile.py --headless -u 300 -r 10 -t 60m --stop-timeout 30s --csv "$resultsFolder\peak_300"
    }

    "stress400" {
        locust -f locustfile.py --headless -u 400 -r 5 -t 45m --stop-timeout 30s --csv "$resultsFolder\stress_400"
    }

    "stress500" {
        locust -f locustfile.py --headless -u 500 -r 5 -t 45m --stop-timeout 30s --csv "$resultsFolder\stress_500"
    }

    "spike" {
        locust -f locustfile.py --headless -u 300 -r 50 -t 20m --stop-timeout 20s --csv "$resultsFolder\spike_300"
    }
}

Write-Host ""
Write-Host "Generating HTML and PDF reports..."
python -c "from utils.report_generator import generate_html_report; generate_html_report(r'$resultsFolder', '$scenario', '$env')"
python -c "from utils.pdf_report_generator import generate_pdf_summary; generate_pdf_summary(r'$resultsFolder', '$scenario', '$env')"

Write-Host ""
Write-Host "Test Completed."
Write-Host "Results saved in: $resultsFolder"
Write-Host ""