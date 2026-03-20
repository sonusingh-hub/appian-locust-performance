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
    [string]$logLevel="WARNING",

    [Parameter(Mandatory=$false)]
    [ValidateSet("realistic","balanced","stress")]
    [string]$runMode="realistic",

    [Parameter(Mandatory=$false)]
    [ValidateSet("benchmark","realistic")]
    [string]$userBehaviorProfile="realistic",

    [Parameter(Mandatory=$false)]
    [ValidateSet("auto","reserved","reserve","reuse")]
    [string]$credentialMode="auto",

    [Parameter(Mandatory=$false)]
    [double]$outlierThresholdMs=120000,

    [Parameter(Mandatory=$false)]
    [ValidateSet("off","minimal","full")]
    [string]$reportMode="minimal",

    [Parameter(Mandatory=$false)]
    [switch]$generateClientReport,

    [Parameter(Mandatory=$false)]
    [switch]$collectFullHistory
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$resultsFolder = "results\$scenario`_$timestamp"

Write-Host ""
Write-Host "-------------------------------------"
Write-Host "Running Locust Scenario: $scenario"
Write-Host "Environment: $env"
Write-Host "Execution Mode: $executionMode"
Write-Host "Log Level: $logLevel"
Write-Host "Run Mode: $runMode"
Write-Host "User Behavior Profile: $userBehaviorProfile"
Write-Host "Credential Mode: $credentialMode"
Write-Host "Outlier Threshold (ms): $outlierThresholdMs"
Write-Host "Report Mode: $reportMode"
Write-Host "Generate Client Report: $generateClientReport"
Write-Host "CSV Full History: $collectFullHistory"
Write-Host "Results Folder: $resultsFolder"
Write-Host "-------------------------------------"
Write-Host ""

$env:APP_ENV = $env
$env:LOCUST_SCENARIO = $scenario
$env:LOCUST_EXECUTION_MODE = $executionMode
$env:LOCUST_RUN_MODE = $runMode
$env:LOCUST_USER_BEHAVIOR_PROFILE = $userBehaviorProfile
$env:LOCUST_OUTLIER_THRESHOLD_MS = "$outlierThresholdMs"
$reportPython = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }

function Get-RecommendedCredentialMode {
    param(
        [int]$users,
        [int]$availableUsers
    )

    if ($availableUsers -le 0) {
        return "reuse"
    }

    # Keep headroom for session churn/refresh and avoid reservation contention.
    $reservedCapacity = [int][math]::Floor($availableUsers * 0.70)
    if ($users -le [math]::Max($reservedCapacity, 1)) {
        return "reserved"
    }

    return "reuse"
}

New-Item -ItemType Directory -Force -Path $resultsFolder | Out-Null

function Get-AvailableCredentialCount {
    param(
        [string]$csvPath,
        [string]$selectedEnv
    )

    if (-not (Test-Path $csvPath)) {
        return 0
    }

    $rows = Import-Csv -Path $csvPath
    if (-not $rows) {
        return 0
    }

    return @(
        $rows | Where-Object {
            $_.environment -and $_.environment.Trim().ToUpper() -eq $selectedEnv.Trim().ToUpper()
        }
    ).Count
}

function Run-LocustScenario {
    param(
        [string]$users,
        [string]$spawnRate,
        [string]$duration,
        [string]$stopTimeout,
        [string]$csvPrefix
    )

    $availableUsers = Get-AvailableCredentialCount -csvPath "data/users.csv" -selectedEnv $env
    $normalizedCredentialMode = if ($credentialMode -eq "reserve") { "reserved" } else { $credentialMode }
    $effectiveCredentialMode = $normalizedCredentialMode

    if ($normalizedCredentialMode -eq "auto") {
        $effectiveCredentialMode = Get-RecommendedCredentialMode -users $users -availableUsers $availableUsers
    }

    $env:LOCUST_CREDENTIAL_MODE = $effectiveCredentialMode

    Write-Host "Scenario users: $users | Available creds: $availableUsers | Effective credential mode: $effectiveCredentialMode"

    $commonArgs = @(
        "--headless",
        "--loglevel", $logLevel,
        "-t", $duration,
        "--stop-timeout", $stopTimeout,
        "--csv", "$resultsFolder\$csvPrefix"
    )
    if ($collectFullHistory) {
        $commonArgs += "--csv-full-history"
    }

    if ($executionMode -eq "step") {
        locust -f locustfile.py,load_shapes/step_load_shape.py @commonArgs
    }
    else {
        locust -f locustfile.py -u $users -r $spawnRate @commonArgs
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Locust execution failed with exit code $LASTEXITCODE"
    }
}

switch ($scenario) {

    "smoke" {
        Run-LocustScenario -users 5 -spawnRate 10 -duration "5m" -stopTimeout "15s" -csvPrefix "smoke"
    }

    "smoke_10" {
        Run-LocustScenario -users 10 -spawnRate 60 -duration "10m" -stopTimeout "15s" -csvPrefix "smoke_10"
    }

    "baseline_25" {
        Run-LocustScenario -users 25 -spawnRate 300 -duration "20m" -stopTimeout "15s" -csvPrefix "baseline_25"
    }

    "baseline_50" {
        Run-LocustScenario -users 50 -spawnRate 600 -duration "20m" -stopTimeout "15s" -csvPrefix "baseline_50"
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
if ($reportMode -eq "off") {
    Write-Host "Skipping report generation (reportMode=off)."
}
elseif ($reportMode -eq "minimal") {
    Write-Host "Generating minimal report (PDF only)..."
    & $reportPython -c "from utils.pdf_report_generator import generate_pdf_summary; generate_pdf_summary(r'$resultsFolder', '$scenario', '$env', credential_mode='$env:LOCUST_CREDENTIAL_MODE', behavior_profile='$env:LOCUST_USER_BEHAVIOR_PROFILE')"
    if ($LASTEXITCODE -ne 0) {
        throw "PDF report generation failed with exit code $LASTEXITCODE"
    }
}
else {
    Write-Host "Generating full reports (HTML + PDF)..."
    & $reportPython -c "from utils.report_generator import generate_html_report; generate_html_report(r'$resultsFolder', '$scenario', '$env', auto_open=False, credential_mode='$env:LOCUST_CREDENTIAL_MODE', behavior_profile='$env:LOCUST_USER_BEHAVIOR_PROFILE')"
    if ($LASTEXITCODE -ne 0) {
        throw "HTML report generation failed with exit code $LASTEXITCODE"
    }
    & $reportPython -c "from utils.pdf_report_generator import generate_pdf_summary; generate_pdf_summary(r'$resultsFolder', '$scenario', '$env', credential_mode='$env:LOCUST_CREDENTIAL_MODE', behavior_profile='$env:LOCUST_USER_BEHAVIOR_PROFILE')"
    if ($LASTEXITCODE -ne 0) {
        throw "PDF report generation failed with exit code $LASTEXITCODE"
    }
}

if ($generateClientReport) {
    Write-Host "Generating consolidated client report from discovered baseline runs..."
    & $reportPython scripts\generate_client_report.py --results-root results --output results\apac_performance_report.pdf --max-runs 5
    if ($LASTEXITCODE -ne 0) {
        throw "Client report generation failed with exit code $LASTEXITCODE"
    }
    Write-Host "Client report saved to: results\apac_performance_report.pdf"
}

Write-Host ""
Write-Host "Test Completed."
Write-Host "Results saved in: $resultsFolder"
Write-Host ""