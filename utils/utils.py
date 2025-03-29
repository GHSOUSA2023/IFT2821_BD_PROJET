import sys
import os

def resource_path(relative_path):
    """Retourne le chemin absolu du fichier dans l'exécutable ou en développement."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
