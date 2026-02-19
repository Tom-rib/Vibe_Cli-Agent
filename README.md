# 🤖 Agent IA CLI - Intelligent File & Task Automation

Un assistant IA intelligent en ligne de commande qui vous aide à créer, lire, modifier et gérer des fichiers avec une interface conversationnelle naturelle. Alimenté par **Claude (Anthropic)** avec des mesures de sécurité robustes.

---

## ✨ Fonctionnalités Principales

### 🎯 **8 Outils Intégrés**
- 📖 **read_file** - Lire le contenu des fichiers
- ✍️ **create_file** - Créer de nouveaux fichiers avec contenu
- ✏️ **edit_file** - Modifier le contenu existant
- 🗑️ **delete_file** - Supprimer des fichiers (avec confirmation)
- 📂 **list_files** - Lister les fichiers d'un répertoire
- ⚙️ **execute_command** - Exécuter des commandes shell sûres
- 📍 **get_working_directory** - Afficher le répertoire courant
- ℹ️ **get_file_info** - Obtenir les infos (taille, permissions, etc.)

### 🔒 **Sécurité Multi-Niveaux**
- ✅ Validation stricte des chemins (pas de traversée de répertoire)
- ✅ Whitelist de commandes (uniquement: ls, cat, grep, echo, mkdir, touch, cp, mv, pwd, whoami, date, find, wc)
- ✅ Blocage de 25+ mots-clés dangereux (rm, sudo, chmod, DROP, etc.)
- ✅ Confirmations interactives pour les actions dangereuses
- ✅ LLM strictement instructionné en Français pour respecter les règles de sécurité

### 📝 **Historique & Logging**
- 📊 Suivi complet de toutes les actions exécutées
- 💾 Persistance optionnelle en JSON
- 📋 Logs détaillés avec timestamps ISO

### 💬 **Deux Modes d'Interaction**

#### Mode One-Shot
```bash
python cli.py "Crée un fichier test.txt avec du contenu"
python cli.py "Lire le fichier README.md"
```

#### Mode Interactif (NOUVEAU! ⭐)
```bash
cliagent
# ou
python cli.py interactive
```

Lance une **session de chat continu** avec l'agent où vous pouvez:
- Exécuter plusieurs commandes sans quitter
- Consulter l'historique en cours de session
- Utiliser des commandes spéciales (exit, history, help, pwd, clear)

---

## 🚀 Démarrage Rapide

### 1️⃣ Installation

```bash
# Cloner/naviguer vers le projet
cd "Cli Agent"

# Créer l'environnement Python
python -m venv venv

# Activer l'environnement
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Ou WSL/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2️⃣ Configuration

```bash
# Copier le modèle d'environnement
cp .env.example .env

# Éditer .env et ajouter votre clé API Anthropic
# ANTHROPIC_API_KEY=sk-ant-...
```

Obtenez votre clé API gratuitement: https://console.anthropic.com/

### 3️⃣ Lancer le CLI

#### **Windows PowerShell (Recommandé)**
```powershell
.\cliagent.ps1
# Ou après setup-alias.ps1:
cliagent
```

#### **Windows Command Prompt**
```cmd
cliagent.bat
```

#### **WSL/Linux/Bash**
```bash
./cliagent.sh
# ou
bash cliagent.sh
# ou direct Python:
python cli.py interactive
```

---

## 💡 Exemples d'Utilisation

### Mode Interactif

```bash
$ cliagent

╔════════════════════════════════════════════════════════════════╗
║           🤖 AGENT IA CLI - MODE INTERACTIF                    ║
╚════════════════════════════════════════════════════════════════╝

📁 Répertoire de travail: /path/to/creations_ia

🤖 Assistant> Crée un fichier liste_courses.txt avec mes courses
⏳ Traitement...

✅ RÉSULTAT:
Fichier créé: liste_courses.txt

🤖 Assistant> Lis le fichier liste_courses.txt
⏳ Traitement...

✅ RÉSULTAT:
- Lait
- Pain
- Oeufs
- Fromage

🤖 Assistant> Modifie le fichier, ajoute "Beurre" à la fin
⏳ Traitement...

✅ RÉSULTAT:
Fichier modifié

🤖 Assistant> Lister les fichiers du répertoire
⏳ Traitement...

✅ RÉSULTAT:
Items: 5
  - liste_courses.txt
  - autre_file.txt
  - ...

🤖 Assistant> exit
👋 Au revoir!
```

### Mode One-Shot

```bash
# Créer un fichier
python cli.py "Crée un fichier welcome.txt avec: Bienvenue!"

