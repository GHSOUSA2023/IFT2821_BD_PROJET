from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ----------------------------- FONCTIONS POUR VEHICULES-OPTIONNELS -----------------------------


# Ajouter un optionnel
def ajouter_optionnel(nom_optionnel, prix_jour):
    """Ajoute un nouvel optionnel de location."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_OPTIONNEL, (nom_optionnel.upper(), prix_jour)
            )
            connexion.commit()
            print("Optionnel ajouté avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de l'optionnel : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer un optionnel par ID
def get_optionnel_par_id(id_optionnel):
    """Récupère un optionnel par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_OPTIONNEL_PAR_ID, (id_optionnel,))
            return curseur.fetchone()
        except Exception as erreur:
            print(f"Erreur lors de la récupération de l'optionnel : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Modifier un optionnel
def modifier_optionnel(id_optionnel, nouveau_nom, nouveau_prix):
    """Modifie un optionnel existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si l'optionnel existe
            curseur.execute(queries.GET_OPTIONNEL_PAR_ID, (id_optionnel,))
            optionnel = curseur.fetchone()
            if not optionnel:
                print("Aucun optionnel trouvé avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de l'optionnel sélectionné :")
            print(f"ID : {optionnel.ID_OPTIO}")
            print(f"Nom : {optionnel.NOM_OPTIO}")
            print(f"Prix par jour : {optionnel.PRIX_OPTIO_JOUR}")

            # Mise à jour de l'optionnel
            curseur.execute(
                queriesupdate.MODIFIER_OPTIONNEL,
                (nouveau_nom.upper(), nouveau_prix, id_optionnel),
            )
            connexion.commit()
            print("Optionnel modifié avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la modification de l'optionnel : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer un optionnel
def supprimer_optionnel(id_optionnel):
    """Supprime un optionnel après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si l'optionnel existe
            curseur.execute(queries.GET_OPTIONNEL_PAR_ID, (id_optionnel,))
            optionnel = curseur.fetchone()
            if not optionnel:
                print("Aucun optionnel trouvé avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_OPTIONNEL, (id_optionnel,))
            connexion.commit()
            print("Optionnel supprimé avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la suppression de l'optionnel : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister tous les optionnels
def lister_tout_optionnels():
    """Retourne la liste de tous les optionnels enregistrés."""
    connexion = database.connecter()
    optionnels = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_OPTIONNELS)
            resultats = curseur.fetchall()

            for optionnel in resultats:
                optionnels.append((
                    optionnel.ID_OPTIO,
                    optionnel.NOM_OPTIO,
                    optionnel.PRIX_OPTIO_JOUR
                ))

        except Exception as erreur:
            print(f"Erreur lors de la récupération des optionnels : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return optionnels



# Rechercher un optionnel par nom
def rechercher_optionnel(terme):
    """Recherche un optionnel par nom."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.RECHERCHER_OPTIONNELS, (f"%{terme.upper()}%",))
            optionnels = curseur.fetchall()

            if not optionnels:
                print("Aucun optionnel correspondant trouvé.")
                return

            print("\nRésultats de la recherche :")
            for optionnel in optionnels:
                print(
                    f"ID: {optionnel.ID_OPTIO} | Nom: {optionnel.NOM_OPTIO} | Prix/jour: {optionnel.PRIX_OPTIO_JOUR}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la recherche des optionnels : {erreur}")
        finally:
            database.fermer_connexion(connexion)

