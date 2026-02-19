"""
Exécuteur d'actions - Phase 2-3
Route les actions décidées par le LLM vers les outils appropriés
Gère la sécurité: read_file, create_file, edit_file, delete_file, execute_command, etc.
"""

import logging
from typing import Any, Dict
from src.tools import Tools
from src.safety import SafetyValidator

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class Executor:
    """Exécute les actions décidées par l'Agent avec validation de sécurité"""
    
    def __init__(self, working_dir: str = "."):
        """Initialise l'exécuteur avec les outils et le validateur"""
        self.tools = Tools(working_dir=working_dir)
        self.safety = SafetyValidator(working_dir=working_dir)
        logger.debug(f"Executor initialisé avec working_dir: {working_dir}")
        
    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une action donnée avec les paramètres fournis
        Valide la sécurité avant exécution
        
        Args:
            action: Nom de l'action (read_file, create_file, edit_file, delete_file, execute_command, etc.)
            parameters: Paramètres pour l'action
            
        Returns:
            Dict avec le résultat de l'exécution
        """
        logger.debug(f"[Exécution] Action: {action} | Paramètres: {parameters}")
        
        try:
            if action == "read_file":
                path = parameters.get("path", "")
                is_valid, error_msg = self.safety.validate_file_path(path)
                if not is_valid:
                    logger.warning(f"Sécurité: lecture refusée - {error_msg}")
                    return {"success": False, "error": error_msg}
                logger.info(f"[Sécurité] ✅ Lecture autorisée: {path}")
                return self.tools.read_file(path)
            
            elif action == "create_file":
                path = parameters.get("path", "")
                is_valid, error_msg = self.safety.validate_file_path(path)
                if not is_valid:
                    logger.warning(f"Sécurité: création refusée - {error_msg}")
                    return {"success": False, "error": error_msg}
                logger.info(f"[Sécurité] ✅ Création autorisée: {path}")
                return self.tools.create_file(path, parameters.get("content", ""))
            
            elif action == "edit_file":
                path = parameters.get("path", "")
                is_valid, error_msg = self.safety.validate_file_path(path)
                if not is_valid:
                    logger.warning(f"Sécurité: édition refusée - {error_msg}")
                    return {"success": False, "error": error_msg}
                logger.info(f"[Sécurité] ✅ Édition autorisée: {path}")
                logger.debug(f"Modification de fichier: {path}")
                return self.tools.edit_file(path, parameters.get("content", ""))
            
            elif action == "delete_file":
                path = parameters.get("path", "")
                is_valid, error_msg = self.safety.validate_delete_action(path)
                if not is_valid:
                    logger.warning(f"Sécurité: suppression refusée - {error_msg}")
                    return {"success": False, "error": error_msg}
                logger.info(f"[Sécurité] ⚠️  Suppression confirmée: {path}")
                logger.debug(f"Suppression de fichier: {path}")
                return self.tools.delete_file(path)
            
            elif action == "execute_command":
                command = parameters.get("command", "")
                is_safe, error_msg = self.safety.is_command_safe(command)
                if not is_safe:
                    logger.warning(f"Sécurité: commande refusée - {error_msg}")
                    return {"success": False, "error": error_msg}
                logger.info(f"[Sécurité] ✅ Commande autorisée: {command}")
                logger.debug(f"Exécution de commande: {command}")
                return self.tools.execute_command(command)
            
            elif action == "get_working_directory":
                return self.tools.get_working_directory()
            
            elif action == "get_file_info":
                path = parameters.get("path", "")
                is_valid, error_msg = self.safety.validate_file_path(path)
                if not is_valid:
                    logger.warning(f"Sécurité: info fichier refusée - {error_msg}")
                    return {"success": False, "error": error_msg}
                return self.tools.get_file_info(path)
            
            elif action == "list_files":
                path = parameters.get("path", ".")
                is_valid, error_msg = self.safety.validate_file_path(path)
                if not is_valid:
                    logger.warning(f"Sécurité: listing refusé - {error_msg}")
                    return {"success": False, "error": error_msg}
                return self.tools.list_files(path)
            
            elif action == "error":
                return {
                    "success": False,
                    "error": "Erreur lors du traitement par le LLM"
                }
            
            else:
                logger.warning(f"Action inconnue: {action}")
                return {
                    "success": False,
                    "error": f"Action inconnue: {action}"
                }
                
        except Exception as e:
            logger.error(f"[Erreur Exécution] {str(e)}")
            return {
                "success": False,
                "error": f"Erreur exécution: {str(e)}"
            }
