# remove_tasks.ps1 - switches The Coach OFF: deletes all its scheduled tasks. Nothing else is touched.
# Turn it back on any time with company\tools\install_tasks.ps1

$folder = "\LearningCompany\"
$tasks = Get-ScheduledTask -TaskPath $folder -ErrorAction SilentlyContinue
if (-not $tasks) { Write-Host "  No Coach tasks found - already off."; return }
foreach ($t in $tasks) {
    Unregister-ScheduledTask -TaskName $t.TaskName -TaskPath $folder -Confirm:$false
    Write-Host "  Removed: $($t.TaskName)"
}
Write-Host "  The Coach is off."
