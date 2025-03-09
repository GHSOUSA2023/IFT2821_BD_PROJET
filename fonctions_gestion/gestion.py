from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

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


# ----------------------------- FONCTIONS POUR VEHICULES-MARQUES -----------------------------


# Ajouter une marque
def ajouter_marque(nom_marque):
    """Ajoute une nouvelle marque à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesinputs.AJOUTER_MARQUE, (nom_marque.upper(),))
            connexion.commit()
            print("Marque ajoutée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de la marque : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer une marque par ID
def get_marque_par_id(id_marque):
    """Récupère une marque par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_MARQUE_PAR_ID, (id_marque,))
            return curseur.fetchone()
        except Exception as erreur:
            print(f"Erreur lors de la récupération de la marque : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Modifier une marque
def modifier_marque(id_marque, nouveau_nom):
    """Modifie le nom d'une marque existante."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si la marque existe
            curseur.execute(queries.GET_MARQUE_PAR_ID, (id_marque,))
            marque = curseur.fetchone()
            if not marque:
                print("Aucune marque trouvée avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de la marque sélectionnée :")
            print(f"ID : {marque.ID_MARQ}")
            print(f"Nom : {marque.MARQUE}")

            # Mise à jour de la marque
            curseur.execute(
                queriesupdate.MODIFIER_MARQUE,
                (nouveau_nom.upper(), id_marque),
            )
            connexion.commit()
            print("Marque modifiée avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la modification de la marque : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer une marque
def supprimer_marque(id_marque):
    """Supprime une marque par son ID après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si la marque existe avant suppression
            curseur.execute(queries.GET_MARQUE_PAR_ID, (id_marque,))
            marque = curseur.fetchone()
            if not marque:
                print("Aucune marque trouvée avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_MARQUE, (id_marque,))
            connexion.commit()
            print("Marque supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de la marque : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister toutes les marques
def lister_marques():
    """Affiche la liste de toutes les marques enregistrées."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_MARQUES)
            marques = curseur.fetchall()

            if not marques:
                print("Aucune marque enregistrée.")
                return

            print("\nLISTE DES MARQUES :")
            for marque in marques:
                print(f"ID: {marque.ID_MARQ} - Nom: {marque.MARQUE}")

        except Exception as erreur:
            print(f"Erreur lors de la récupération des marques : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Rechercher une marque par nom
def rechercher_marque(nom_marque):
    """Recherche une marque par son nom (partiel ou complet)."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.RECHERCHER_MARQUE, (f"%{nom_marque.upper()}%",))
            marques = curseur.fetchall()

            if not marques:
                print("Aucune marque trouvée.")
                return

            print("\nMARQUES TROUVÉES :")
            for marque in marques:
                print(f"ID: {marque.ID_MARQ} - Nom: {marque.MARQUE}")

        except Exception as erreur:
            print(f"Erreur lors de la recherche de la marque : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# ----------------------------- FONCTIONS POUR VEHICULES-MODELES -----------------------------


# Ajouter un modèle
def ajouter_modele(nom_modele):
    """Ajoute un nouveau modèle de véhicule."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesinputs.AJOUTER_MODELE, (nom_modele.upper(),))
            connexion.commit()
            print("Modèle ajouté avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout du modèle : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer un modèle par ID
def get_modele_par_id(id_modele):
    """Récupère un modèle par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_MODELE_PAR_ID, (id_modele,))
            return curseur.fetchone()
        except Exception as erreur:
            print(f"Erreur lors de la récupération du modèle : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Modifier un modèle
def modifier_modele(id_modele, nouveau_nom):
    """Modifie un modèle existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si le modèle existe
            curseur.execute(queries.GET_MODELE_PAR_ID, (id_modele,))
            modele = curseur.fetchone()
            if not modele:
                print("Aucun modèle trouvé avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails du modèle sélectionné :")
            print(f"ID : {modele.ID_MOD}")
            print(f"Nom : {modele.MODELE}")

            # Mise à jour du modèle
            curseur.execute(
                queriesupdate.MODIFIER_MODELE,
                (nouveau_nom.upper(), id_modele),
            )
            connexion.commit()
            print("Modèle modifié avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la modification du modèle : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer un modèle
def supprimer_modele(id_modele):
    """Supprime un modèle après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si le modèle existe
            curseur.execute(queries.GET_MODELE_PAR_ID, (id_modele,))
            modele = curseur.fetchone()
            if not modele:
                print("Aucun modèle trouvé avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_MODELE, (id_modele,))
            connexion.commit()
            print("Modèle supprimé avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la suppression du modèle : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister tous les modèles
def lister_tout_modeles():
    """Affiche tous les modèles enregistrés."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_TOUT_MODELES)
            modeles = curseur.fetchall()

            if not modeles:
                print("Aucun modèle trouvé.")
                return

            print("\nListe des modèles enregistrés :")
            for modele in modeles:
                print(f"ID: {modele.ID_MOD} | Nom: {modele.MODELE}")

        except Exception as erreur:
            print(f"Erreur lors de la récupération des modèles : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Rechercher un modèle par nom
def rechercher_modele(terme):
    """Recherche un modèle par nom."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.RECHERCHER_MODELES, (f"%{terme.upper()}%",))
            modeles = curseur.fetchall()

            if not modeles:
                print("Aucun modèle correspondant trouvé.")
                return

            print("\nRésultats de la recherche :")
            for modele in modeles:
                print(f"ID: {modele.ID_MOD} | Nom: {modele.MODELE}")

        except Exception as erreur:
            print(f"Erreur lors de la recherche de modèles : {erreur}")
        finally:
            database.fermer_connexion(connexion)


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
    """Affiche tous les optionnels enregistrés."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_OPTIONNELS)
            optionnels = curseur.fetchall()

            if not optionnels:
                print("Aucun optionnel trouvé.")
                return

            print("\nListe des optionnels enregistrés :")
            for optionnel in optionnels:
                print(
                    f"ID: {optionnel.ID_OPTIO} | Nom: {optionnel.NOM_OPTIO} | Prix/jour: {optionnel.PRIX_OPTIO_JOUR}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la récupération des optionnels : {erreur}")
        finally:
            database.fermer_connexion(connexion)


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


# ----------------------------- FONCTIONS POUR VEHICULES-MAINTENANCE -----------------------------

# Ajouter une maintenance
def ajouter_maintenance(id_vehic, id_emp, type_maintenance, date_maintenance, description, status):
    """Ajoute une nouvelle maintenance à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_MAINTENANCE,
                (
                    id_vehic,
                    id_emp,
                    type_maintenance.upper(),
                    date_maintenance,
                    description,
                    status.upper(),
                ),
            )
            connexion.commit()
            print("Maintenance ajoutée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de la maintenance : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Récupérer une maintenance par ID
def get_maintenance_par_id(id_maintenance):
    """Récupère une maintenance par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_MAINTENANCE_PAR_ID, (id_maintenance,))
            return curseur.fetchone()
        except Exception as erreur:
            print(f"Erreur lors de la récupération de la maintenance : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None


# Modifier une maintenance
def modifier_maintenance(id_maintenance, type_maintenance, date_fin_maintenance, description, status):
    """Modifie une maintenance existante."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si la maintenance existe
            maintenance = get_maintenance_par_id(id_maintenance)
            if not maintenance:
                print("Aucune maintenance trouvée avec cet ID.")
                return

            # Afficher les informations avant changement
            print("\nDétails de la maintenance sélectionnée :")
            print(f"ID : {maintenance.ID_MAINTEN}")
            print(f"Type : {maintenance.TYPE_MAINTEN}")
            print(f"Date fin maintenance : {maintenance.DATE_MAINTEN_FIN}")
            print(f"Description : {maintenance.DESC_MAINTEN}")
            print(f"Statut : {maintenance.STATUS_MAINT}")


            curseur.execute(
                queriesupdate.MODIFIER_MAINTENANCE,
                (
                    type_maintenance.upper(),
                    date_fin_maintenance,
                    description,
                    status.upper(),
                    id_maintenance,
                ),
            )
            connexion.commit()
            print("Maintenance modifiée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la modification de la maintenance : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer une maintenance
def supprimer_maintenance(id_maintenance):
    """Supprime une maintenance après confirmation."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si la maintenance existe
            maintenance = get_maintenance_par_id(id_maintenance)
            if not maintenance:
                print("Aucune maintenance trouvée avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_MAINTENANCE, (id_maintenance,))
            connexion.commit()
            print("Maintenance supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de la maintenance : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Lister toutes les maintenances
def lister_maintenances():
    """Affiche la liste de toutes les maintenances."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_MAINTENANCES)
            maintenances = curseur.fetchall()

            if not maintenances:
                print("Aucune maintenance enregistrée.")
                return

            print("\nListe des maintenances :")
            for maintenance in maintenances:
                print(
                    f"ID : {maintenance.ID_MAINTEN} | Type : {maintenance.TYPE_MAINTEN} | Véhicule : {maintenance.ID_VEHIC} | Statut : {maintenance.STATUS_MAINT} | Date Debut : {maintenance.DATE_MAINTEN} | Date Fin : {maintenance.DATE_MAINTEN_FIN}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la récupération des maintenances : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Rechercher une maintenance
def rechercher_maintenance(terme):
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Se for dígito, vamos buscar por ID_VEHIC
            if terme.isdigit():
                # "param_type" recebe algo que NUNCA vai bater com TYPE_MAINTEN:
                param_type = "#no_match#"    # <--- NÃO mais '%'
                param_check = terme         # "10"
                param_id = int(terme)       # 10
            else:
                # Se NÃO for dígito, vamos buscar por TYPE_MAINTEN
                param_type = f"%{terme}%"   # ex: "%REPARATION%"
                param_check = "#no_num#"    # algo que não passa em ISNUMERIC
                param_id = -1

            # Executar a query
            curseur.execute(
                queries.RECHERCHER_MAINTENANCE, 
                (param_type, param_check, param_id)
            )
            maintenances = curseur.fetchall()

            if not maintenances:
                print("Aucune maintenance trouvée.")
                return

            print("\nRésultats de la recherche :")
            for maintenance in maintenances:
                print(
                    f"ID : {maintenance.ID_MAINTEN} | "
                    f"Type : {maintenance.TYPE_MAINTEN} | "
                    f"Véhicule : {maintenance.ID_VEHIC} | "
                    f"Statut : {maintenance.STATUS_MAINT}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la recherche de la maintenance : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# ----------------------------- FONCTIONS POUR VEHICULES-FLOTTE -----------------------------

# Ajouter un véhicule dans la flotte
def ajouter_vehicule(id_marque, id_modele, id_type, annee_fab, couleur, immatriculation, status, km, type_carbur):
    """Ajoute un nouveau véhicule dans la flotte."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_VEHICULE,
                (id_marque, id_modele, id_type, annee_fab, couleur.upper(), immatriculation.upper(), status.upper(), km, type_carbur.upper()),
            )
            connexion.commit()
            print("Véhicule ajouté avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de l'ajout du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Récupérer un véhicule par ID
def get_vehicule_par_id(id_vehicule):
    """Récupère un véhicule par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_VEHICULE_PAR_ID, (id_vehicule,))
            return curseur.fetchone()
        except Exception as erreur:
            print(f"Erreur lors de la récupération du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

# Modifier un véhicule
def modifier_vehicule(id_vehicule, type_carbur, annee_fab, couleur, immatriculation, status, km, id_marque, id_modele, id_type):
    """Modifie un véhicule existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si le véhicule existe
            curseur.execute(queries.GET_VEHICULE_PAR_ID, (id_vehicule,))
            vehicule = curseur.fetchone()
            if not vehicule:
                print("Aucun véhicule trouvé avec cet ID.")
                return

            # Affichage des informations avant modification
            print("\nDétails du véhicule sélectionné :")
            print(f"ID : {vehicule[0]}")
            print(f"Type de carburant : {vehicule[1]}")
            print(f"Année de fabrication : {vehicule[2]}")
            print(f"Couleur : {vehicule[3]}")
            print(f"Immatriculation : {vehicule[4]}")
            print(f"Statut : {vehicule[5]}")
            print(f"Kilométrage : {vehicule[6]}")
            print(f"Marque (ID) : {vehicule[7]}")
            print(f"Modèle (ID) : {vehicule[8]}")
            print(f"Type de véhicule (ID) : {vehicule[9]}")

            # Mise à jour du véhicule
            curseur.execute(
                queriesupdate.MODIFIER_VEHICULE,
                (
                    type_carbur.upper(),
                    id_marque, 
                    id_modele, 
                    id_type, 
                    annee_fab, 
                    couleur.upper(), 
                    immatriculation.upper(), 
                    status.upper(), 
                    km, 
                    id_vehicule,
                ),
            )
            connexion.commit()
            print("Véhicule modifié avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la modification du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# Supprimer un véhicule
def supprimer_vehicule(id_vehicule):
    """Supprime un véhicule après confirmation."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Vérifier si le véhicule existe
            curseur.execute(queries.GET_VEHICULE_PAR_ID, (id_vehicule,))
            vehicule = curseur.fetchone()
            if not vehicule:
                print("Aucun véhicule trouvé avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_VEHICULE, (id_vehicule,))
            connexion.commit()
            print("Véhicule supprimé avec succès !")

        except Exception as erreur:
            print(f"Erreur lors de la suppression du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Lister tous les véhicules de la flotte
def lister_tous_vehicules():
    """Affiche tous les véhicules enregistrés dans la flotte."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_VEHICULES)
            vehicules = curseur.fetchall()

            if not vehicules:
                print("Aucun véhicule trouvé dans la flotte.")
                return

            print("\nListe des véhicules enregistrés :")
            for vehicule in vehicules:
                print(f"ID: {vehicule.ID_VEHIC} | Marque: {vehicule.MARQUE} | Modèle: {vehicule.MODELE} | Type: {vehicule.TYPE_VEHIC} | Immatriculation: {vehicule.IMMATRICULATION} | Statut: {vehicule.STATUS} | KM: {vehicule.KM}")

        except Exception as erreur:
            print(f"Erreur lors de la récupération des véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Rechercher un véhicule par immatriculation ou modèle
def rechercher_vehicule(terme):
    """Recherche un véhicule par immatriculation ou modèle."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.RECHERCHER_VEHICULE, (f"%{terme.upper()}%", f"%{terme.upper()}%"))
            vehicules = curseur.fetchall()

            if not vehicules:
                print("Aucun véhicule correspondant trouvé.")
                return

            print("\nRésultats de la recherche :")
            for vehicule in vehicules:
                print(f"ID: {vehicule.ID_VEHIC} | Marque: {vehicule.MARQUE} | Modèle: {vehicule.MODELE} | Type: {vehicule.TYPE_VEHIC} | Immatriculation: {vehicule.IMMATRICULATION} | Statut: {vehicule.STATUS} | KM: {vehicule.KM}")

        except Exception as erreur:
            print(f"Erreur lors de la recherche des véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)

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
            return curseur.fetchone()
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
    """Affiche toutes les assurances enregistrées."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_ASSURANCES)
            assurances = curseur.fetchall()

            if not assurances:
                print("Aucune assurance trouvée.")
                return

            print("\nListe des assurances enregistrées :")
            for assurance in assurances:
                print(
                    f"ID: {assurance.ID_ASSURANCE} | Type: {assurance.TYPE_ASSURANCE} | Prix/jour: {assurance.PRIX_JOUR}"
                )

        except Exception as erreur:
            print(f"Erreur lors de la récupération des assurances : {erreur}")
        finally:
            database.fermer_connexion(connexion)


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
