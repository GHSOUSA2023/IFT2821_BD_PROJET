import pyodbc

CONFIGURATION_BD = {
    "DRIVER": "SQL Server",
    "SERVEUR": "localhost",
    "BASE_DE_DONNEES": "GNLOCATION",
    "UTILISATEUR": "appuser",
    "MOT_DE_PASSE": "ift2821h25",
}

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

def fermer_connexion(connexion):
    if connexion:
        connexion.close()

# ✅ Converte um único resultado em dict
def fetchone_dict(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# ✅ Converte uma lista de resultados em liste de dicts
def fetchall_dict(cursor):
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
