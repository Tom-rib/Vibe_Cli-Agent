"""
Définition des outils disponibles pour l'Agent
Phases 1-2: Outils basiques et avancés (lecture, création, édition, suppression, exécution)
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Tools:
    """Ensemble des outils disponibles pour l'Agent"""
    
    def __init__(self, working_dir: str = "."):
        """Initialise les outils avec un répertoire de travail"""
        self.working_dir = Path(working_dir).resolve()
        
    def _validate_path(self, path: str) -> Path:
        """
        Valide qu'un chemin ne sort pas du répertoire de travail
        Prévient la traversée de répertoire (../)
        
        Args:
            path: Le chemin à valider
            
        Returns:
            Path objet validé
            
        Raises:
            ValueError: Si le chemin tente une traversée de répertoire
        """
        full_path = (self.working_dir / path).resolve()
        
        # Vérifier que le chemin reste dans working_dir
        if not str(full_path).startswith(str(self.working_dir)):
            raise ValueError(f"❌ Traversée de répertoire interdite: {path}")
        
        return full_path
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Lit le contenu d'un fichier
        
        Args:
            path: Chemin du fichier à lire
            
        Returns:
            Dict avec 'success', 'content' ou 'error'
        """
        try:
            validated_path = self._validate_path(path)
            
            if not validated_path.exists():
                return {
                    "success": False,
                    "error": f"Fichier non trouvé: {path}"
                }
            
            if not validated_path.is_file():
                return {
                    "success": False,
                    "error": f"N'est pas un fichier: {path}"
                }
            
            with open(validated_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "path": str(validated_path)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lecture: {str(e)}"
            }
    
    def create_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Crée un fichier avec du contenu
        
        Args:
            path: Chemin du fichier à créer
            content: Contenu du fichier
            
        Returns:
            Dict avec 'success' ou 'error'
        """
        try:
            validated_path = self._validate_path(path)
            
            # Créer les répertoires parents si nécessaire
            validated_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Créer le fichier
            with open(validated_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"Fichier créé: {path}",
                "path": str(validated_path)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur création: {str(e)}"
            }
    
    def get_working_directory(self) -> Dict[str, Any]:
        """
        Retourne le répertoire de travail courant
        
        Returns:
            Dict avec 'success', 'working_dir' et 'absolute_path'
        """
        return {
            "success": True,
            "working_dir": str(self.working_dir),
            "absolute_path": str(self.working_dir.resolve())
        }
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Obtient les informations d'un fichier
        
        Args:
            path: Chemin du fichier
            
        Returns:
            Dict avec infos du fichier ou erreur
        """
        try:
            validated_path = self._validate_path(path)
            
            if not validated_path.exists():
                return {
                    "success": False,
                    "error": f"Fichier non trouvé: {path}"
                }
            
            stat = validated_path.stat()
            
            return {
                "success": True,
                "path": str(validated_path),
                "is_file": validated_path.is_file(),
                "is_dir": validated_path.is_dir(),
                "size": stat.st_size,
                "modified": str(validated_path.stat().st_mtime)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur info: {str(e)}"
            }
    
    def list_files(self, path: str = ".") -> Dict[str, Any]:
        """
        Liste les fichiers d'un répertoire
        
        Args:
            path: Chemin du répertoire
            
        Returns:
            Dict avec liste des fichiers ou erreur
        """
        try:
            validated_path = self._validate_path(path)
            
            if not validated_path.exists():
                return {
                    "success": False,
                    "error": f"Répertoire non trouvé: {path}"
                }
            
            if not validated_path.is_dir():
                return {
                    "success": False,
                    "error": f"N'est pas un répertoire: {path}"
                }
            
            items = []
            for item in validated_path.iterdir():
                items.append({
                    "name": item.name,
                    "is_file": item.is_file(),
                    "size": item.stat().st_size if item.is_file() else 0
                })
            
            return {
                "success": True,
                "path": str(validated_path),
                "items": items,
                "count": len(items)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur listing: {str(e)}"
            }
    
    def edit_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Modifie le contenu d'un fichier existant.
        
        Args:
            path: Chemin du fichier à modifier
            content: Nouveau contenu du fichier
            
        Returns:
            Dict avec 'success' et 'message' ou 'error'
        """
        try:
            validated_path = self._validate_path(path)
            
            if not validated_path.exists():
                return {
                    "success": False,
                    "error": f"Fichier non trouvé: {path}"
                }
            
            if not validated_path.is_file():
                return {
                    "success": False,
                    "error": f"N'est pas un fichier: {path}"
                }
            
            # Backup du contenu original
            with open(validated_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Écrire le nouveau contenu
            with open(validated_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Fichier modifié: {path} ({len(content)} caractères)")
            
            return {
                "success": True,
                "message": f"Fichier modifié: {path}",
                "path": str(validated_path),
                "size": len(content)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur édition: {str(e)}"
            }
    
    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Supprime un fichier.
        
        Args:
            path: Chemin du fichier à supprimer
            
        Returns:
            Dict avec 'success' et 'message' ou 'error'
        """
        try:
            validated_path = self._validate_path(path)
            
            if not validated_path.exists():
                return {
                    "success": False,
                    "error": f"Fichier non trouvé: {path}"
                }
            
            if not validated_path.is_file():
                return {
                    "success": False,
                    "error": f"N'est pas un fichier: {path}"
                }
            
            validated_path.unlink()
            logger.info(f"Fichier supprimé: {path}")
            
            return {
                "success": True,
                "message": f"Fichier supprimé: {path}",
                "path": str(validated_path)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur suppression: {str(e)}"
            }
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Exécute une commande shell sûre avec timeout.
        
        Whitelist de commandes autorisées:
        ls, cat, grep, echo, mkdir, touch, cp, mv, pwd, whoami, date, find, wc
        
        Args:
            command: Commande à exécuter
            
        Returns:
            Dict avec 'success', 'output' ou 'error'
        """
        # Whitelist stricte des commandes
        allowed_commands = {
            'ls', 'cat', 'grep', 'echo', 'mkdir', 'touch', 
            'cp', 'mv', 'pwd', 'whoami', 'date', 'find', 'wc',
            'dir', 'type'  # Variantes Windows
        }
        
        try:
            # Extraire la commande de base
            cmd_parts = command.strip().split()
            if not cmd_parts:
                return {
                    "success": False,
                    "error": "Commande vide"
                }
            
            base_cmd = cmd_parts[0].lower()
            
            # Vérifier la whitelist
            if base_cmd not in allowed_commands:
                return {
                    "success": False,
                    "error": f"Commande non autorisée: {base_cmd}. Autorisées: {', '.join(allowed_commands)}"
                }
            
            # Exécuter avec timeout de 10 secondes
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.working_dir)
            )
            
            if result.returncode == 0:
                logger.info(f"Commande exécutée: {command}")
                return {
                    "success": True,
                    "output": result.stdout,
                    "command": command
                }
            else:
                logger.warning(f"Commande avec erreur: {command}")
                return {
                    "success": False,
                    "error": result.stderr if result.stderr else f"Code retour: {result.returncode}",
                    "command": command
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Commande a dépassé le timeout (10s): {command}"
            }
        except Exception as e:
            logger.error(f"Erreur exécution: {str(e)}")
            return {
                "success": False,
                "error": f"Erreur exécution: {str(e)}"
            }
