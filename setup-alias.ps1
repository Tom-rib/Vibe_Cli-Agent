# Setup PowerShell Alias for cliagent
# Run this script once to create a permanent alias

$profilePath = $PROFILE
if (!(Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force | Out-Null
    Write-Host "✅ Profil PowerShell créé: $profilePath" -ForegroundColor Green
}

# Déterminer le chemin du script cliagent.ps1
$script = Get-Location
$alias_content = @"
# Agent IA CLI - cliagent alias
function cliagent {
    & "$($script.Path)\cliagent.ps1" @args
}
"@

# Ajouter l'alias au profil
Add-Content $profilePath "`n$alias_content"

Write-Host ""
Write-Host "✅ Alias 'cliagent' créé avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Pour l'utiliser maintenant, exécutez:" -ForegroundColor Cyan
Write-Host ". `$PROFILE" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 Ensuite, vous pouvez taper:" -ForegroundColor Cyan
Write-Host "cliagent" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ou ouvrez un nouveau terminal PowerShell pour que l'alias soit chargé automatiquement" -ForegroundColor Gray
