# Makefile - Agent IA CLI
# Commandes utiles pour développement et déploiement

.PHONY: help install dev clean test demo run docker-build docker-run lint format requirements

VENV := venv
PYTHON := python3
PIP := $(VENV)/bin/pip
PYTHON_VENV := $(VENV)/bin/python

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

# Default target
help:
	@echo "$(GREEN)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║          Agent IA CLI - Makefile Commands                  ║$(NC)"
	@echo "$(GREEN)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Installation & Setup:$(NC)"
	@echo "  make install         - Installer les dépendances"
	@echo "  make dev             - Setup environnement développement (venv + install)"
	@echo "  make requirements    - Générer requirements.txt à partir du project"
	@echo ""
	@echo "$(YELLOW)Exécution:$(NC)"
	@echo "  make run CMD='...'   - Exécuter le CLI avec instruction (ex: make run CMD='Lire README.md')"
	@echo "  make demo            - Exécuter démo complète (12 exemples)"
	@echo "  make test            - Tester l'installation"
	@echo ""
	@echo "$(YELLOW)Development:$(NC)"
	@echo "  make lint            - Vérifier la qualité du code (pylint/flake8)"
	@echo "  make format          - Formater le code (black)"
	@echo "  make clean           - Nettoyer fichiers temporaires"
	@echo ""
	@echo "$(YELLOW)Docker:$(NC)"
	@echo "  make docker-build    - Builder l'image Docker"
	@echo "  make docker-run      - Exécuter avec Docker (nécessite Docker installé)"
	@echo ""
	@echo "$(YELLOW)Documentation:$(NC)"
	@echo "  make help            - Afficher cette aide"
	@echo ""

# Installation des dépendances
install:
	@echo "$(GREEN)Installation des dépendances...$(NC)"
	$(PIP) install --upgrade pip 2>/dev/null || pip install --upgrade pip
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Installation complète!$(NC)"

# Setup environnement développement
dev:
	@echo "$(GREEN)Setup environnement développement...$(NC)"
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV)" python -m venv $(VENV)
	@echo Setup venv Windows...
	call $(VENV)\Scripts\activate.bat
else
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "Setup venv Unix..."
	. $(VENV)/bin/activate
endif
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "$(GREEN)✅ Environnement développement prêt!$(NC)"
	@echo "$(YELLOW)Pour activer le venv:$(NC)"
ifeq ($(OS),Windows_NT)
	@echo "  $(VENV)\Scripts\activate"
else
	@echo "  source $(VENV)/bin/activate"
endif

# Configuration de l'API
configure:
	@echo "$(YELLOW)Configuration de l'API...$(NC)"
	@if [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✅ Fichier .env créé!$(NC)"; \
		echo "$(RED)❌ Veuillez éditer .env et ajouter votre ANTHROPIC_API_KEY$(NC)"; \
	else \
		echo "$(GREEN)✅ .env déjà configuré$(NC)"; \
	fi

# Exécuter le CLI
run: configure
	@echo "$(GREEN)Exécution: $(CMD)$(NC)"
	python cli.py "$(CMD)"

# Test simple
test: configure
	@echo "$(GREEN)Test d'installation...$(NC)"
	python cli.py "Vérifie que tu fonctionnes en disant: 'Agent IA CLI v1.0 - Opérationnel!' "
	@echo "$(GREEN)✅ Test réussi!$(NC)"

# Exécuter démo complète
demo: configure
ifeq ($(OS),Windows_NT)
	@echo "$(GREEN)Exécution démo PowerShell...$(NC)"
	powershell.exe -ExecutionPolicy Bypass -File .\DEMO.ps1
else
	@echo "$(GREEN)Exécution démo Bash...$(NC)"
	bash DEMO.sh
endif

# Lint du code
lint:
	@echo "$(YELLOW)Vérification du code...$(NC)"
	@command -v pylint >/dev/null 2>&1 || pip install pylint
	@echo "$(GREEN)Pylint sur src/...$(NC)"
	pylint src/ --fail-under=8 2>/dev/null || echo "$(YELLOW)Avertissements de qualité encontrés$(NC)"
	@echo "$(GREEN)✅ Lint terminé$(NC)"

# Format du code
format:
	@echo "$(YELLOW)Formatage du code...$(NC)"
	@command -v black >/dev/null 2>&1 || pip install black
	black src/ cli.py --line-length 100
	@echo "$(GREEN)✅ Formatage complété$(NC)"

# Générer requirements.txt
requirements:
	@echo "$(YELLOW)Génération requirements.txt...$(NC)"
	pip freeze > requirements_generated.txt
	@echo "$(GREEN)✅ requirements_generated.txt créé$(NC)"
	@echo "$(YELLOW)Fichier actuel: requirements.txt$(NC)"
	@echo "$(YELLOW)Fichier généré: requirements_generated.txt$(NC)"

# Build Docker
docker-build:
	@echo "$(GREEN)Build image Docker...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker n'est pas installé$(NC)"; exit 1; }
	docker build -t agent-cli:latest .
	@echo "$(GREEN)✅ Image Docker construite!$(NC)"
	@echo "$(YELLOW)Tag: agent-cli:latest$(NC)"

