from base_donnees import database
from requetes_sql import queriesinputs

from base_donnees import database
from requetes_sql import queriesinputs
import pyodbc

def ajouter_incident(type_incident, date_incident, couts, details, id_contrat):
    """Ajoute un incident à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_INCIDENT,
                (type_incident, date_incident, couts, details, id_contrat)
            )
            connexion.commit()
            print("⚠️ Incident ajouté avec succès !")
            return True
        except pyodbc.IntegrityError as erreur:
            if "UNIQUE KEY constraint" in str(erreur):
                print("⚠️ Un incident est déjà enregistré pour ce contrat.")
                return "incident_existe"
            print(f"❌ Erreur d'intégrité : {erreur}")
            return False
        except Exception as erreur:
            print(f"❌ Erreur générale lors de l'ajout de l'incident : {erreur}")
            return False
        finally:
            database.fermer_connexion(connexion)

