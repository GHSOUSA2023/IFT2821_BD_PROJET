from base_donnees import database
from requetes_sql import queriesrapports

def rapport_flotte_vehicules():
    """Retourne la liste de tous les véhicules de la flotte avec leur état et la présence éventuelle d'un contrat actif."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_FLOTTE_VEHICULES)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération du rapport flotte véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_clients_incidents_assurance():
    """Liste des clients impliqués dans des incidents ayant une incidence sur la valeur de l'assurance."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_CLIENTS_AVEC_INCIDENTS_ASSURANCE)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération du rapport clients/incidents : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_vehicules_incidents():
    """Liste de tous les véhicules ayant eu des incidents, avec le nombre d'incidents."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_VEHICULES_AVEC_INCIDENTS)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération du rapport véhicules/incidents : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_vehicules_disponibles_par_agence():
    """Quantité de véhicules disponibles par agence selon le type de voiture."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_VEHICULES_DISPONIBLES_PAR_AGENCE)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération du rapport véhicules disponibles par agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_entretien_par_agence():
    """Liste de l'état d'entretien des véhicules, par agence, employé responsable, et durée de l'entretien."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_ENTRETIEN_PAR_AGENCE)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération du rapport entretien par agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_vehicules_contrats_actifs():
    """Liste tous les véhicules avec contrats actifs."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_VEHICULES_CONTRATS_ACTIFS)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération des véhicules avec contrats actifs : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_employes_avec_incidents():
    """Liste des employés responsables ayant des contrats avec incidents, avec le nombre de contrats impliqués."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_EMPLOYES_AVEC_INCIDENTS)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération des employés avec incidents : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_reservations_agence_janvier():
    """Nombre de réservations par agence pour le mois de janvier."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_RESERVATIONS_PAR_AGENCE_JANVIER)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération des réservations de janvier : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_contrats_agence_janvier():
    """Nombre de contrats en cours par agence pour le mois de janvier."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_CONTRATS_PAR_AGENCE_JANVIER)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération des contrats de janvier : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []

def rapport_facturation_agence_par_mois():
    """Total de la facturation prévue et réalisée par agence et par mois."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesrapports.GET_FACTURATION_PAR_AGENCE_MOIS)
            colonnes = [desc[0] for desc in curseur.description]
            donnees = curseur.fetchall()
            return colonnes, donnees
        except Exception as erreur:
            print(f"Erreur lors de la récupération du rapport de facturation : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return [], []
