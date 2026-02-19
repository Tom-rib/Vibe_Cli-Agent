"""
Agent IA principal - Phase 4
Orchestre la boucle complète: analyse → décision → exécution → résultat
Intègre l'historique des actions et meilleur logging
"""

import logging
import time
from typing import Any, Dict, Optional
from src.llm_interface import LLMInterface
from src.executor import Executor
from src.history import ActionHistory

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class Agent:
    """Agent IA qui traite les instructions utilisateur"""
    
    def __init__(self, working_dir: str = ".", history_file: Optional[str] = None):
        """
        Initialise l'agent avec LLM, Executor et historique
        
        Args:
            working_dir: Répertoire de travail
            history_file: Fichier optionnel pour charger/sauvegarder l'historique
        """
        self.llm = LLMInterface()
        self.executor = Executor(working_dir=working_dir)
        self.history = ActionHistory()
        self.history_file = history_file
        
        # Charger l'historique existant si fourni
        if history_file:
            self.history.load_from_file(history_file)
        
        logger.info(f"Agent initialisé | working_dir: {working_dir}")
        
    def process_request(self, instruction: str) -> Dict[str, Any]:
        """
        Traite une demande utilisateur complète:
        1. Envoi à Claude pour analyse/décision
        2. Exécution de l'action décidée
        3. Enregistrement dans l'historique
        4. Retour du résultat formaté
        
        Args:
            instruction: L'instruction de l'utilisateur
            
        Returns:
            Dict avec: instruction, reasoning, action, result, status, execution_time
        """
        start_time = time.time()
        logger.info(f"[Agent] Traitement de: '{instruction}'")
        
        # Étape 1: Appel au LLM pour décider l'action
        logger.info("[Agent] Analyse et décision via LLM...")
        # Transmettre les dernières actions au LLM pour le contexte
        recent_actions = self.history.get_recent_actions(count=5)
        llm_response = self.llm.call_llm(instruction, recent_actions=recent_actions)
        
        reasoning = llm_response.get("reasoning", "N/A")
        action = llm_response.get("action", "error")
        parameters = llm_response.get("parameters", {})
        safety_check = llm_response.get("safety_check", "N/A")
        
        logger.info(f"[Agent Reasoning] {reasoning}")
        logger.info(f"[Agent Decision] Action: {action}")
        logger.info(f"[Sécurité] {safety_check}")
        
        # Étape 2: Exécution de l'action
        logger.info(f"[Agent] Exécution de l'action: {action}")
        execution_result = self.executor.execute_action(action, parameters)
        
        # Calculer le temps d'exécution
        execution_time = time.time() - start_time
        
        # Détermine le statut (succès si aucune erreur)
        status = "success" if execution_result.get("success", True) else "error"
        
        # Étape 3: Enregistrement dans l'historique
        self.history.record_action(
            action=action,
            parameters=parameters,
            result=execution_result,
            reasoning=reasoning,
            execution_time=execution_time,
            status=status
        )
        
        # Sauvegarder l'historique si un fichier est spécifié
        if self.history_file:
            self.history.save_to_file(self.history_file)
        
        # Étape 4: Formatage du résultat
        result = {
            "instruction": instruction,
            "reasoning": reasoning,
            "action": action,
            "parameters": parameters,
            "security_check": safety_check,
            "execution_result": execution_result,
            "execution_time": execution_time,
            "status": status
        }
        
        logger.info(f"[Agent] Résultat: {status} ({execution_time:.3f}s)")
        
        return result
    
    def format_output(self, result: Dict[str, Any]) -> str:
        """
        Formate le résultat pour affichage utilisateur
        
        Args:
            result: Résultat de process_request
            
        Returns:
            String formaté pour affichage
        """
        output = []
        output.append("\n" + "="*60)
        output.append(f"📋 Instruction: {result['instruction']}")
        output.append("-"*60)
        output.append(f"🧠 Reasoning: {result['reasoning']}")
        output.append(f"🎯 Action: {result['action']}")
        output.append(f"🔒 Sécurité: {result['security_check']}")
        output.append(f"⏱️  Temps d'exécution: {result['execution_time']:.3f}s")
        output.append("-"*60)
        
        exec_result = result['execution_result']
        if result['status'] == 'success' and exec_result.get('success'):
            output.append("✅ RÉSULTAT:")
            if 'content' in exec_result:
                output.append(f"\n{exec_result['content']}")
            elif 'message' in exec_result:
                output.append(f"{exec_result['message']}")
            elif 'output' in exec_result:
                output.append(f"{exec_result['output']}")
            elif 'working_dir' in exec_result:
                output.append(f"Répertoire: {exec_result['working_dir']}")
            elif 'items' in exec_result:
                output.append(f"Items: {len(exec_result['items'])}")
                for item in exec_result['items'][:10]:  # Afficher max 10
                    size = item.get('size', 0)
                    item_type = 'dossier' if not item.get('is_file', False) else f'{size}b'
                    output.append(f"  - {item['name']} ({item_type})")
        else:
            output.append("❌ ERREUR:")
            error_msg = exec_result.get('error', 'Erreur inconnue')
            output.append(f"{error_msg}")
        
        output.append("="*60 + "\n")
        return "\n".join(output)
    
    def get_history_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé de l'historique des actions
        
        Returns:
            Statistiques et résumé
        """
        return self.history.to_dict()
    
    def format_history_output(self) -> str:
        """
        Formate l'historique pour affichage
        
        Returns:
            Historique formaté
        """
        summary = self.history.get_action_summary()
        output = []
        output.append("\n" + "="*60)
        output.append("📊 HISTORIQUE DES ACTIONS")
        output.append("-"*60)
        output.append(f"Nombre total d'actions: {summary['total_actions']}")
        output.append(f"  ✅ Succès: {summary['success_count']}")
        output.append(f"  ❌ Erreurs: {summary['error_count']}")
        output.append(f"Temps total d'exécution: {summary['total_execution_time']:.3f}s")
        
        if summary['total_actions'] > 0:
            output.append(f"Temps moyen: {summary['average_execution_time']:.3f}s")
            output.append(f"Première action: {summary['first_action']}")
            output.append(f"Dernière action: {summary['last_action']}")
            
            output.append("\n🔄 10 Dernières actions:")
            output.append("-"*60)
            for i, action in enumerate(self.history.get_recent_actions(10), 1):
                status_emoji = "✅" if action['status'] == 'success' else "❌"
                output.append(
                    f"{i}. {status_emoji} {action['action']} "
                    f"({action['execution_time']:.3f}s) - {action['timestamp']}"
                )
        
        output.append("="*60 + "\n")
        return "\n".join(output)
