#!/bin/bash
# Script bash pour lancer l'Agent IA CLI en mode interactif (WSL/Linux)
# Usage: ./copilot.sh ou copilot (si dans le PATH)

# Déterminer le répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Vérifier venv
VENV_ACTIVATE="$SCRIPT_DIR/venv/bin/activate"
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo ""
    echo "❌ Erreur: virtualenv non trouvé"
    echo "   Veuillez exécuter: python -m venv venv"
    echo ""
    exit 1
fi

# Vérifier .env
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo ""
    echo "❌ Erreur: fichier .env non trouvé"
    echo "   Veuillez copier .env.example vers .env et configurer votre clé API"
    echo ""
    exit 1
fi

# Activer venv
source "$VENV_ACTIVATE"

# Lancer le CLI en mode interactif
python "$SCRIPT_DIR/cli.py" interactive "$@"
