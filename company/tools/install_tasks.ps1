# install_tasks.ps1 - registers The Coach's reminders in Windows Task Scheduler (this PC, your user, no admin needed).
#   Morning tasks     every day 07:00   (before your 08:00 start)
#   Evening check-in  every day 21:45   (end of the evening routine)
#   Sunday review     Sunday   18:00
# If the PC is off or asleep at that time, the reminder is sent as soon as it's back on.
# Run again any time - it replaces the old tasks. Switch them all off: company\tools\remove_tasks.ps1
# Pause / resume without deleting: see company\HOW_IT_WORKS.md

$ErrorActionPreference = "Stop"
$repo   = (Resolve-Path "$PSScriptRoot\..\..").Path
$coach  = Join-Path $PSScriptRoot "coach.py"
$python = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source      # pythonw = no black window popping up
if (-not $python) { $python = (Get-Command python.exe).Source }
$folder = "\LearningCompany\"

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

$jobs = @(
    @{ Name = "Coach - morning tasks";    Arg = "morning"; Trigger = (New-ScheduledTaskTrigger -Daily -At "07:00") },
    @{ Name = "Coach - evening check-in"; Arg = "evening"; Trigger = (New-ScheduledTaskTrigger -Daily -At "21:45") },
    @{ Name = "Coach - Sunday review";    Arg = "sunday";  Trigger = (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "18:00") }
)

foreach ($j in $jobs) {
    $action = New-ScheduledTaskAction -Execute $python -Argument "`"$coach`" $($j.Arg)" -WorkingDirectory $repo
    Register-ScheduledTask -TaskName $j.Name -TaskPath $folder -Action $action -Trigger $j.Trigger -Settings $settings `
        -Description "Learning company - The Coach ($($j.Arg)). Repo: $repo" -Force | Out-Null
    Write-Host "  Registered: $($j.Name)"
}
Write-Host "`n  Done. Check them: Get-ScheduledTask -TaskPath '$folder'"