# Run Docker
docker-run: docker-build
	@echo "$(GREEN)Exécution avec Docker...$(NC)"
	@if [ -z "$(ANTHROPIC_API_KEY)" ]; then \
		echo "$(RED)❌ Erreur: ANTHROPIC_API_KEY non définie$(NC)"; \
		exit 1; \
	fi
	docker run --rm -e ANTHROPIC_API_KEY=$(ANTHROPIC_API_KEY) agent-cli:latest "$(CMD)"

# Nettoyer fichiers temporaires
clean:
	@echo "$(YELLOW)Nettoyage...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info 2>/dev/null || true
	rm -f *.log 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage complété$(NC)"

# Full clean (inclut venv)
clean-all: clean
	@echo "$(RED)Suppression de l'environnement virtuel...$(NC)"
ifeq ($(OS),Windows_NT)
	@if exist "$(VENV)" rmdir /s /q $(VENV)
else
	@if [ -d "$(VENV)" ]; then rm -rf $(VENV); fi
endif
	@echo "$(GREEN)✅ Environnement virtuel supprimé$(NC)"

# Afficher status
status:
	@echo "$(GREEN)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║              Agent IA CLI - Status du Projet               ║$(NC)"
	@echo "$(GREEN)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC)"
	@python3 --version || python --version
	@echo ""
	@echo "$(YELLOW)Dépendances installées:$(NC)"
	@pip list | grep -E "anthropic|typer|python-dotenv" || echo "  Non installées - Exécutez: make install"
	@echo ""
	@echo "$(YELLOW)Configuration .env:$(NC)"
	@if [ -f ".env" ]; then \
		echo "  $(GREEN)✅ Présent$(NC)"; \
		grep ANTHROPIC_API_KEY .env | cut -d'=' -f1 || echo "  $(RED)❌ API key non configurée$(NC)"; \
	else \
		echo "  $(RED)❌ Absent$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Fichiers du projet:$(NC)"
	@ls -la src/*.py | wc -l | xargs echo "  Modules:" || true
	@find . -name "*.md" | wc -l | xargs echo "  Documentation:" || true
	@echo ""

# Vérification système
check:
	@echo "$(GREEN)Vérification système...$(NC)"
	@echo ""
	@echo "$(YELLOW)1. Python$(NC)"
	@python3 --version || python --version || echo "$(RED)❌ Python non trouvé$(NC)"
	@echo ""
	@echo "$(YELLOW)2. pip$(NC)"
	@pip3 --version || pip --version || echo "$(RED)❌ pip non trouvé$(NC)"
	@echo ""
	@echo "$(YELLOW)3. Dépendances requises$(NC)"
	@python3 -c "import anthropic; print('  ✅ anthropic')" 2>/dev/null || echo "  ❌ anthropic manquante"
	@python3 -c "import typer; print('  ✅ typer')" 2>/dev/null || echo "  ❌ typer manquante"
	@python3 -c "import dotenv; print('  ✅ dotenv')" 2>/dev/null || echo "  ❌ dotenv manquante"
	@echo ""
	@echo "$(YELLOW)4. Fichiers importants$(NC)"
	@[ -f "cli.py" ] && echo "  ✅ cli.py" || echo "  ❌ cli.py manquant"
	@[ -f ".env" ] && echo "  ✅ .env" || echo "  ❌ .env manquant"
	@[ -d "src" ] && echo "  ✅ src/" || echo "  ❌ src/ manquant"
	@echo ""
	@echo "$(GREEN)Vérification complétée!$(NC)"

# Info projet
info:
	@echo "$(GREEN)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║          Agent IA CLI - Informations Projet                ║$(NC)"
	@echo "$(GREEN)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Statistiques:$(NC)"
	@wc -l src/*.py cli.py 2>/dev/null | tail -1 | awk '{print "  Lignes de code: " $$1}' || echo "  Code source non accessible"
	@find . -name "*.md" | wc -l | xargs echo "  Fichiers documentation:"
	@ls -d */ | wc -l | xargs echo "  Répertoires:"
	@echo ""
	@echo "$(YELLOW)URL utiles:$(NC)"
	@echo "  Anthropic API: https://console.anthropic.com"
	@echo "  Documentation: Lire README.md"
	@echo "  Quick Start: Lire QUICK_START.md"
	@echo ""

.DEFAULT_GOAL := help
