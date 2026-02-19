"""
Point d'entrée CLI avec Typer - Phase 4
Interface ligne de commande pour l'Agent IA
Support de l'historique des actions et meilleur formatting
"""

import typer
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from src.agent import Agent
from src.logger import Logger

# Charger les variables d'environnement depuis .env
load_dotenv()

app = typer.Typer(
    help="Agent IA CLI - Exécute des tâches avec intelligence artificielle"
)

def check_env():
    """Vérifie que les variables d'environnement requises sont présentes"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        typer.echo("❌ Erreur: ANTHROPIC_API_KEY non configurée")
        typer.echo("   Veuillez créer un fichier .env avec votre clé API")
        typer.echo("   Voir .env.example pour le modèle")
        raise typer.Exit(code=1)

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    instruction: str = typer.Argument(None, help="L'instruction pour l'agent ou une commande (interactive, history)"),
    working_dir: str = typer.Option(".", help="Répertoire de travail pour l'agent"),
    debug: bool = typer.Option(False, "--debug", help="Mode debug activé"),
    history_file: str = typer.Option(None, "--history-file", help="Fichier pour persister l'historique"),
    show_history: bool = typer.Option(False, "--show-history", help="Afficher l'historique avant d'exécuter"),
    clear_history: bool = typer.Option(False, "--clear-history", help="Vider l'historique au démarrage")
):
    """
    Lance l'Agent IA pour traiter une instruction ou une commande
    
    Exemples:
        python cli.py "Lire le fichier README.md"
        python cli.py interactive (pour mode interactif)
        python cli.py history (pour voir l'historique)
        python cli.py "Créer test.txt" --working-dir ./data
        python cli.py "Lire file.txt" --history-file ~/.agent_history.json --show-history
    """
    # Si une commande a été invoquée (history, interactive), ne rien faire ici
    if ctx.invoked_subcommand is not None:
        return
    
    # Vérifier si l'instruction est en fact une commande connue
    if instruction in ["interactive", "history"]:
        # Rediriger vers la commande appropriée
        if instruction == "interactive":
            # Pour le mode interactif, utiliser creations_ia par défaut si working_dir est "."
            final_working_dir = "creations_ia" if working_dir == "." else working_dir
            ctx.invoke(interactive, working_dir=final_working_dir, history_file=history_file, debug=debug)
        elif instruction == "history":
            ctx.invoke(history, working_dir=working_dir, history_file=history_file)
        return
    
    # Si pas d'instruction fournie, afficher l'aide
    if not instruction:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)
    
    # Vérifier l'environnement
    check_env()
    
    # Configurer le logging
    log_level = logging.DEBUG if debug else logging.INFO
    Logger.configure(
        level=log_level,
        log_file=os.path.join(working_dir, ".agent.log") if not debug else None
    )
    
    if debug:
        typer.echo("🔧 Mode DEBUG activé\n")
    
    # Vérifier que le répertoire de travail existe
    if not Path(working_dir).exists():
        typer.echo(f"❌ Erreur: Le répertoire de travail n'existe pas: {working_dir}")
        raise typer.Exit(code=1)
    
    try:
        # Créer l'agent (avec ou sans fichier d'historique)
        agent = Agent(working_dir=working_dir, history_file=history_file)
        
        # Vider l'historique si demandé
        if clear_history:
            agent.history.clear()
            typer.echo("✅ Historique vidé\n")
        
        # Afficher l'historique si demandé
        if show_history:
            typer.echo(agent.format_history_output())
        
        # Traiter l'instruction
        typer.echo(f"⏳ Traitement de: '{instruction}'\n")
        result = agent.process_request(instruction)
        
        # Afficher le résultat formaté
        formatted_output = agent.format_output(result)
        typer.echo(formatted_output)
        
        # Retourner le code de sortie approprié
        if result['status'] == 'error':
            raise typer.Exit(code=1)
        
    except KeyboardInterrupt:
        typer.echo("\n\n⚠️  Interruption par l'utilisateur")
        raise typer.Exit(code=130)
    except Exception as e:
        typer.echo(f"❌ Erreur fatale: {str(e)}")
        if debug:
            import traceback
            typer.echo(traceback.format_exc())
        raise typer.Exit(code=1)

@app.command()
def history(
    working_dir: str = typer.Option(".", help="Répertoire de travail de l'agent"),
    history_file: str = typer.Option(None, help="Fichier d'historique")
):
    """
    Affiche l'historique des actions exécutées
    
    Exemple:
        python cli.py history --history-file ~/.agent_history.json
    """
    check_env()
    
    try:
        agent = Agent(working_dir=working_dir, history_file=history_file)
        typer.echo(agent.format_history_output())
    except Exception as e:
        typer.echo(f"❌ Erreur: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def interactive(
    working_dir: str = typer.Option("creations_ia", help="Répertoire de travail pour l'agent (défaut: creations_ia)"),
    history_file: str = typer.Option(None, help="Fichier pour persister l'historique"),
    debug: bool = typer.Option(False, "--debug", help="Mode debug activé")
):
    """
    Lance le CLI en mode INTERACTIF - conversation continu avec l'agent
    
    Exemples:
        python cli.py interactive (utilise creations_ia par défaut)
        python cli.py interactive --working-dir ./data
        python cli.py interactive --debug
    """
    # Vérifier l'environnement
    check_env()
    
    # Configurer le logging
    log_level = logging.DEBUG if debug else logging.INFO
    Logger.configure(
        level=log_level,
        log_file=os.path.join(working_dir, ".agent.log") if not debug else None
    )
    
    if debug:
        typer.echo("🔧 Mode DEBUG activé\n")
    
    # Créer le répertoire de travail s'il n'existe pas
    work_path = Path(working_dir)
    if not work_path.exists():
        try:
            work_path.mkdir(parents=True, exist_ok=True)
            typer.echo(f"📁 Dossier créé: {working_dir}\n")
        except Exception as e:
            typer.echo(f"❌ Erreur: Impossible de créer le répertoire {working_dir}: {str(e)}")
            raise typer.Exit(code=1)
    
    try:
        # Créer l'agent
        agent = Agent(working_dir=working_dir, history_file=history_file)
        
        # Banner d'accueil
        typer.echo(f"""
╔════════════════════════════════════════════════════════════════╗
║           🤖 AGENT IA CLI - MODE INTERACTIF                    ║
╚════════════════════════════════════════════════════════════════╝

📁 Répertoire de travail: {work_path.resolve()}

💡 Commandes spéciales:
  • 'exit' ou 'quit' → Quitter le mode interactif
  • 'history' → Afficher l'historique des actions
  • 'clear' → Vider l'historique
  • 'help' → Afficher cette aide
  • 'pwd' → Afficher le répertoire courant

⚡ Tapez vos instructions en langage naturel:
  • "Créer un fichier (fichier.txt)"
  • "Lire un fichier"
  • "Lister les fichiers"
  • etc...

""")
        
        # Boucle interactive
        while True:
            try:
                # Afficher le prompt
                instruction = typer.prompt(
                    f"\n🤖 Assistant> ",
                    default=""
                ).strip()
                
                # Vérifier les commandes spéciales
                if not instruction:
                    continue
                
                if instruction.lower() in ['exit', 'quit', 'q']:
                    typer.echo("\n👋 Au revoir!")
                    break
                
                if instruction.lower() == 'history':
                    typer.echo(agent.format_history_output())
                    continue
                
                if instruction.lower() == 'clear':
                    agent.history.clear()
                    typer.echo("✅ Historique vidé\n")
                    continue
                
                if instruction.lower() == 'help':
                    typer.echo("""
💡 Commandes spéciales:
  • 'exit' ou 'quit' → Quitter
  • 'history' → Afficher l'historique
  • 'clear' → Vider l'historique
  • 'pwd' → Répertoire courant
  
📝 Exemples d'instructions:
  • "Lire README.md"
  • "Créer un fichier test.txt avec contenu"
  • "Lister les fichiers"
  • "Afficher mon répertoire de travail"
""")
                    continue
                
                if instruction.lower() == 'pwd':
                    typer.echo(f"📂 Répertoire: {Path(working_dir).resolve()}\n")
                    continue
                
                # Traiter l'instruction
                typer.echo(f"⏳ Traitement...\n")
                result = agent.process_request(instruction)
                
                # Afficher le résultat formaté
                formatted_output = agent.format_output(result)
                typer.echo(formatted_output)
                
            except KeyboardInterrupt:
                typer.echo("\n\n⚠️  Interruption par l'utilisateur")
                break
            except EOFError:
                typer.echo("\n👋 Au revoir!")
                break
        
    except Exception as e:
        typer.echo(f"❌ Erreur fatale: {str(e)}")
        if debug:
            import traceback
            typer.echo(traceback.format_exc())
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
