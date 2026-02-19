"""
Historique des actions - Phase 4
Enregistre toutes les actions exécutées par l'agent
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ActionHistory:
    """Gère l'historique des actions exécutées"""
    
    def __init__(self, max_items: int = 100):
        """
        Initialise l'historique
        
        Args:
            max_items: Nombre maximum d'actions à conserver en mémoire
        """
        self.actions: List[Dict[str, Any]] = []
        self.max_items = max_items
        logger.info(f"ActionHistory initialisé (max: {max_items} actions)")
    
    def record_action(
        self,
        action: str,
        parameters: Dict[str, Any],
        result: Dict[str, Any],
        reasoning: str = "",
        execution_time: float = 0.0,
        status: str = "success"
    ) -> None:
        """
        Enregistre une action dans l'historique
        
        Args:
            action: Nom de l'action (read_file, create_file, etc.)
            parameters: Paramètres de l'action
            result: Résultat de l'exécution
            reasoning: Reasoning du LLM
            execution_time: Temps d'exécution en secondes
            status: Statut de l'action (success, error)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "parameters": parameters,
            "result": result,
            "reasoning": reasoning,
            "execution_time": execution_time,
            "status": status
        }
        
        self.actions.append(entry)
        
        # Limiter la taille en mémoire
        if len(self.actions) > self.max_items:
            removed = self.actions.pop(0)
            logger.debug(f"Historique tronqué: {len(self.actions)} actions conservées")
        
        logger.debug(f"Action enregistrée: {action} ({status}) - {execution_time:.3f}s")
    
    def get_recent_actions(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Retourne les N dernières actions
        
        Args:
            count: Nombre d'actions à retourner
            
        Returns:
            Liste des actions récentes
        """
        return self.actions[-count:] if self.actions else []
    
    def get_action_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé de l'historique
        
        Returns:
            Dict avec statistiques
        """
        if not self.actions:
            return {
                "total_actions": 0,
                "success_count": 0,
                "error_count": 0,
                "total_execution_time": 0.0
            }
        
        success_count = sum(1 for a in self.actions if a.get("status") == "success")
        error_count = sum(1 for a in self.actions if a.get("status") == "error")
        total_time = sum(a.get("execution_time", 0) for a in self.actions)
        
        return {
            "total_actions": len(self.actions),
            "success_count": success_count,
            "error_count": error_count,
            "total_execution_time": total_time,
            "average_execution_time": total_time / len(self.actions) if self.actions else 0,
            "first_action": self.actions[0].get("timestamp") if self.actions else None,
            "last_action": self.actions[-1].get("timestamp") if self.actions else None
        }
    
    def to_json(self) -> str:
        """
        Sérialise l'historique en JSON
        
        Returns:
            String JSON représentant l'historique
        """
        return json.dumps(self.actions, indent=2, default=str)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Retourne l'historique sous forme de dictionnaire
        
        Returns:
            Dict avec historique et statistiques
        """
        return {
            "summary": self.get_action_summary(),
            "actions": self.actions
        }
    
    def save_to_file(self, filepath: str) -> bool:
        """
        Sauvegarde l'historique dans un fichier JSON
        
        Args:
            filepath: Chemin du fichier de sauvegarde
            
        Returns:
            True si succès, False sinon
        """
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, default=str)
            
            logger.info(f"Historique sauvegardé: {filepath} ({len(self.actions)} actions)")
            return True
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde historique: {str(e)}")
            return False
    
    def load_from_file(self, filepath: str) -> bool:
        """
        Charge l'historique depuis un fichier JSON
        
        Args:
            filepath: Chemin du fichier de sauvegarde
            
        Returns:
            True si succès, False sinon
        """
        try:
            path = Path(filepath)
            if not path.exists():
                logger.warning(f"Fichier historique non trouvé: {filepath}")
                return False
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and "actions" in data:
                self.actions = data.get("actions", [])
            else:
                self.actions = data if isinstance(data, list) else []
            
            logger.info(f"Historique chargé: {filepath} ({len(self.actions)} actions)")
            return True
            
        except Exception as e:
            logger.error(f"Erreur chargement historique: {str(e)}")
            return False
    
    def clear(self) -> None:
        """Vide l'historique"""
        self.actions.clear()
        logger.info("Historique vidé")
