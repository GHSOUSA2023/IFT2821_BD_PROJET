from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete, procedure, views

# ----------------------------- FONCTIONS POUR RÉSERVATIONS -----------------------------
# Ajouter une réservation via procédure stockée
def ajouter_reservation_via_procedure(id_client, id_vehic, date_debut, date_fin, id_tarif, id_assurance, id_optio):
    """Appelle la procédure stockée pour ajouter une réservation et vérifie le prix total calculé."""
    connexion = database.connecter(auto_commit=True)
    id_reservation = None
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(procedure.AJOUTER_RESERVATION_PROCEDURE,
                (id_client, id_vehic, date_debut, date_fin, id_tarif, id_assurance, id_optio))
            
            result = curseur.fetchone()
            if result:
                id_reservation = result.ID_RESERV
                print(f"Réservation ajoutée avec succès (ID: {id_reservation})")

                # Vérification du prix total calculé
                curseur.execute("SELECT PRIX_TOTAL FROM RESERVATIONS WHERE ID_RESERV = ?", (id_reservation,))
                prix_total = curseur.fetchone()

        except Exception as erreur:
            print(f"Erreur lors de l'ajout de la réservation via la procédure : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return id_reservation




# Confirmer une réservation (mettre à jour le statut à 'CONFIRMEE')
def confirmer_reservation(id_reserv):
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute("""
                UPDATE RESERVATIONS SET STATUS_RESER = 'CONFIRMEE' 
                WHERE ID_RESERV = ?
            """, (id_reserv,))
            connexion.commit()
            print(f"Réservation {id_reserv} confirmée avec succès.")
        except Exception as erreur:
            print(f"Erreur lors de la confirmation de la réservation : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Ajouter une réservation
def ajouter_reservation(date_debut, date_fin, status_reser, id_client, id_vehic, id_tarif, id_assurance, id_optio, prix_total):
    """Ajoute une nouvelle réservation à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_RESERVATION,
                (date_debut, date_fin, status_reser, id_client, id_vehic, id_tarif, id_assurance, id_optio, prix_total),
            )
            connexion.commit()
            print("Réservation ajoutée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de la réservation : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Modifier une réservation
def modifier_reservation(id_reserv, date_debut, date_fin, status_reser, id_vehic, id_tarif, id_assurance, id_optio):
    """Modifie les informations d'une réservation existante."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si la réservation existe avant modification
            curseur.execute(queries.GET_RESERVATION_PAR_ID, (id_reserv,))
            reservation = curseur.fetchone()
            if not reservation:
                print("Aucune réservation trouvée avec cet ID.")
                return

            # Exécuter la mise à jour
            curseur.execute(
                queriesupdate.MODIFIER_RESERVATION,
                (date_debut, date_fin, status_reser, id_vehic, id_tarif, id_assurance, id_optio, id_reserv),
            )
            connexion.commit()
            print("Réservation modifiée avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la modification de la réservation : {erreur}")
        finally:
            database.fermer_connexion(connexion)



# Supprimer une réservation
def supprimer_reservation(id_reserv):
    """Supprime une réservation par son ID après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si la réservation existe avant suppression
            curseur.execute(queries.GET_RESERVATION_PAR_ID, (id_reserv,))
            reservation = curseur.fetchone()

            if not reservation:
                print("Aucune réservation trouvée avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_RESERVATION, (id_reserv,))
            connexion.commit()
            print("Réservation supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de la réservation : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister toutes les réservations avec les détails étendus depuis la vue VIEW_RESERVATION_DETAILS
def lister_toutes_reservations():
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


# Rechercher une réservation dans la vue détaillée
def rechercher_reservation(terme_recherche):
    """
    Recherche des réservations dans la vue VIEW_RESERVATION_DETAILS
    par ID réservation, ID contrat ou nom du client.
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
            terme = f"%{terme_recherche.lower()}%"  # Minuscule pour correspondre à NOM_CLIENT en minuscules
            curseur.execute(views.RECHERCHER_RESERVATIONS, (terme, terme, terme))
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
            print(f"Erreur lors de la recherche des réservations détaillées : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, reservations


# Afficher la liste des réservations à supprimer
def afficher_liste_reservations_supprimer():
    """
    Récupère la liste des réservations sous forme de tableau de données pour suppression,
    affichant les mêmes champs que dans le tableau client.
    """
    colonnes = [
        "Nº réservation",
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
            print(f"Erreur lors de la récupération des réservations : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, reservations


# Annuler une réservation (mettre à jour le statut à 'ANNULEE')
def annuler_reservation(id_reserv):
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesupdate.UPDATE_STATUS_RESERVATION_ANNULEE, (id_reserv,))

            connexion.commit()
            print(f"Réservation {id_reserv} annulée avec succès.")
        except Exception as erreur:
            print(f"Erreur lors de l'annulation de la réservation : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer une réservation par son ID
def get_reservation_par_id(id_reserv):
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_RESERVATION_DETAILS_PAR_ID, (id_reserv,))
            row = curseur.fetchone()
            if row:
                colonnes = [desc[0] for desc in curseur.description]
                reservation = dict(zip(colonnes, row))
                return reservation
        except Exception as erreur:
            print(f"Erreur lors de la récupération de la réservation par ID : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

