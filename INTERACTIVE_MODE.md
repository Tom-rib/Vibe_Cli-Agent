# Mode Interactif - Guide de Démarrage Rapide

## 🚀 Accès Rapide

Trois façons de lancer le mode interactif:

### 1️⃣ **Windows (PowerShell)**
```powershell
# Direct (si dans le PATH)
cliagent

# Ou depuis le répertoire du projet
.\cliagent.ps1

# Ou en Python
python cli.py interactive
```

### 2️⃣ **Windows (Command Prompt)**
```cmd
:: Double-cliquez sur cliagent.bat
:: Ou depuis le répertoire du projet
cliagent.bat

:: Ou en Python
python cli.py interactive
```

### 3️⃣ **WSL/Linux**
```bash
# Depuis le répertoire du projet
./cliagent.sh
# ou
bash cliagent.sh

# Ou en Python
python cli.py interactive
```

---

## ⚙️ Configuration du PATH (Optionnel)

Pour pouvoir taper `cliagent` depuis n'importe où:

### **Option A: Windows PowerShell (Recommandé)**

1. Ouvrez PowerShell en tant qu'administrateur
2. Exécutez:
```powershell
# Créer un alias permanent
$profilePath = $PROFILE
if (!(Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force | Out-Null
}

# Ajouter la fonction au profil
@"
function cliagent {
    & "C:\Users\Tom\Documents\Github\BTP B2\Cli Agent\cliagent.ps1" @args
}
"@ | Add-Content $profilePath

# Recharger le profil
. $PROFILE
```

Maintenant vous pouvez taper `cliagent` depuis n'importe où!

### **Option B: Windows Command Prompt**

1. Créez un raccourci pour `copilot.bat` dans un dossier du PATH
2. Ou ajoutez le répertoire du projet au PATH système

### **Option C: WSL/Linux**

1. Créez un lien symbolique dans `/usr/local/bin`:
```bash
sudo ln -s /mnt/c/Users/Tom/Documents/Github/BTP\ B2/Cli\ Agent/cliagent.sh /usr/local/bin/cliagent
chmod +x /mnt/c/Users/Tom/Documents/Github/BTP\ B2/Cli\ Agent/cliagent.sh
```

2. Ou ajoutez le répertoire au PATH dans `~/.bashrc`:
```bash
export PATH="/mnt/c/Users/Tom/Documents/Github/BTP B2/Cli Agent:$PATH"
```

---

## 📝 Utilisation du Mode Interactif

Une fois lancé, vous verrez:
```
╔════════════════════════════════════════════════════════════════╗
║           🤖 AGENT IA CLI - MODE INTERACTIF                    ║
╚════════════════════════════════════════════════════════════════╝

💡 Commandes spéciales:
  • 'exit' ou 'quit' → Quitter le mode interactif
  • 'history' → Afficher l'historique des actions
  • 'clear' → Vider l'historique
  • 'help' → Afficher cette aide
  • 'pwd' → Afficher le répertoire courant

🤖 Assistant> 
```

### Exemples d'Utilisation

```
🤖 Assistant> Dis bonjour
⏳ Traitement...

============================================================
📋 Instruction: Dis bonjour
------------------------------------------------------------
🧠 Reasoning: L'utilisateur demande simplement un salut...
🎯 Action: execute_command
🔒 Sécurité: ✅ Commande echo sûre
⏱️  Temps d'exécution: 2.8s
------------------------------------------------------------
✅ RÉSULTAT:
Bonjour ! Je suis votre Assistant IA...
============================================================

🤖 Assistant> Lire README.md
⏳ Traitement...
[affiche le contenu du fichier]

🤖 Assistant> history
[affiche l'historique des actions]

🤖 Assistant> exit
👋 Au revoir!
```

---

## 🎯 Cas d'Usage

### Mode One-Shot (Traditionnel)
```bash
# Une seule commande, puis quitter
python cli.py "Dis bonjour"
python cli.py "Lire README.md"
```

### Mode Interactif (Nouveau!)
```bash
cliagent
# Lance une session continue où vous pouvez:
# - Créer plusieurs fichiers
# - Exécuter plusieurs commandes
# - Consulter l'historique entre les actions
# - Changer facilement de contexte
```

---

## 🔧 Options Avancées

### Avec répertoire de travail personnalisé
```bash
copilot --working-dir ./data
# Les fichiers seront créés/lus dans ./data/
```

### Avec historique persistant
```bash
copilot --history-file ~/.agent_history.json
# L'historique sera sauvegardé entre les sessions
```

### Mode Debug
```bash
copilot --debug
# Affiche les logs détaillés dans la console
```

### Combinés
```bash
python cli.py interactive --working-dir ./projects --history-file ~/.agent.json --debug
```

---

## 📌 Notes Importantes

1. **Fichier .env requis**: Assurez-vous que `.env` contient votre clé API Anthropic
2. **Virtual Environment**: Le script active automatiquement le `venv`
3. **Historique**: L'historique se réinitialise à chaque nouvelle session (sauf si `--history-file` est spécifié)
4. **Interruption**: Tapez `Ctrl+C` ou `exit` pour quitter

---

## 🐛 Dépannage

**Le script dit que venv n'existe pas**
```bash
# Créer le venv
python -m venv venv

# Installer les dépendances
pip install -r requirements.txt
```

**Le script dit que .env n'existe pas**
```bash
# Copier le modèle
cp .env.example .env

# Éditer .env et ajouter votre clé API
```

**PowerShell refuse d'exécuter le script**
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

Bon chat avec votre Assistant IA! 🚀