# Lire un fichier
python cli.py "Lis le contenu du fichier welcome.txt"

# Avec options avancées
python cli.py "Crée rapport.md" --working-dir ./rapports --debug
```

---

## 📂 Structure du Projet

```
cli-agent/
├── cli.py                      # Point d'entrée principal
├── cliagent.ps1               # Lanceur PowerShell
├── cliagent.sh                # Lanceur Bash/WSL
├── cliagent.bat               # Lanceur Command Prompt
├── setup-alias.ps1            # Configuration alias PowerShell
├── requirements.txt           # Dépendances Python
├── .env.example               # Template variables
├── .gitignore                 # Fichiers ignorés par Git
├── Makefile                   # Commandes utiles
├── Dockerfile                 # Conteneurisation
│
├── src/                        # Modules IA
│   ├── agent.py              # Orchestration IA
│   ├── llm_interface.py       # Interface Claude API
│   ├── tools.py              # 8 outils implémentés
│   ├── executor.py           # Routeur d'actions
│   ├── safety.py             # Validateur sécurité
│   ├── history.py            # Gestionnaire historique
│   └── logger.py             # Logging centralisé
│
├── creations_ia/              # 📂 Dossier de travail par défaut
│   └── (fichiers créés par l'IA)
│
├── README.md                  # Ce fichier
├── QUICK_START.md            # Guide setup détaillé
├── QUICK_USE.md              # Guide d'utilisation
├── INTERACTIVE_MODE.md       # Mode interactif doc
└── IMPLEMENTATION.md         # Détails techniques
```

---

## ⚙️ Options Avancées

### Mode One-Shot Personnalisé

```bash
# Avec répertoire custom
python cli.py "Instruction" --working-dir ./mon_dossier

# Avec historique persistant
python cli.py "Instruction" --history-file ~/.agent_history.json

# Mode Debug (logs détaillés)
python cli.py "Instruction" --debug

# Afficher l'historique avant
python cli.py "Instruction" --show-history

# Effacer l'historique
python cli.py "Instruction" --clear-history

# Combinés
python cli.py "Instruction" --working-dir ./data --debug --show-history
```

### Mode Interactif Personnalisé

```bash
# Autre répertoire
python cli.py interactive --working-dir ./projects

# Historique persistant
python cli.py interactive --history-file ~/.my_agent.json

# Debug mode
python cli.py interactive --debug

# Tous ensemble
python cli.py interactive --working-dir ./work --history-file ~/.agent.json --debug
```

### Commandes Spéciales en Mode Interactif

```
exit          # Quitter la session
quit          # Alias pour exit
history       # Afficher l'historique des actions
clear         # Vider l'historique
help          # Afficher l'aide
pwd           # Afficher le répertoire courant
```

---

## 🔧 Configuration

### .env (REQUIS)

```bash
# Copier depuis .env.example
cp .env.example .env

# Éditer avec votre clé API
ANTHROPIC_API_KEY=sk-ant-...
```

### Alias PowerShell Permanent (Optionnel)

```powershell
# Une seule fois
.\setup-alias.ps1

# Puis recharger le profil
. $PROFILE

# Maintenant vous pouvez taper simplement:
cliagent
```

### Makefile

```bash
make help           # Afficher les commandes disponibles
make install        # Installer les dépendances
make run            # Lancer le CLI interactif
make test           # Tester la configuration
make docker-build   # Construire l'image Docker
make docker-run     # Exécuter dans Docker
make clean          # Nettoyer les fichiers temporaires
```

---

## 🐳 Docker (Optionnel)

```bash
# Construire l'image
make docker-build

# Exécuter dans Docker
make docker-run

# Ou directement:
docker build -t cliagent .
docker run -it --env-file .env cliagent
```

---

## 🔐 Sécurité - Détails

L'agent respecte **5 niveaux de sécurité**:

### 1️⃣ Validation des Chemins
- ✅ Empêche la traversée de répertoire (`..`)
- ✅ Bloque les chemins absolus depuis la racine
- ✅ Confine les opérations au `working_dir`

### 2️⃣ Whitelist de Commandes
Commandes autorisées uniquement:
```
ls, cat, grep, echo, mkdir, touch, cp, mv, pwd, 
whoami, date, find, wc, dir, type
```

### 3️⃣ Filtrage de Mots-Clés
Prévention de commandes dangereuses:
```
rm, sudo, su, chmod, chown, DROP, DELETE FROM,
mkfs, dd, curl, wget, bash, sh, ...
```

### 4️⃣ Confirmations Interactives
Les actions dangereuses demandent confirmation:
```
⚠️  ACTION DANGEREUSE DÉTECTÉE: delete_file
Description: Supprimer /path/to/file.txt
Êtes-vous CERTAIN? (oui/non):
```

### 5️⃣ Prompting Stricts au LLM
L'agent Claude reçoit des instructions strictes de sécurité en Français pour respecter toutes les règles.

---

## 📊 Architecture

### Phase 1️⃣: Fondations
- ✅ 5 outils de base (read, create, list, pwd, info)
- ✅ Interface Claude API
- ✅ Logger centralisé

### Phase 2️⃣: Tooling & Exécution
- ✅ 3 outils avancés (edit, delete, execute_command)
- ✅ Routing des actions
- ✅ Whitelist de commandes

### Phase 3️⃣: Sécurité
- ✅ SafetyValidator multi-niveaux
- ✅ Validations de chemins
- ✅ Confirmations interactives

### Phase 4️⃣: Raffinement
- ✅ Historique persistant
- ✅ Logging avec timestamps
- ✅ Contexte d'historique au LLM

### Phase 5️⃣ (Bonus): Mode Interactif
- ✅ Session conversationnelle continue
- ✅ Commandes spéciales (exit, history, help, pwd)
- ✅ Default working_dir `creations_ia/`

---

## 📚 Documentation Supplémentaire

- **[QUICK_START.md](QUICK_START.md)** - Guide détaillé de setup
- **[QUICK_USE.md](QUICK_USE.md)** - Guide d'utilisation complet
- **[INTERACTIVE_MODE.md](INTERACTIVE_MODE.md)** - Documentation mode interactif
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Détails techniques d'implémentation

---

## 🐛 Dépannage

### "ANTHROPIC_API_KEY non configurée"
```bash
# Créer .env depuis le template
cp .env.example .env

# Éditer et ajouter votre clé
# Voir: https://console.anthropic.com/
```

### "virtualenv non trouvé"
```bash
# Créer le venv
python -m venv venv

# Activer et installer
source venv/bin/activate  # Linux/WSL
.\venv\Scripts\Activate.ps1  # PowerShell
pip install -r requirements.txt
```

### "PowerShell refuse d'exécuter le script"
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Les fichiers ne se créent pas dans `creations_ia/`
```bash
# Vérifier le working_dir
python cli.py interactive --working-dir creations_ia

# Ou utiliser directement:
cliagent  # Utilise creations_ia/ par défaut
```

---

## 🎯 Cas d'Usage

### 📝 Gestion de Tâches
```
🤖 Assistant> Crée un fichier TODO.md avec mes tâches pour la semaine
🤖 Assistant> Ajoute une nouvelle tâche "Finaliser le projet"
🤖 Assistant> Montre-moi les tâches restantes
```

### 📊 Analyse de Données
```
🤖 Assistant> Lis le fichier data.csv
🤖 Assistant> Modifie le fichier pour corriger les erreurs
🤖 Assistant> Exporte en format JSON
```

### 🧪 Développement
```
🤖 Assistant> Crée un fichier script.py avec du code Python
🤖 Assistant> Exécute le script
🤖 Assistant> Lis les résultats
```

---

## 📈 Performance

- **Temps moyen de réponse**: 2-4 secondes (dépendent de l'API Claude)
- **Taille maximale de fichier**: Illimitée (limites API Claude appliquées)
- **Commandes par session**: Illimitées
- **Historique**: Jusqu'à 100 actions en mémoire

---

## 🤝 Contribution & Amélioration

Suggérations pour améliorations futures:
- [ ] Support de plusieurs modèles LLM (GPT, Ollama, etc.)
- [ ] Implémentation DAC (Discretionary Access Control)
- [ ] Rate limiting avec cache
- [ ] Support de pipelines (chaîner des commandes)
- [ ] Interface Web/GUI
- [ ] Synchronisation cloud
- [ ] Plugins personnalisés

---

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

---

## 🎉 Prêt à Commencer?

```bash
# Installation rapide
python -m venv venv
source venv/bin/activate  # Linux/WSL ou .\venv\Scripts\Activate.ps1 (Windows)
pip install -r requirements.txt
cp .env.example .env

# Éditer .env avec votre clé API

# Lancer!
cliagent
```

**Bon chat avec votre Agent IA!** 🚀
