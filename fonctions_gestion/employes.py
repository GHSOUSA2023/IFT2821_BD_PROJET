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
                (nas, 
                nom.upper(), 
                prenom.upper(), 
                salaire, 
                poste, 
                id_age),
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
            return employe  # RETOURNER L'EMPLOYÉ
        except Exception as erreur:
            print(f"Erreur lors de la récupération de l'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Récupérer la liste des employés pour modification
def afficher_liste_employes_modifier():
    """
    Récupère la liste des employés sous forme de tableau de données.
    """
    colonnes = ["ID", "NAS", "Nom", "Prénom", "Salaire", "Poste", "Agence"]
    employes = []

    # Connexion à la base de données
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_EMPLOYES)
            employes_bd = curseur.fetchall()

            # Ajouter les données à la liste
            for employe in employes_bd:
                employes.append([
                    str(employe.ID_EMP),  # ID en chaîne pour PyQt
                    employe.NAS,
                    employe.NOM,
                    employe.PRENOM,
                    str(employe.SALAIRE),  # Convertir salaire en string pour affichage
                    employe.POSTE,
                    employe.ID_AGE
                ])

        except Exception as erreur:
            print(f"Erreur lors de la récupération des employés : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, employes


# Modifier un employé
def modifier_employe(id_emp, nas, nom, prenom, salaire, poste, id_age):
    """Modifie les informations d'un employé existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            # Vérifier si l'employé existe avant modification
            employe = get_employe_par_id(id_emp)
            if not employe:
                print("Aucun employé trouvé avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de l'employé sélectionné :")
            print(f"ID : {employe.ID_EMP}")
            print(f"Nom : {employe.NOM}")
            print(f"Prénom : {employe.PRENOM}")
            print(f"Poste : {employe.POSTE}")

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
def afficher_liste_employes_supprimer():
    """
    Récupère la liste des employés sous forme de tableau de données pour suppression.
    """
    colonnes = ["ID", "NAS", "Nom", "Prénom", "Salaire", "Poste", "ID Agence"]
    employes = []

    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_EMPLOYES)
            employes_bd = curseur.fetchall()

            # Ajouter les employés dans le tableau
            for employe in employes_bd:
                employes.append([
                    str(employe.ID_EMP),  # ID en chaîne pour PyQt
                    employe.NAS,
                    employe.NOM,
                    employe.PRENOM,
                    employe.SALAIRE,
                    employe.POSTE,
                    employe.ID_AGE
                ])

        except Exception as erreur:
            print(f"Erreur lors de la récupération des employés : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, employes


def supprimer_employe(id_emp):
    """Supprime un employé par son ID après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si l'employé existe avant suppression
            curseur.execute(queries.GET_EMPLOYE_PAR_ID, (id_emp,))
            employe = curseur.fetchone()

            if not employe:
                print("Aucun employé trouvé avec cet ID.")
                return

            # Afficher les informations avant suppression (debug)
            print("\nDétails de l'employé sélectionné :")
            print(f"ID : {employe.ID_EMP}")
            print(f"Nom : {employe.NOM}")
            print(f"Prénom : {employe.PRENOM}")

            # Supprimer l'employé
            curseur.execute(queriesdelete.SUPPRIMER_EMPLOYE, (id_emp,))
            connexion.commit()
            print("Employé supprimé avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de l'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister tous les employés
def lister_employes():
    """Retourne une liste de tous les employés avec le NOM de l'agence au lieu de son ID."""
    connexion = database.connecter()
    employes = []

    if connexion:
        try:
            curseur = connexion.cursor()
            # 🔹 Jointure entre employés et agences pour obtenir le NOM au lieu de l'ID
            curseur.execute("""
                SELECT e.ID_EMP, e.NAS, e.NOM, e.PRENOM, e.SALAIRE, e.POSTE, a.NOM_AGE
                FROM EMPLOYES e
                JOIN AGENCES a ON e.ID_AGE = a.ID_AGE
            """)
            resultats = curseur.fetchall()

            for employe in resultats:
                employes.append((
                    employe.ID_EMP,
                    employe.NAS,
                    employe.NOM,
                    employe.PRENOM,
                    employe.SALAIRE,
                    employe.POSTE,
                    employe.NOM_AGE  # 🔹 Afficher le NOM de l'agence au lieu de l'ID
                ))

        except Exception as erreur:
            print(f"Erreur lors de la récupération des employés : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return employes  # 🔹 Retourne la liste mise à jour



# Rechercher un employé par NAS ou Nom
def rechercher_employe(terme_recherche):
    """Recherche un employé par NAS, Nom ou Prénom et retourne les résultats sous forme de tableau."""
    connexion = database.connecter()
    colonnes = ["ID", "NAS", "Nom", "Prénom", "Salaire", "Poste", "Agence"]
    employes = []

    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"  # 🔹 Ajoute les wildcards pour la recherche

            # 🔹 Ajout des marqueurs `?` ou `%s` selon le SGBD utilisé
            requete = """
                SELECT e.ID_EMP, e.NAS, e.NOM, e.PRENOM, e.SALAIRE, e.POSTE, a.NOM_AGE
                FROM EMPLOYES e
                JOIN AGENCES a ON e.ID_AGE = a.ID_AGE
                WHERE e.NAS LIKE ? OR e.NOM LIKE ? OR e.PRENOM LIKE ?
            """

            curseur.execute(requete, (terme, terme, terme))  # 🔹 Ajout correct des paramètres
            resultats = curseur.fetchall()

            for employe in resultats:
                employes.append([
                    employe.ID_EMP,
                    employe.NAS,
                    employe.NOM,
                    employe.PRENOM,
                    employe.SALAIRE,
                    employe.POSTE,
                    employe.NOM_AGE  # 🔹 Affiche bien le NOM de l'agence
                ])

        except Exception as erreur:
            print(f"Erreur lors de la recherche d'employé : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, employes  # 🔹 Retourne une liste même si vide


