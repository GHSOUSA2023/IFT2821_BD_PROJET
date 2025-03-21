import pyodbc

# Configuration de la connexion à la base de données
CONFIGURATION_BD = {
    "DRIVER": "SQL Server",
    "SERVEUR": "localhost",
    "BASE_DE_DONNEES": "GNLOCATION",
    "UTILISATEUR": "appuser",
    "MOT_DE_PASSE": "ift2821h25",
}


# Fonction pour établir une connexion avec la base de données
def connecter(auto_commit=False):
    try:
        connexion = pyodbc.connect(
            f"DRIVER={CONFIGURATION_BD['DRIVER']};"
            f"SERVER={CONFIGURATION_BD['SERVEUR']};"
            f"DATABASE={CONFIGURATION_BD['BASE_DE_DONNEES']};"
            f"UID={CONFIGURATION_BD['UTILISATEUR']};"
            f"PWD={CONFIGURATION_BD['MOT_DE_PASSE']}"
        )
        connexion.autocommit = auto_commit
        return connexion
    except Exception as erreur:
        print(f"Erreur de connexion à la base de données : {erreur}")
        return None



# Fonction pour fermer la connexion à la base de données
def fermer_connexion(connexion):
    if connexion:
        connexion.close()
