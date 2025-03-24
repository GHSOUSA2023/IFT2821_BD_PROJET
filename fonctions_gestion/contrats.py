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


def terminer_contrat(id_reservation, date_fin, prix_total, duree_jours):
    """
    Terminer un contrat en mettant à jour sa date de fin, son statut, la durée et le prix total.
    """
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesupdate.MODIFIER_CONTRAT, 
                (date_fin, 'TERMINEE', duree_jours, prix_total, id_reservation)
            )
            connexion.commit()
            return True
        except Exception as erreur:
            print(f"Erreur lors de la terminaison du contrat : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return False
