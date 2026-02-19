"""
Validateur de sécurité - Phase 3
Valide les actions pour prévenir les comportements dangereux
"""

import logging
import re
from pathlib import Path
from typing import Tuple, List

logger = logging.getLogger(__name__)


class SafetyValidator:
    """Valide la sécurité des actions de l'agent"""
    
    # Whitelist stricte des commandes autorisées
    ALLOWED_COMMANDS = {
        'ls', 'cat', 'grep', 'echo', 'mkdir', 'touch', 
        'cp', 'mv', 'pwd', 'whoami', 'date', 'find', 'wc',
        'dir', 'type', 'cd', 'rmdir'  # Variantes Windows sûres
    }
    
    # Mots-clés dangereux à surveiller
    DANGEROUS_KEYWORDS = {
        'rm', 'rm -rf', 'del', 'erase', 'format',
        'sudo', 'su', 'chmod', 'chown',
        'DROP', 'DELETE FROM', 'TRUNCATE',
        'mkfs', 'dd', 'fdisk', 'shutdown', 'reboot',
        'curl', 'wget', 'nc', 'bash', 'sh'
    }
    
    # Chemins système sensibles interdit
    FORBIDDEN_PATHS = {
        '/', '/etc', '/sys', '/proc', '/root', '/var',
        '/usr/bin', '/bin', '/sbin', '/boot',
        'C:\\Windows', 'C:\\System32', 'C:\\Program Files',
        '..', '../'
    }
    
    def __init__(self, working_dir: str = "."):
        """
        Initialise le validateur de sécurité
        
        Args:
            working_dir: Répertoire de travail autorisé
        """
        self.working_dir = Path(working_dir).resolve()
        logger.info(f"SafetyValidator initialisé avec working_dir: {self.working_dir}")
    
    def validate_file_path(self, path: str) -> Tuple[bool, str]:
        """
        Valide qu'un chemin est sûr.
        
        Prévient:
        - Traversée de répertoire (..)
        - Accès aux chemins absolus sensibles
        - Accès en dehors du working_dir
        
        Args:
            path: Chemin à valider
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not path:
            return False, "Chemin vide"
        
        # Vérifier les patterns dangereux
        path_lower = path.lower().replace('\\', '/')
        if '..' in path_lower or path_lower.startswith('/'):
            return False, f"❌ Traversée de répertoire interdite: {path}"
        
        # Vérifier les chemins sensibles (utiliser des word boundaries pour éviter les faux positifs)
        # Par exemple, '/' est sensible (accès racine) mais pas un séparateur de chemin
        forbidden_keywords = ['/etc', '/sys', '/proc', '/root', '/var', '/usr/bin', '/bin', '/sbin', '/boot',
                             'C:\\Windows', 'C:\\System32', 'C:\\Program Files']
        
        for forbidden in forbidden_keywords:
            if forbidden.lower() in path_lower:
                return False, f"❌ Accès au chemin sensible interdit: {path}"
        
        # Vérifier que le chemin résolu reste dans working_dir
        try:
            full_path = (self.working_dir / path).resolve()
            if not str(full_path).startswith(str(self.working_dir)):
                return False, f"❌ L'action sortirait du répertoire de travail: {path}"
        except Exception as e:
            return False, f"❌ Chemin invalide: {path} ({str(e)})"
        
        return True, ""
    
    def is_command_safe(self, command: str) -> Tuple[bool, str]:
        """
        Valide qu'une commande est sûre d'exécuter.
        
        Vérifie:
        - La commande est dans la whitelist
        - Pas de mots-clés dangereux
        
        Args:
            command: Commande à valider
            
        Returns:
            Tuple (is_safe, error_message)
        """
        if not command:
            return False, "Commande vide"
        
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return False, "Commande vide"
        
        base_cmd = cmd_parts[0].lower()
        
        # Vérifier la whitelist
        if base_cmd not in self.ALLOWED_COMMANDS:
            return False, f"❌ Commande non autorisée: {base_cmd}"
        
        # Vérifier les keywords dangereux (avec limites de mots pour éviter les faux positifs)
        command_lower = command.lower()
        for keyword in self.DANGEROUS_KEYWORDS:
            # Utiliser des limites de mots (\b) pour éviter les correspondances partielles
            # Ex: 'su' ne matchera pas dans 'success' mais matchera dans 'su' seul
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, command_lower):
                return False, f"❌ Commande contient un pattern dangereux: {keyword}"
        
        return True, ""
    
    def get_dangerous_keywords(self) -> List[str]:
        """
        Retourne la liste des mots-clés dangereux détectés.
        
        Returns:
            Lista des keywords dangereux
        """
        return sorted(list(self.DANGEROUS_KEYWORDS))
    
    def confirm_dangerous_action(self, action_type: str, description: str) -> bool:
        """
        Demande confirmation pour une action potentiellement dangereuse.
        
        Args:
            action_type: Type d'action (delete_file, etc.)
            description: Description détaillée de l'action
            
        Returns:
            True si confirmation, False sinon
        """
        logger.warning(f"Action dangereuse détectée: {action_type}")
        logger.warning(f"Description: {description}")
        
        try:
            response = input(
                f"\n⚠️  ACTION DANGEREUSE DÉTECTÉE: {action_type}\n"
                f"Description: {description}\n"
                f"Êtes-vous CERTAIN? (oui/non): "
            )
            
            return response.lower() in ['oui', 'yes', 'o', 'y']
        except EOFError:
            # En cas d'entrée non disponible (scripts), refuser
            logger.error("Impossible de confirmer action dangereuse: pas d'entrée disponible")
            return False
    
    def validate_delete_action(self, path: str) -> Tuple[bool, str]:
        """
        Valide une action de suppression.
        
        Args:
            path: Fichier à supprimer
            
        Returns:
            Tuple (is_valid, error_message)
        """
        # Vérifier d'abord le chemin
        is_valid, error_msg = self.validate_file_path(path)
        if not is_valid:
            return False, error_msg
        
        # Suppression est dangereuse, demander confirmation
        if not self.confirm_dangerous_action(
            "delete_file",
            f"Supprimer le fichier: {path}"
        ):
            return False, "❌ Suppression annulée par l'utilisateur"
        
        return True, ""
