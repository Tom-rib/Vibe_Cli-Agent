# Script PowerShell pour lancer l'Agent IA CLI en mode interactif
# Usage: .\copilot.ps1 ou copilot (si dans le PATH)

param(
    [string[]]$Arguments
)

# Déterminer le répertoire du script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Vérifier venv
$venvPath = Join-Path $scriptDir "venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host ""
    Write-Host "❌ Erreur: virtualenv non trouvé" -ForegroundColor Red
    Write-Host "   Veuillez exécuter: python -m venv venv" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Vérifier .env
$envPath = Join-Path $scriptDir ".env"
if (-not (Test-Path $envPath)) {
    Write-Host ""
    Write-Host "❌ Erreur: fichier .env non trouvé" -ForegroundColor Red
    Write-Host "   Veuillez copier .env.example vers .env et configurer votre clé API" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Activer venv
& $venvPath

# Lancer le CLI en mode interactif
$cliPath = Join-Path $scriptDir "cli.py"
if ($Arguments) {
    python $cliPath interactive @Arguments
} else {
    python $cliPath interactive
}
