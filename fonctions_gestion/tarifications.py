from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ----------------------------- FONCTIONS POUR TARIFICATIONS -----------------------------

# Ajouter une tarification
def ajouter_tarification(km_jour, prix_locat_jour, id_tp_vehic):
    """Ajoute une nouvelle tarification à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_TARIFICATION,
                (km_jour, prix_locat_jour, id_tp_vehic),
            )
            connexion.commit()
            print("Tarification ajoutée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de la tarification : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Modifier une tarification
def modifier_tarification(id_tarif, km_jour, prix_locat_jour, id_tp_vehic):
    """Modifie une tarification existante."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesupdate.MODIFIER_TARIFICATION,
                (km_jour, prix_locat_jour, id_tp_vehic, id_tarif),
            )
            connexion.commit()
            print("Tarification modifiée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la modification de la tarification : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer une tarification
def supprimer_tarification(id_tarif):
    """Supprime une tarification par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesdelete.SUPPRIMER_TARIFICATION, (id_tarif,))
            connexion.commit()
            print("Tarification supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de la tarification : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister toutes les tarifications
def lister_toutes_tarifications():
    """Retourne la liste de toutes les tarifications enregistrées."""
    connexion = database.connecter()
    tarifications = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_TARIFICATIONS)
            resultats = curseur.fetchall()

            for tarif in resultats:
                tarifications.append([
                    tarif.ID_TARIF,
                    tarif.KM_JOUR,
                    tarif.PRIX_LOCAT_JOUR,
                    tarif.TYPE_VEHIC  # Remplace ID par le nom du type de véhicule
                ])

        except Exception as erreur:
            print(f"Erreur lors de la récupération des tarifications : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return tarifications


# Rechercher une tarification
def rechercher_tarification(terme_recherche):
    """Recherche une tarification par type de véhicule, km/jour ou prix."""
    connexion = database.connecter()
    colonnes = ["ID", "KM/Jour", "Prix/Locat/Jour", "Type Véhicule"]
    tarifications = []

    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"
            curseur.execute(queries.RECHERCHER_TARIFICATION, (terme, terme, terme))
            resultats = curseur.fetchall()

            for tarif in resultats:
                tarifications.append([
                    tarif.ID_TARIF,
                    tarif.KM_JOUR,
                    tarif.PRIX_LOCAT_JOUR,
                    tarif.TYPE_VEHIC
                ])

        except Exception as erreur:
            print(f"Erreur lors de la recherche d'une tarification : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, tarifications


# Récupérer une tarification par ID
def get_tarif_par_id(id_tarif):
    """Récupère les détails d'une tarification spécifique par son ID sous forme de dictionnaire."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_TARIF_PAR_ID, (id_tarif,))
            row = curseur.fetchone()
            if row:
                colonnes = [desc[0] for desc in curseur.description]
                tarif = dict(zip(colonnes, row))
                return tarif
        except Exception as erreur:
            print(f"Erreur lors de la récupération de la tarification par ID : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

