# ⚡ Démarrage Rapide - cliagent

## 🚀 Lancer le Mode Interactif

### Option 1: Direct Python (Recommandé)
```bash
python cli.py interactive
```

### Option 2: Via le script shell (WSL/Linux)
```bash
./cliagent.sh
# ou
bash cliagent.sh
```

### Option 3: Via le script PowerShell (Windows)
```powershell
.\cliagent.ps1
# ou simplement (après setup-alias)
cliagent
```

### Option 4: Via le script batch (Command Prompt/Windows)
```cmd
cliagent.bat
```

---

## 🎯 Utilisation du Mode Interactif

Une fois lancé, il y a plusieurs commandes:

### Commandes de l'Agent IA
Tapez n'importe quelle instruction en français:
```
🤖 Assistant> Dis bonjour
🤖 Assistant> Lire README.md
🤖 Assistant> Créer un fichier test.txt avec le contenu: Bonjour
🤖 Assistant> Lister les fichiers du répertoire
```

### Commandes Spéciales (internes)
```
🤖 Assistant> exit         # Quitter le mode interactif
🤖 Assistant> quit         # Alias pour exit
🤖 Assistant> history      # Afficher l'historique des actions
🤖 Assistant> clear        # Vider l'historique
🤖 Assistant> help         # Afficher cette aide
🤖 Assistant> pwd          # Afficher le répertoire courant
```

---

## 📋 Exemples Pratiques

### Exemple 1: Créer et lire un fichier
```
🤖 Assistant> Crée un fichier notes.txt avec le contenu: Mes notes importantes
⏳ Traitement...

✅ RÉSULTAT: Fichier créé...

🤖 Assistant> Lis le contenu du fichier notes.txt
⏳ Traitement...

✅ RÉSULTAT: Mes notes importantes
```

### Exemple 2: Lister les fichiers et en savoir plus
```
🤖 Assistant> Lister tous les fichiers du répertoire
🤖 Assistant> Affiche les informations du fichier cli.py
🤖 Assistant> Montre le répertoire courant
```

### Exemple 3: Session de travail
```
🤖 Assistant> pwd
📂 Répertoire: /mnt/c/Users/Tom/Documents/Github/BTP B2/Cli Agent

🤖 Assistant> history
📊 HISTORIQUE DES ACTIONS
Nombre total d'actions: 5
  ✅ Succès: 5
  ❌ Erreurs: 0

🤖 Assistant> exit
👋 Au revoir!
```

---

## 🔧 Configuration (Optionnel)

### Créer un alias PowerShell permanent

Si vous êtes sur Windows avec PowerShell:

```powershell
# Exécuter dans le répertoire du projet
.\setup-alias.ps1

# Recharger le profil
. $PROFILE

# Maintenant vous pouvez taper simplement
cliagent
```

### Ajouter au PATH (Windows)

Pour pouvoir taper `cliagent` depuis n'importe où:

1. Ouvrez les paramètres système (Windows + X → Paramètres)
2. Allez dans: Paramètres > Système > À propos > Paramètres avancés > Variables d'environnement
3. Sous "Variables utilisateur", cliquez "Nouveau..."
4. Nom: `PATH`
5. Valeur: `C:\Users\Tom\Documents\Github\BTP B2\Cli Agent`
6. Cliquez "OK" et redémarrez PowerShell

Puis vous pouvez taper `cliagent` partout!

---

## ⚙️ Options Avancées

### Avec répertoire de travail personnalisé
```bash
python cli.py interactive --working-dir ./data
```

### Avec historique persistant
```bash
python cli.py interactive --history-file ~/.agent_history.json
```

### Mode Debug (affiche les logs)
```bash
python cli.py interactive --debug
```

### Combinés
```bash
python cli.py interactive --working-dir ./projects --history-file ~/.agent.json --debug
```

---

## 💾 Modes d'Utilisation

### Mode One-Shot (une commande à la fois)
```bash
python cli.py "Dis bonjour"
python cli.py "Lire README.md"
```

### Mode Interactif (session continue) - **NOUVEAU!**
```bash
cliagent
# ou
python cli.py interactive
```

Le mode interactif vous permet de:
- ✅ Exécuter plusieurs commandes sans quitter
- ✅ Consulter l'historique entre les actions
- ✅ Changer de contexte facilement
- ✅ Bénéficier d'une meilleure expérience utilisateur

---

## 🐛 Dépannage

**"Le script n'existe pas"**
```bash
# Vérifier que vous êtes dans le bon répertoire
ls cliagent.sh  (Linux/WSL)
dir cliagent.ps1  (Windows PowerShell)
```

**"ANTHROPIC_API_KEY non configurée"**
```bash
# Copier le modèle .env
cp .env.example .env

# Éditer le fichier et ajouter votre clé API
# (voir QUICK_START.md pour les détails)
```

**PowerShell refuse d'exécuter le script**
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Fichiers Importants

- `cli.py` - Point d'entrée principal
- `cliagent.ps1` - Lanceur PowerShell
- `cliagent.sh` - Lanceur bash/WSL
- `cliagent.bat` - Lanceur Command Prompt
- `setup-alias.ps1` - Configuration de l'alias PowerShell
- `INTERACTIVE_MODE.md` - Guide détaillé du mode interactif
- `QUICK_START.md` - Guide initial de configuration

---

Bon chat avec votre Agent IA! 🚀
