from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ----------------------------- FONCTIONS POUR EMPLOYÉS -----------------------------


# Ajouter un employé
def ajouter_employe(nas, nom, prenom, salaire, poste, id_age):
    """Ajoute un employé à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_EMPLOYE,
                (nas, nom, prenom, salaire, poste, id_age),
            )
            connexion.commit()
            print("Employé ajouté avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de l'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer un employé par ID
def get_employe_par_id(id_emp):
    """Récupère les informations d'un employé spécifique."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_EMPLOYE_PAR_ID, (id_emp,))
            employe = curseur.fetchone()
            return employe  # ✅ RETOURNER L'EMPLOYÉ
        except Exception as erreur:
            print(f"Erreur lors de la récupération de l'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Modifier un employé
def modifier_employe(id_emp, nas, nom, prenom, salaire, poste, id_age):
    """Modifie les informations d'un employé existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            employe = get_employe_par_id(id_emp)
            if not employe:
                print("Aucun employé trouvé avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de l'employé sélectionné :")
            print(f"ID : {employe.ID_EMP}")
            print(f"Nom : {employe.NOM}")
            print(f"ID AGENCE : {employe.ID_AGE}")

            curseur.execute(
                queriesupdate.MODIFIER_EMPLOYE,
                (
                    nas,
                    nom.upper(),
                    prenom.upper(),
                    salaire,
                    poste.upper(),
                    id_age,
                    id_emp,
                ),
            )
            connexion.commit()
            print("Employé modifié avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la modification de l'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer un employé
def supprimer_employe(id_emp):
    """Supprime un employé par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesdelete.SUPPRIMER_EMPLOYE, (id_emp,))
            connexion.commit()
            print("Employé supprimé avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de l'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister tous les employés
def lister_employes():
    """Retourne la liste de tous les employés enregistrés."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_EMPLOYES)
            employes = curseur.fetchall()

            if not employes:
                print("Aucun employé enregistré.")
                return

            print("\nListe des employés :")
            print(
                f"{'ID':<5} {'NAS':<15} {'Nom':<15} {'Prénom':<15} {'Salaire':<10} {'Poste':<20} {'ID Agence'}"
            )
            print("-" * 90)

            for employe in employes:
                print(
                    f"{employe.ID_EMP:<5} {employe.NAS:<15} {employe.NOM:<15} {employe.PRENOM:<15} {employe.SALAIRE:<10} {employe.POSTE:<20} {employe.ID_AGE}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la récupération des employés : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Rechercher un employé par NAS ou Nom
def rechercher_employe(terme_recherche):
    """Recherche un employé par NAS ou Nom."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"
            curseur.execute(queries.RECHERCHER_EMPLOYE, (terme, terme))
            employes = curseur.fetchall()

            if not employes:
                print("Aucun employé trouvé.")
                return

            print("\nRésultats de la recherche :")
            print(
                f"{'ID':<5} {'NAS':<15} {'Nom':<15} {'Prénom':<15} {'Salaire':<10} {'Poste':<20} {'ID Agence'}"
            )
            print("-" * 90)

            for employe in employes:
                print(
                    f"{employe.ID_EMP:<5} {employe.NAS:<15} {employe.NOM:<15} {employe.PRENOM:<15} {employe.SALAIRE:<10} {employe.POSTE:<20} {employe.ID_AGE}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la recherche d'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)