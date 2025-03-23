from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete, procedure, views

# Lister toutes les réservations avec les détails étendus depuis la vue VIEW_RESERVATION_DETAILS
def lister_toutes_contrats():
    """
    Liste toutes les réservations avec les détails étendus depuis la vue VIEW_RESERVATION_DETAILS.
    """
    colonnes = [
        "Nº reservation",
        "Nº contrat",
        "Date début",
        "Date fin",
        "Nombre de jours",
        "Prix total",
        "Status du contrat",
        "Agence",
        "Nom client",
        "Véhicule"
    ]
    reservations = []

    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(views.GET_CONTRATS_TOUT)
            resultats = curseur.fetchall()

            for contrat in resultats:
                reservations.append([
                    contrat.ID_RESERV,
                    contrat.ID_CONTRACT,
                    contrat.CONTRAT_DATE_DEBUT,
                    contrat.CONTRAT_DATE_FIN,
                    contrat.CONTRAT_DUREE_JOURS,
                    contrat.CONTRAT_PRIX_TOTAL,
                    contrat.STATUS,
                    contrat.NOM_AGENCE,
                    contrat.NOM_CLIENT,
                    contrat.MODELE_VEHICULE
                ])
        except Exception as erreur:
            print(f"Erreur lors de la récupération des réservations détaillées : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, reservations
