from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete, procedure

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
def modifier_reservation(id_reserv, date_debut, date_fin, status_reser, id_client, id_vehic, id_tarif, id_assurance, id_optio, prix_total):
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

            curseur.execute(
                queriesupdate.MODIFIER_RESERVATION,
                (date_debut, date_fin, status_reser, id_client, id_vehic, id_tarif, id_assurance, id_optio, prix_total, id_reserv),
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


# Lister toutes les réservations
def lister_toutes_reservations():
    """Retourne une liste de toutes les réservations avec les détails associés."""
    connexion = database.connecter()
    reservations = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_RESERVATIONS)
            resultats = curseur.fetchall()

            for reservation in resultats:
                reservations.append((
                    reservation.ID_RESERV,
                    reservation.DATE_DEBUT,
                    reservation.DATE_FIN,
                    reservation.STATUS_RESER,
                    reservation.DUREE_JOUR,
                    reservation.ID_CLIENT,
                    reservation.ID_VEHIC,
                    reservation.ID_TARIF,
                    reservation.ID_ASSURANCE,
                    reservation.ID_OPTIO,
                    reservation.PRIX_TOTAL
                ))

        except Exception as erreur:
            print(f"Erreur lors de la récupération des réservations : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return reservations


# Rechercher une réservation par ID client, véhicule ou date
def rechercher_reservation(terme_recherche):
    """Recherche une réservation par ID du client, ID du véhicule ou date et retourne les résultats sous forme de tableau."""
    connexion = database.connecter()
    colonnes = ["ID", "Date Début", "Date Fin", "Statut", "Durée (jours)", "Client", "Véhicule", "Tarif", "Assurance", "Options", "Prix Total"]
    reservations = []

    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"  

            requete = """
                SELECT r.ID_RESERV, r.DATE_DEBUT, r.DATE_FIN, r.STATUS_RESER, r.DUREE_JOUR,
                       r.ID_CLIENT, r.ID_VEHIC, r.ID_TARIF, r.ID_ASSURANCE, r.ID_OPTIO, r.PRIX_TOTAL
                FROM RESERVATIONS r
                WHERE CAST(r.ID_CLIENT AS TEXT) LIKE ? OR 
                      CAST(r.ID_VEHIC AS TEXT) LIKE ? OR 
                      r.DATE_DEBUT LIKE ?
            """

            curseur.execute(requete, (terme, terme, terme))  
            resultats = curseur.fetchall()

            for reservation in resultats:
                reservations.append([
                    reservation.ID_RESERV,
                    reservation.DATE_DEBUT,
                    reservation.DATE_FIN,
                    reservation.STATUS_RESER,
                    reservation.DUREE_JOUR,
                    reservation.ID_CLIENT,
                    reservation.ID_VEHIC,
                    reservation.ID_TARIF,
                    reservation.ID_ASSURANCE,
                    reservation.ID_OPTIO,
                    reservation.PRIX_TOTAL
                ])

        except Exception as erreur:
            print(f"Erreur lors de la recherche de réservation : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, reservations


# Afficher la liste des réservations à modifier
def afficher_liste_reservations_modifier():
    """
    Récupère la liste des réservations sous forme de tableau de données.
    """
    colonnes = ["ID", "Date Début", "Date Fin", "Statut", "Durée (jours)", "Client", "Véhicule", "Tarif", "Assurance", "Options", "Prix Total"]
    reservations = []

    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_RESERVATIONS)
            resultats = curseur.fetchall()

            for reservation in resultats:
                reservations.append([
                    reservation.ID_RESERV,
                    reservation.DATE_DEBUT,
                    reservation.DATE_FIN,
                    reservation.STATUS_RESER,
                    reservation.DUREE_JOUR,
                    reservation.ID_CLIENT,
                    reservation.ID_VEHIC,
                    reservation.ID_TARIF,
                    reservation.ID_ASSURANCE,
                    reservation.ID_OPTIO,
                    reservation.PRIX_TOTAL
                ])

        except Exception as erreur:
            print(f"Erreur lors de la récupération des réservations : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, reservations


# Afficher la liste des réservations à supprimer
def afficher_liste_reservations_supprimer():
    """
    Récupère la liste des réservations sous forme de tableau de données pour suppression.
    """
    colonnes = ["ID", "Date Début", "Date Fin", "Statut", "Durée (jours)", "Client", "Véhicule", "Tarif", "Assurance", "Options", "Prix Total"]
    reservations = []

    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_RESERVATIONS)
            resultats = curseur.fetchall()

            for reservation in resultats:
                reservations.append([
                    reservation.ID_RESERV,
                    reservation.DATE_DEBUT,
                    reservation.DATE_FIN,
                    reservation.STATUS_RESER,
                    reservation.DUREE_JOUR,
                    reservation.ID_CLIENT,
                    reservation.ID_VEHIC,
                    reservation.ID_TARIF,
                    reservation.ID_ASSURANCE,
                    reservation.ID_OPTIO,
                    reservation.PRIX_TOTAL
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

