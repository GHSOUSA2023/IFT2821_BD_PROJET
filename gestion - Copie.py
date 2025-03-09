import database
import queries
import queriesinputs
import queriesupdate
import queriesdelete


# ----------------------------- FONCTIONS POUR AGENCES -----------------------------

# Ajouter une agence
def ajouter_agence(nom, adresse, ville, telephone, email):
    """Ajoute une nouvelle agence à la base de données avec les champs en majuscules."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_AGENCE,
                (
                    nom.upper(),
                    adresse.upper(),
                    ville.upper(),
                    telephone,
                    email.lower(),
                ),
            )
            connexion.commit()
            print("Agence ajoutée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de l'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer une agence par ID
def get_agence_par_id(id_agence):
    """Récupère les informations d'une agence spécifique."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_AGENCE_PAR_ID, (id_agence,))
            agence = curseur.fetchone()
            return agence  # 🔹 RETOURNE L'AGENCE ICI
        except Exception as erreur:
            print(f"Erreur lors de la récupération de l'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Modifier une agence
def modifier_agence(id_agence, nom, adresse, ville, telephone, email):
    """Modifie une agence existante avec des valeurs en majuscules."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            # Vérifier si l'agence existe avant modification
            agence = get_agence_par_id(id_agence)  # 🔹 UTILISER LA FONCTION
            if not agence:
                print("Aucune agence trouvée avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de l'agence sélectionnée :")
            print(f"ID : {agence.ID_AGE}")
            print(f"Nom : {agence.NOM_AGE}")
            print(f"Ville : {agence.VILLE}")

            curseur.execute(
                queriesupdate.MODIFIER_AGENCE,
                (
                    nom.upper(),
                    adresse.upper(),
                    ville.upper(),
                    telephone,
                    email.lower(),
                    id_agence,
                ),
            )
            connexion.commit()
            print("Agence modifiée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la modification de l'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer une agence
def supprimer_agence(id_agence):
    """Supprime une agence par son ID après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si l'agence existe avant de la supprimer
            curseur.execute(queries.GET_AGENCE_PAR_ID, (id_agence,))
            agence = curseur.fetchone()

            if not agence:
                print("Aucune agence trouvée avec cet ID.")
                return

            # Afficher les informations avant suppression
            print("\nDétails de l'agence sélectionnée :")
            print(f"ID : {agence.ID_AGE}")
            print(f"Nom : {agence.NOM_AGE}")
            print(f"Ville : {agence.VILLE}")

            # Demander confirmation
            confirmation = (
                input(f"Confirmez-vous la suppression de '{agence.NOM_AGE}' ? (O/N) : ")
                .strip()
                .upper()
            )
            if confirmation != "O":
                print("Suppression annulée.")
                return

            # Supprimer l'agence
            curseur.execute(queriesdelete.SUPPRIMER_AGENCE, (id_agence,))
            connexion.commit()
            print("Agence supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de l'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister toutes les agences
def lister_tout_agences():
    """Récupère et affiche toutes les agences enregistrées."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_AGENCES)
            agences = curseur.fetchall()

            if not agences:
                print("Aucune agence enregistrée.")
                return

            print("\nListe des agences :")
            print(
                f"{'ID':<5} {'Nom':<27} {'Ville':<20} {'Adresse':<30} {'Téléphone':<15} {'Email'}"
            )
            print("-" * 90)

            for agence in agences:
                print(
                    f"{agence.ID_AGE:<5} {agence.NOM_AGE:<27} {agence.VILLE:<20} {agence.ADRESSE:<30} {agence.TELEPHONE:<15} {agence.EMAIL}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la récupération des agences : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Rechercher une agence par nom, ville ou adresse
def rechercher_agence(terme_recherche):
    """Recherche les agences correspondant au terme donné."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"  # Ajoute les wildcards pour la recherche
            curseur.execute(queries.RECHERCHER_AGENCE, (terme, terme, terme))
            agences = curseur.fetchall()

            if not agences:
                print("Aucune agence trouvée.")
                return

            print("\nRésultats de la recherche :")
            print(
                f"{'ID':<5} {'Nom':<20} {'Ville':<15} {'Adresse':<25} {'Téléphone':<15} {'Email'}"
            )
            print("-" * 90)

            for agence in agences:
                print(
                    f"{agence.ID_AGE:<5} {agence.NOM_AGE:<20} {agence.VILLE:<15} {agence.ADRESSE:<25} {agence.TELEPHONE:<15} {agence.EMAIL}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la recherche d'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)

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


# Modifier un employé
def modifier_employe(id_emp, nas, nom, prenom, salaire, poste, id_age):
    """Modifie les informations d'un employé existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesupdate.MODIFIER_EMPLOYE,
                (nas, nom, prenom, salaire, poste, id_age, id_emp),
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
