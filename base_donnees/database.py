import pyodbc

CONFIGURATION_BD = {
    "DRIVER": "ODBC Driver 17 for SQL Server",
    "SERVEUR": "localhost",
    "BASE_DE_DONNEES": "GNLOCATION",
}

def connecter(auto_commit=False):
    print("🔌 Tentative de connexion à la base de données (Windows Authentication)...")
    print("🛠️  Configuration utilisée :")
    for cle, valeur in CONFIGURATION_BD.items():
        print(f"   {cle} = {valeur}")

    try:
        connexion = pyodbc.connect(
            f"DRIVER={CONFIGURATION_BD['DRIVER']};"
            f"SERVER={CONFIGURATION_BD['SERVEUR']};"
            f"DATABASE={CONFIGURATION_BD['BASE_DE_DONNEES']};"
            f"Trusted_Connection=yes"
        )
        connexion.autocommit = auto_commit
        print("✅ Connexion réussie à la base de données !")
        return connexion
    except Exception as erreur:
        print("❌ Erreur de connexion à la base de données :")
        print(erreur)
        return None

def fermer_connexion(connexion):
    if connexion:
        connexion.close()
        print("🔒 Connexion fermée.")
