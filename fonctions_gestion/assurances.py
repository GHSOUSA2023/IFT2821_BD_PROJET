from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete


# ----------------------------- FONCTIONS POUR VEHICULES-ASSURANCE -----------------------------


# Ajouter une assurance
def ajouter_assurance(type_assurance, prix_jour):
    """Ajoute une nouvelle assurance à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_ASSURANCE, (type_assurance.upper(), prix_jour)
            )
            connexion.commit()
            print("Assurance ajoutée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de l'assurance : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer une assurance par ID
def get_assurance_par_id(id_assurance):
    """Récupère une assurance par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_ASSURANCE_PAR_ID, (id_assurance,))
            return database.fetchone_dict(curseur)
        except Exception as erreur:
            print(f"Erreur lors de la récupération de l'assurance : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None




# Modifier une assurance
def modifier_assurance(id_assurance, type_assurance, prix_jour):
    """Modifie une assurance existante."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si l'assurance existe
            curseur.execute(queries.GET_ASSURANCE_PAR_ID, (id_assurance,))
            assurance = curseur.fetchone()
            if not assurance:
                print("Aucune assurance trouvée avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de l'assurance sélectionnée :")
            print(f"ID : {assurance.ID_ASSURANCE}")
            print(f"Type : {assurance.TYPE_ASSURANCE}")
            print(f"Prix/jour : {assurance.PRIX_JOUR}")

            # Mise à jour de l'assurance
            curseur.execute(
                queriesupdate.MODIFIER_ASSURANCE,
                (type_assurance.upper(), prix_jour, id_assurance),
            )
            connexion.commit()
            print("Assurance modifiée avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la modification de l'assurance : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer une assurance
def supprimer_assurance(id_assurance):
    """Supprime une assurance après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si l'assurance existe
            curseur.execute(queries.GET_ASSURANCE_PAR_ID, (id_assurance,))
            assurance = curseur.fetchone()
            if not assurance:
                print("Aucune assurance trouvée avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_ASSURANCE, (id_assurance,))
            connexion.commit()
            print("Assurance supprimée avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la suppression de l'assurance : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister toutes les assurances
def lister_toutes_assurances():
    """Retourne toutes les assurances enregistrées sous forme de liste."""
    connexion = database.connecter()
    assurances = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_ASSURANCES)
            resultats = curseur.fetchall()

            for assurance in resultats:
                assurances.append((
                    assurance.ID_ASSURANCE,
                    assurance.TYPE_ASSURANCE,
                    assurance.PRIX_JOUR
                ))

        except Exception as erreur:
            print(f"Erreur lors de la récupération des assurances : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return assurances



# Rechercher une assurance par type
def rechercher_assurance(terme):
    """Recherche une assurance par type."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.RECHERCHER_ASSURANCE, (f"%{terme.upper()}%",))
            assurances = curseur.fetchall()

            if not assurances:
                print("Aucune assurance correspondante trouvée.")
                return

            print("\nRésultats de la recherche :")
            for assurance in assurances:
                print(
                    f"ID: {assurance.ID_ASSURANCE} | Type: {assurance.TYPE_ASSURANCE} | Prix/jour: {assurance.PRIX_JOUR}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la recherche des assurances : {erreur}")
        finally:
            database.fermer_connexion(connexion)
