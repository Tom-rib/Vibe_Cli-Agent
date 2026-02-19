"""
Interface avec l'API Claude (Anthropic) - Phase 4
Gère la communication avec le modèle Haiku
Support du contexte d'historique pour meilleure coordination des actions
"""

import json
import os
import logging
from typing import Any, Dict, Optional, List
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class LLMInterface:
    """Interface pour communiquer avec Claude via l'API Anthropic"""
    
    def __init__(self, include_history: bool = False):
        """
        Initialise le client Anthropic avec la clé API depuis l'environnement
        
        Args:
            include_history: Si True, les actions précédentes sont inclues dans le prompt
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY non configurée dans les variables d'environnement")
        
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "claude-3-5-haiku-20241022")
        self.conversation_history = []
        self.include_history = include_history
        logger.info(f"LLMInterface initialisé | Model: {self.model} | History: {include_history}")
        
    
    def set_history_context(self, recent_actions: List[Dict[str, Any]]) -> None:
        """
        Définit le contexte d'historique pour les futurs appels au LLM
        
        Args:
            recent_actions: Liste des dernières actions exécutées
        """
        self.recent_actions = recent_actions
        logger.debug(f"Contexte historique défini: {len(recent_actions)} actions")
    
    def build_history_context(self, recent_actions: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Construit un contexte à partir de l'historique des actions
        
        Args:
            recent_actions: Actions récentes à inclure
            
        Returns:
            String avec le contexte d'historique
        """
        if not recent_actions or len(recent_actions) == 0:
            return ""
        
        history_text = "\n\nCONTEXTE D'HISTORIQUE (Actions précédentes):\n"
        history_text += "-" * 40 + "\n"
        
        for i, action in enumerate(recent_actions[-5:], 1):  # Afficher max 5 dernières
            status_symbol = "✅" if action.get("status") == "success" else "❌"
            history_text += f"{i}. {status_symbol} {action.get('action', '?')} "
            history_text += f"({action.get('execution_time', 0):.2f}s)\n"
            
            # Ajouter un résumé du résultat
            result = action.get("result", {})
            if isinstance(result, dict):
                if result.get("success"):
                    if "content" in result:
                        history_text += f"   Résultat: {result['content'][:100]}...\n"
                    elif "message" in result:
                        history_text += f"   Résultat: {result['message']}\n"
                else:
                    history_text += f"   Erreur: {result.get('error', 'Inconnue')}\n"
        
        history_text += (
            "\nUtilise ce contexte pour éviter de refaire les mêmes actions "
            "et pour coordonner les tâches logiquement.\n"
        )
        
        return history_text
    
    def build_system_prompt(self) -> str:
        """Construit le prompt système avec description des outils disponibles"""
        return """Tu es un Agent IA intelligent capable d'exécuter des commandes et manipuler des fichiers.

Outils disponibles:
1. read_file(path) - Lire le contenu d'un fichier
2. create_file(path, content) - Créer un nouveau fichier
3. edit_file(path, content) - Modifier le contenu d'un fichier
4. delete_file(path) - Supprimer un fichier (DANGEREUX - DEMANDER CONFIRMATION)
5. list_files(path) - Lister les fichiers d'un répertoire
6. execute_command(command) - Exécuter une commande système (SÛRE UNIQUEMENT)
7. get_working_directory() - Obtenir le répertoire courant
8. get_file_info(path) - Obtenir les informations d'un fichier

IMPORTANT: Toujours répondre au format JSON suivant:
{
  "reasoning": "Explication détaillée étape par étape de ta décision",
  "action": "Nom de l'action (read_file, create_file, edit_file, delete_file, execute_command, etc.)",
  "parameters": {
    "param1": "valeur1",
    "param2": "valeur2"
  },
  "safety_check": "✅ Décision AVEC justification de sécurité"
}

⚠️  RÈGLES DE SÉCURITÉ STRICTES - À RESPECTER ABSOLUMENT:

1. CHEMINS DE FICHIERS:
   - JAMAIS de traversée de répertoire (..)
   - JAMAIS de chemins absolus en dehors de la zone de travail
   - JAMAIS d'accès à des fichiers système sensibles (/etc, /sys, /root, etc.)
   - Tous les chemins doivent être relatifs au répertoire de travail

2. SUPPRESSION DE FICHIERS (delete_file):
   - Cette action est TRÈS DANGEREUSE
   - TOUJOURS expliquer POURQUOI la suppression est nécessaire
   - DEMANDER une confirmation explicite de l'utilisateur dans le reasoning
   - Exemple: "Je demande confirmation à l'utilisateur avant de supprimer X"

3. EXÉCUTION DE COMMANDES:
   - Seulement: ls, cat, grep, echo, mkdir, touch, cp, mv, pwd, whoami, date, find, wc
   - JAMAIS de: rm, rm -rf, del, sudo, su, chmod, chown, curl, wget, bash, sh
   - JAMAIS d'injection de commande
   - Pour echo: utiliser des guillemets doubles, pas des simples
   - Par exemple: echo "Bonjour le monde" (pas: echo 'Bonjour le monde' avec apostrophes)
   - Si le texte contient des guillemets doubles, utiliser des guillemets simples autour
   - Chaque commande a un timeout de 10 secondes

4. CONTENU DE FICHIERS:
   - Avant de modifier (edit_file) ou créer (create_file), expliquer le contenu
   - Vérifier que le contenu est sûr et pertinent

5. JUSTIFICATION DÉTAILLÉE:
   - Chaque action doit avoir une reasoning TRÈS claire
   - Mentionner les vérifications de sécurité effectuées
   - Si en doute, refuser l'action

Exemple de réponse CORRECTE:
{
  "reasoning": "L'utilisateur demande de lire README.md. Le chemin est relatif à la zone de travail et ne contient pas '..' - action sûre.",
  "action": "read_file",
  "parameters": {"path": "README.md"},
  "safety_check": "✅ Lecture sûre - chemin validé, pas de risque"
}

Exemple de réponse REFUSÉE:
{
  "reasoning": "L'utilisateur demande de supprimer /etc/passwd. C'est EXTRÊMEMENT DANGEREUX et en dehors de la zone autorisée.",
  "action": "error",
  "parameters": {},
  "safety_check": "❌ Action REFUSÉE - accès système interdit"
}"""
    
    def call_llm(self, user_instruction: str, recent_actions: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Appelle le modèle Claude avec une instruction utilisateur
        Optionnellement inclut un contexte d'historique
        
        Args:
            user_instruction: L'instruction de l'utilisateur
            recent_actions: Actions récentes optionnelles pour le contexte
            
        Returns:
            Dict contenant: reasoning, action, parameters, safety_check
        """
        try:
            # Construire le prompt utilisateur avec contexte d'historique optionnel
            user_prompt = user_instruction
            if recent_actions and self.include_history:
                user_prompt += self.build_history_context(recent_actions)
            
            # Ajouter le message utilisateur à l'historique
            self.conversation_history.append({
                "role": "user",
                "content": user_prompt
            })
            
            # Appel à l'API Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.build_system_prompt(),
                messages=self.conversation_history
            )
            
            # Extraire la réponse
            assistant_message = response.content[0].text
            
            # Ajouter la réponse à l'historique
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Parser la réponse JSON
            try:
                # Nettoyer la réponse (supprimer espaces avant/après)
                assistant_message = assistant_message.strip()
                
                # Extraire le premier objet JSON valide (gère les réponses multiples)
                if '{' in assistant_message:
                    start_idx = assistant_message.find('{')
                    # Compter les accolades pour trouver la fin du premier objet JSON
                    bracket_count = 0
                    end_idx = start_idx
                    for i in range(start_idx, len(assistant_message)):
                        if assistant_message[i] == '{':
                            bracket_count += 1
                        elif assistant_message[i] == '}':
                            bracket_count -= 1
                            if bracket_count == 0:
                                end_idx = i + 1
                                break
                    json_str = assistant_message[start_idx:end_idx]
                else:
                    json_str = assistant_message
                
                # Essayer de parser le JSON - si ça échoue, essayer de le nettoyer
                try:
                    result = json.loads(json_str)
                except json.JSONDecodeError as e:
                    # Si le parsing échoue, essayer de nettoyer les caractères problématiques
                    logger.warning(f"Problème JSON détecté: {str(e)}")
                    # Normaliser les newlines et caractères de contrôle indésirables
                    # Mais préserver la structure JSON valide
                    import re
                    # Remplacer les newlines à l'intérieur des strings avec des espaces
                    json_str_cleaned = json_str.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
                    # Supprimer les caractères de contrôle
                    json_str_cleaned = ''.join(char for char in json_str_cleaned if ord(char) >= 32 or char in '\t')
                    try:
                        result = json.loads(json_str_cleaned)
                    except json.JSONDecodeError:
                        # En dernier recours, utiliser la réponse brute
                        logger.error(f"Impossible de parser JSON: {json_str[:200]}")
                        raise
                
                logger.debug(f"Réponse LLM: {result.get('action', 'unknown')}")
                return result
            except json.JSONDecodeError:
                # Si le modèle n'a pas répondu en JSON valide
                logger.error(f"Réponse non-JSON: {assistant_message}")
                return {
                    "reasoning": "Réponse non structurée du modèle",
                    "action": "error",
                    "parameters": {},
                    "safety_check": f"❌ Réponse invalide: {assistant_message[:100]}..."
                }
                
        except Exception as e:
            return {
                "reasoning": "Erreur lors de l'appel API",
                "action": "error",
                "parameters": {},
                "safety_check": f"❌ Erreur API: {str(e)}"
            }
    
    def reset_conversation(self):
        """Réinitialise l'historique de conversation"""
        self.conversation_history = []
