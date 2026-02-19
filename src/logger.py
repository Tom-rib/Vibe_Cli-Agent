"""
Logger centralisé - Phase 4
Configuration unifiée du logging pour tous les modules
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class Logger:
    """Configuration centralisée du logging"""
    
    _configured = False
    
    @staticmethod
    def configure(
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        format_string: Optional[str] = None
    ) -> None:
        """
        Configure le logging de l'application
        
        Args:
            level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
            log_file: Chemin optionnel pour le fichier de log
            format_string: Format personnalisé pour les logs
        """
        if Logger._configured:
            return
        
        if format_string is None:
            format_string = (
                '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
            )
        
        formatter = logging.Formatter(format_string)
        
        # Configuration du logger root
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Handler console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # Handler fichier optionnel
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            root_logger.info(f"Log fichier activé: {log_file}")
        
        Logger._configured = True
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Retourne un logger configuré pour un module
        
        Args:
            name: Nom du module (__name__)
            
        Returns:
            Logger instance
        """
        return logging.getLogger(name)


# Alias pour simplicité
def get_logger(name: str) -> logging.Logger:
    """Retourne un logger pour le module spécifié"""
    return Logger.get_logger(name)
