  # 🚀 QUICK START - Agent IA CLI

Démarrage rapide en 5 minutes!

---

## ⚡ Installation (2 min)

### 1. Vérifier les prérequis
```bash
python --version      # Python 3.11+
pip --version         # pip installé
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

**OU** (recommandé: utiliser un virtualenv)
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# OU
venv\Scripts\activate           # Windows (PowerShell)
pip install -r requirements.txt
```

### 3. Configurer l'API Claude
```bash
cp .env.example .env
```

Éditer `.env` et ajouter votre clé:
```
ANTHROPIC_API_KEY=sk-ant-ABC123...    # Votre clé API réelle
MODEL_NAME=claude-3-5-haiku-20241022
```

(Obtenir une clé: https://console.anthropic.com/)

---

## ✨ Utilisation (3 min)

### Commande simple
```bash
python cli.py "Lire le fichier README.md"
```

### Avec options
```bash
# Mode debug
python cli.py "Mon instruction" --debug

# Afficher l'historique
python cli.py "Mon instruction" --show-history

# Sauvegarder l'historique
python cli.py "Mon instruction" --history-file /tmp/history.json

# Tout ensemble
python cli.py "Instruction" --debug --show-history --history-file /tmp/h.json
```

---

## 🧪 Tester rapidement (2 exemples)

### Test 1: Lecture de fichier (Phase 1)
```bash
python cli.py "Lis le fichier requirements.txt"
```
**Résultat expected:** Affiche le contenu du fichier

### Test 2: Créer un fichier (Phase 2)
```bash
python cli.py "Crée un fichier test.txt avec 'Hello World'"
```
**Résultat expected:** Fichier créé avec succès

### Test 3: Sécurité (Phase 3)
```bash
python cli.py "Supprime test.txt"
```
**Résultat expected:** Demande confirmation interactive

---

## 📚 Fonctionnalités

| Phase | Capacity | Exemples |
|-------|----------|----------|
| **1** | Lecture fichier | Lire, lister, infos |
| **2** | Manipulation | Créer, éditer, deletion |
| **2** | Commandes | echo, ls, cat, grep, date... |
| **3** | Sécurité | Validation, whitelist, confirmations |
| **4** | Historique | Persist, stats, contexte |

---

## 🎓 Exemples pratiques

```bash
# Phase 1 - Lecture
python cli.py "Affiche le contenu de cli.py"
python cli.py "Quels fichiers sont dans le dossier courant?"

# Phase 2 - Créer
python cli.py "Crée un fichier myfile.txt contenant 'Coucou!'"

# Phase 2 - Éditer
python cli.py "Édite myfile.txt en rajoutant une 2e ligne"

# Phase 2 - Exécuter commande
python cli.py "Exécute la commande: date"

# Phase 3 - Sécurité (refusé)
python cli.py "Lis ../../../etc/passwd"    # ❌ Refusé

# Phase 4 - Historique
python cli.py "Info sur cli.py" --show-history --history-file ~/.agent_h.json
```

---

## 🐛 Debug

Activer le mode debug pour voir tous les détails:
```bash
python cli.py "Mon instruction" --debug
```

Affiche:
- Messages [DEBUG] détaillés
- Appels LLM complets
- Validations sécurité
- Temps d'exécution

---

## 🐳 Avec Docker (optionnel)

```bash
# Build l'image
docker build -t agent-cli .

# Run
docker run --rm \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  agent-cli \
  "Lire le fichier requirements.txt"
```

---

## ❓ Erreurs communes

### Erreur: "ANTHROPIC_API_KEY not configured"
**Solution:** Vérifier que `.env` existe et contient votre clé API valide

### Erreur: "Module not found: anthropic"
**Solution:** Installer les dépendances: `pip install -r requirements.txt`

### Erreur: "Python 3.11 required"
**Solution:** Upgrade Python: `python --version` (doit être 3.11+)

### Erreur: "timeout"
**Solution:** Vérifier votre internet, ou augmenter timeout dans `execute_command()` si besoin

---

## 📖 Documentation complète

- **README.md** - Guide détaillé avec tous les exemples
- **IMPLEMENTATION.md** - Architecture technique
- **DEMO.sh / DEMO.ps1** - Scripts de démonstration complète
- **CHECKLIST.md** - Status du projet

---

## 🎯 Prochaines étapes

1. **Tester** l'installation basique (Test 1 above)
2. **Explorer** les fonctionnalités (lire le README)
3. **Essayer** les exemples (Phase 1-4)
4. **Exécuter** la démo complète (`DEMO.sh` ou `DEMO.ps1`)

---

## ✅ Vérification rapide

```bash
# 1. Vérifier requirements.txt
cat requirements.txt

# 2. Vérifier .env est configuré
echo "ANTHROPIC_API_KEY est: $(grep ANTHROPIC_API_KEY .env | cut -d= -f2)"

# 3. Tester l'installation
python -c "import anthropic; print('✅ OK')"

# 4. Exécuter test simple
python cli.py "Test"
```

---

## 🚀 Vous êtes prêt!

Pour commencer:
```bash
python cli.py "Dis-moi bonjour!"
```

Enjoy! 🎉

---

**Questions?** Consultez README.md ou IMPLEMENTATION.md
