from fonctions_gestion import agences, assurances, employes, flotte


# ----------------------------- MENU PRINCIPAL -----------------------------
def menu_principal():
    """Affiche le menu de gestion des agences."""
    while True:
        print("\nGESTION DES AGENCES")
        print("1 - Gestion des agences")
        print("2 - Gestion des employés")
        print("3 - Gestion des véhicules")
        print("4 - Quitter")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            menu_agences()
        elif choix == "2":
            menu_employes()
        elif choix == "3":
            menu_vehicules()
        elif choix == "4":
            print("Fin du programme.")
            break
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- MENU AGENCES -----------------------------


def menu_agences():
    """Affiche le menu principal."""
    while True:
        print("\nMenu de Gestion des Agences")
        print("1 - Ajouter une agence")
        print("2 - Modifier une agence")
        print("3 - Supprimer une agence")
        print("4 - Lister toutes les agences")
        print("5 - Rechercher une agence")
        print("6 - Quitter")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            ajouter_agence()
        elif choix == "2":
            modifier_agence()
        elif choix == "3":
            supprimer_agence()
        elif choix == "4":
            lister_agences()
        elif choix == "5":
            rechercher_agence()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- MENU EMPLOYES -----------------------------


def menu_employes():
    """Affiche le menu de gestion des employés."""
    while True:
        print("\nGESTION DES EMPLOYÉS")
        print("1 - Ajouter un employé")
        print("2 - Modifier un employé")
        print("3 - Supprimer un employé")
        print("4 - Lister tous les employés")
        print("5 - Rechercher un employé")
        print("6 - Retour au menu principal")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            ajouter_employe()
        elif choix == "2":
            modifier_employe()
        elif choix == "3":
            supprimer_employe()
        elif choix == "4":
            lister_employes()
        elif choix == "5":
            rechercher_employe()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- MENU VÉHICULES -----------------------------


def menu_vehicules():
    """Affiche le menu de gestion des véhicules et de ses sous-catégories."""
    while True:
        print("\nGESTION DES VÉHICULES")
        print("1 - Gérer les marques")
        print("2 - Gérer les modèles")
        print("3 - Gérer les optionnels")
        print("4 - Gérer la maintenance")
        print("5 - Gérer la flotte")
        print("6 - Gérer les assurances")
        print("7 - Retour au menu principal")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            menu_marques()
        elif choix == "2":
            menu_modeles()
        elif choix == "3":
            menu_optionnels()
        elif choix == "4":
            menu_maintenance()
        elif choix == "5":
            menu_flotte()
        elif choix == "6":
            menu_assurances()
        elif choix == "7":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- SUB-MENU VÉHICULES-MARQUES -----------------------------
def menu_marques():
    """Affiche le menu de gestion des marques de véhicules."""
    while True:
        print("\nGESTION DES MARQUES")
        print("1 - Ajouter une marque")
        print("2 - Modifier une marque")
        print("3 - Supprimer une marque")
        print("4 - Lister toutes les marques")
        print("5 - Recherche marques")
        print("6 - Retour au menu véhicules")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            ajouter_marque()
        elif choix == "2":
            modifier_marque()
        elif choix == "3":
            supprimer_marque()
        elif choix == "4":
            lister_marques()
        elif choix == "5":
            rechercher_marque()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- SUB-MENU VÉHICULES-MODELES -----------------------------


def menu_modeles():
    """Affiche le menu de gestion des modèles de véhicules."""
    while True:
        print("\nGESTION DES MODÈLES")
        print("1 - Ajouter un modèle")
        print("2 - Modifier un modèle")
        print("3 - Supprimer un modèle")
        print("4 - Lister tous les modèles")
        print("5 - Rechercher un modèle")
        print("6 - Retour au menu véhicules")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            ajouter_modele()
        elif choix == "2":
            modifier_modele()
        elif choix == "3":
            supprimer_modele()
        elif choix == "4":
            lister_modeles()
        elif choix == "5":
            rechercher_modele()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- SUB-MENU VÉHICULES-OPTIONNELS-----------------------------


def menu_optionnels():
    """Affiche le menu de gestion des optionnels des véhicules."""
    while True:
        print("\nGESTION DES OPTIONNELS")
        print("1 - Ajouter un optionnel")
        print("2 - Modifier un optionnel")
        print("3 - Supprimer un optionnel")
        print("4 - Lister tous les optionnels")
        print("5 - Rechercher un optionnel")
        print("6 - Retour au menu véhicules")

        choix = input("👉 Choisissez une option : ").strip()

        if choix == "1":
            ajouter_optionnel()
        elif choix == "2":
            modifier_optionnel()
        elif choix == "3":
            supprimer_optionnel()
        elif choix == "4":
            lister_optionnels()
        elif choix == "5":
            rechercher_optionnel()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- SUB-MENU VÉHICULES-MAITENANCE-----------------------------


def menu_maintenance():
    """Affiche le menu de gestion de la maintenance des véhicules."""
    while True:
        print("\nGESTION DES MAINTENANCES")
        print("1 - Ajouter une maintenance")
        print("2 - Modifier une maintenance")
        print("3 - Supprimer une maintenance")
        print("4 - Lister toutes les maintenances")
        print("5 - Rechercher une maintenance")
        print("6 - Retour au menu véhicules")

        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            ajouter_maintenance()
        elif choix == "2":
            modifier_maintenance()
        elif choix == "3":
            supprimer_maintenance()
        elif choix == "4":
            lister_maintenances()
        elif choix == "5":
            rechercher_maintenance()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- SUB-MENU VÉHICULES-FLOTTE-----------------------------


def menu_flotte():
    """Affiche le menu de gestion de la flotte de véhicules."""
    while True:
        print("\nGESTION DE LA FLOTTE")
        print("1 - Ajouter un véhicule")
        print("2 - Modifier un véhicule")
        print("3 - Supprimer un véhicule")
        print("4 - Lister tous les véhicules")
        print("5 - Rechercher un véhicule")
        print("6 - Retour au menu véhicules")

        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            ajouter_vehicule()
        elif choix == "2":
            modifier_vehicule()
        elif choix == "3":
            supprimer_vehicule()
        elif choix == "4":
            lister_vehicules()
        elif choix == "5":
            rechercher_vehicule()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- SUB-MENU VÉHICULES-ASSURANCE-----------------------------


def menu_assurances():
    """Affiche le menu de gestion des assurances pour les véhicules."""
    while True:
        print("\nGESTION DES ASSURANCES")
        print("1 - Ajouter une assurance")
        print("2 - Modifier une assurance")
        print("3 - Supprimer une assurance")
        print("4 - Lister toutes les assurances")
        print("5 - Rechercher une assurance")
        print("6 - Retour au menu véhicules")

        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            ajouter_assurance()
        elif choix == "2":
            modifier_assurance()
        elif choix == "3":
            supprimer_assurance()
        elif choix == "4":
            lister_assurances()
        elif choix == "5":
            rechercher_assurance()
        elif choix == "6":
            return
        else:
            print("Option invalide. Essayez à nouveau.")


# ----------------------------- FONCTIONS POUR AGENCES -----------------------------


def ajouter_agence():
    """Ajoute une agence après saisie des informations utilisateur."""
    print("\n Ajout d'une nouvelle agence")
    nom = input("Entrez le nom de l'agence : ").upper()
    adresse = input("Entrez l'adresse : ").upper()
    ville = input("Entrez la ville : ").upper()
    telephone = input("Entrez le numéro de téléphone : ")
    email = input("Entrez l'adresse e-mail : ").lower()

    agences.ajouter_agence(nom, adresse, ville, telephone, email)


def modifier_agence():
    """Modifie une agence après sélection de son ID."""
    print("\nModification d'une agence")
    id_agence = input("Entrez l'ID de l'agence à modifier : ")

    # Vérification si l'agence existe
    agence = agences.get_agence_par_id(id_agence)  # 🔹 CHANGER ICI
    if not agence:
        print("Aucune agence trouvée avec cet ID.")
        return

    print("\nLaissez vide un champ pour conserver l'ancienne valeur.")
    nom = input(f"Nouveau nom ({agence.NOM_AGE}) : ") or agence.NOM_AGE
    adresse = input(f"Nouvelle adresse ({agence.ADRESSE}) : ") or agence.ADRESSE
    ville = input(f"Nouvelle ville ({agence.VILLE}) : ") or agence.VILLE
    telephone = input(f"Nouveau téléphone ({agence.TELEPHONE}) : ") or agence.TELEPHONE
    email = input(f"Nouvel e-mail ({agence.EMAIL}) : ") or agence.EMAIL

    agences.modifier_agence(
        id_agence, nom.upper(), adresse.upper(), ville.upper(), telephone, email.lower()
    )


def supprimer_agence():
    """Demande l'ID de l'agence à supprimer et exécute la suppression."""
    print("\nSuppression d'une agence")
    id_agence = input("Entrez l'ID de l'agence à supprimer : ").strip()
    agences.supprimer_agence(id_agence)


def lister_agences():
    agences.lister_tout_agences()


def rechercher_agence():
    """Demande un terme de recherche et affiche les résultats."""
    terme = input(
        "Entrez le nom, la ville ou l'adresse de l'agence à rechercher : "
    ).strip()
    agences.rechercher_agence(terme)


# ----------------------------- FONCTIONS POUR EMPLOYÉS -----------------------------


def ajouter_employe():
    """Ajoute un employé après saisie des informations utilisateur."""
    nas = input("Entrez le NAS de l'employé : ")
    nom = input("Entrez le nom : ").upper()
    prenom = input("Entrez le prénom : ").upper()
    salaire = input("Entrez le salaire : ")
    poste = input("Entrez le poste : ").upper()
    id_age = input("Entrez l'ID de l'agence : ")

    employes.ajouter_employe(nas, nom, prenom, salaire, poste, id_age)


def modifier_employe():
    """Modifie un employé après sélection de son ID."""
    id_emp = input("Entrez l'ID de l'employé à modifier : ")

    # Vérification si l'employé existe
    employe = employes.get_employe_par_id(id_emp)
    if not employe:
        print("Aucun employé trouvé avec cet ID.")
        return

    print("\nLaissez vide un champ pour conserver l'ancienne valeur.")
    nas = input(f"NAS actuel ({employe.NAS}): ") or employe.NAS
    nom = input(f"Nouveau nom ({employe.NOM}): ") or employe.NOM
    prenom = input(f"Nouveau prénom ({employe.PRENOM}): ") or employe.PRENOM
    salaire = input(f"Salaire actuel ({employe.SALAIRE}): ") or employe.SALAIRE
    poste = input(f"Poste actuel ({employe.POSTE}): ") or employe.POSTE
    id_age = input(f"ID Agence actuelle ({employe.ID_AGE}): ") or employe.ID_AGE

    # ✅ Passer tous les paramètres
    employes.modifier_employe(
        id_emp, nas, nom.upper(), prenom.upper(), float(salaire), poste.upper(), id_age
    )


def supprimer_employe():
    """Supprime un employé après confirmation."""
    id_emp = input("Entrez l'ID de l'employé à supprimer : ").strip()
    employes.supprimer_employe(id_emp)


def lister_employes():
    """Liste tous les employés enregistrés."""
    employes.lister_employes()


def rechercher_employe():
    """Recherche un employé par NAS ou Nom."""
    terme = input("Entrez le NAS ou le nom de l'employé : ").strip()
    employes.rechercher_employe(terme)


# ----------------------------- FONCTIONS POUR VEHICULES-MARQUES -----------------------------


def ajouter_marque():
    """Ajoute une marque après saisie des informations utilisateur."""
    nom = input("Entrez le nom de la marque : ").strip().upper()
    flotte.ajouter_marque(nom)


def modifier_marque():
    """Modifie une marque après sélection de son ID."""
    id_marque = input("Entrez l'ID de la marque à modifier : ").strip()

    # Vérifier si la marque existe
    marque = flotte.get_marque_par_id(id_marque)
    if not marque:
        print("Aucune marque trouvée avec cet ID.")
        return

    # Affichage des informations actuelles de la marque
    print("\nDétails de la marque sélectionnée :")
    print(f"ID : {marque.ID_MARQ}")
    print(f"Nom : {marque.MARQUE}")

    # Demander un nouveau nom, conserver l'ancien si l'utilisateur ne saisit rien
    nouveau_nom = input(f"Nouveau nom ({marque.MARQUE}) : ").strip() or marque.MARQUE

    flotte.modifier_marque(id_marque, nouveau_nom.upper())


def supprimer_marque():
    """Demande l'ID de la marque à supprimer et exécute la suppression."""
    id_marque = input("Entrez l'ID de la marque à supprimer : ").strip()
    flotte.supprimer_marque(id_marque)


def lister_marques():
    """Liste toutes les marques enregistrées."""
    flotte.lister_marques()


def rechercher_marque():
    """Recherche une marque par nom."""
    nom_marque = input("Entrez le nom (ou partie du nom) de la marque : ").strip()
    flotte.rechercher_marque(nom_marque)


# ----------------------------- FONCTIONS POUR VEHICULES-MODELES -----------------------------


def ajouter_modele():
    """Ajoute un modèle après saisie des informations utilisateur."""
    nom_modele = input("Entrez le nom du modèle : ").strip().upper()
    flotte.ajouter_modele(nom_modele)


def modifier_modele():
    """Modifie un modèle après sélection de son ID."""
    id_modele = input("Entrez l'ID du modèle à modifier : ").strip()

    # Vérification si le modèle existe
    modele = flotte.get_modele_par_id(id_modele)
    if not modele:
        print("Aucun modèle trouvé avec cet ID.")
        return

    print("\nDétails du modèle sélectionné :")
    print(f"ID : {modele.ID_MOD}")
    print(f"Nom : {modele.MODELE}")

    nouveau_nom = input(f"Nouveau nom ({modele.MODELE}) : ").strip() or modele.MODELE
    flotte.modifier_modele(id_modele, nouveau_nom.upper())


def supprimer_modele():
    """Demande l'ID du modèle à supprimer et exécute la suppression."""
    id_modele = input("Entrez l'ID du modèle à supprimer : ").strip()
    flotte.supprimer_modele(id_modele)


def lister_modeles():
    flotte.lister_tout_modeles()


def rechercher_modele():
    terme = input("Entrez le nom du modèle à rechercher : ").strip()
    flotte.rechercher_modele(terme)


# ----------------------------- FONCTIONS POUR VEHICULES-OPTIONNELS -----------------------------


def ajouter_optionnel():
    """Ajoute un optionnel après saisie des informations utilisateur."""
    nom_optionnel = input("Entrez le nom de l'optionnel : ").strip().upper()
    prix_jour = float(input("Entrez le prix par jour : ").strip())

    flotte.ajouter_optionnel(nom_optionnel, prix_jour)


def modifier_optionnel():
    """Modifie un optionnel après sélection de son ID."""
    id_optionnel = input("Entrez l'ID de l'optionnel à modifier : ").strip()

    # Vérification si l'optionnel existe
    optionnel = flotte.get_optionnel_par_id(id_optionnel)
    if not optionnel:
        print("Aucun optionnel trouvé avec cet ID.")
        return

    print("\nDétails de l'optionnel sélectionné :")
    print(
        f"ID : {optionnel.ID_OPTIO} | Nom : {optionnel.NOM_OPTIO} | Prix/jour : {optionnel.PRIX_OPTIO_JOUR}"
    )

    nouveau_nom = (
        input(f"Nouveau nom ({optionnel.NOM_OPTIO}) : ").strip() or optionnel.NOM_OPTIO
    )
    nouveau_prix = (
        input(f"Nouveau prix ({optionnel.PRIX_OPTIO_JOUR}) : ").strip()
        or optionnel.PRIX_OPTIO_JOUR
    )

    flotte.modifier_optionnel(id_optionnel, nouveau_nom.upper(), float(nouveau_prix))


def supprimer_optionnel():
    """Supprime un optionnel après confirmation."""
    id_optionnel = input("Entrez l'ID de l'optionnel à supprimer : ").strip()

    # Vérification si l'optionnel existe
    optionnel = flotte.get_optionnel_par_id(id_optionnel)
    if not optionnel:
        print("Aucun optionnel trouvé avec cet ID.")
        return

    confirmation = (
        input(f"Êtes-vous sûr de vouloir supprimer '{optionnel.NOM_OPTIO}' ? (O/N) : ")
        .strip()
        .upper()
    )
    if confirmation == "O":
        flotte.supprimer_optionnel(id_optionnel)
    else:
        print("Annulation de la suppression.")


def lister_optionnels():
    """Liste tous les optionnels enregistrés."""
    flotte.lister_tout_optionnels()


def rechercher_optionnel():
    """Recherche un optionnel par nom."""
    terme = input("Entrez le nom de l'optionnel à rechercher : ").strip()
    flotte.rechercher_optionnel(terme)


# ----------------------------- FONCTIONS POUR VEHICULES-MAINTENANCE -----------------------------


def ajouter_maintenance():
    """Ajoute une maintenance après saisie des informations utilisateur."""
    id_vehic = input("Entrez l'ID du véhicule : ").strip()
    id_emp = input("Entrez l'ID de l'employé responsable : ").strip()
    type_maintenance = (
        input("Type (REVISION, REPARATION, CONTROLE TECHNIQUE) : ").strip().upper()
    )
    date_maintenance = input("Date début (YYYY-MM-DD) : ").strip()
    description = input("Description : ").strip()
    status = input("Statut (EN MAINTENANCE / TERMINEE) : ").strip().upper()

    flotte.ajouter_maintenance(
        id_vehic, id_emp, type_maintenance, date_maintenance, description, status
    )


def modifier_maintenance():
    """Modifie une maintenance après sélection de son ID."""
    id_maintenance = input("Entrez l'ID de la maintenance à modifier : ").strip()

    # Vérification si la maintenance existe
    maintenance = flotte.get_maintenance_par_id(id_maintenance)
    if not maintenance:
        print("Aucune maintenance trouvée avec cet ID.")
        return

    print("\nDétails de la maintenance sélectionnée :")
    print(f"ID : {maintenance.ID_MAINTEN}")
    print(f"Type : {maintenance.TYPE_MAINTEN}")
    # print(f"Date début : {maintenance.DATE_MAINTEN}")
    print(f"Date fin maintenance : {maintenance.DATE_MAINTEN_FIN}")
    print(f"Description : {maintenance.DESC_MAINTEN}")
    print(f"Statut : {maintenance.STATUS_MAINT}")

    type_maintenance = (
        input(f"Nouveau type ({maintenance.TYPE_MAINTEN}) : ").strip()
        or maintenance.TYPE_MAINTEN
    )
    date_fin_maintenance = (
        input(f"Date fin maintenance ({maintenance.DATE_MAINTEN_FIN}) : ").strip()
        or maintenance.DATE_MAINTEN_FIN
    )
    description = (
        input(f"Nouvelle description ({maintenance.DESC_MAINTEN}) : ").strip()
        or maintenance.DESC_MAINTEN
    )
    status = (
        input(f"Nouveau statut ({maintenance.STATUS_MAINT}) : ").strip().upper()
        or maintenance.STATUS_MAINT
    )

    flotte.modifier_maintenance(
        id_maintenance,
        type_maintenance.upper(),
        date_fin_maintenance,
        description,
        status,
    )


def supprimer_maintenance():
    """Demande l'ID de la maintenance à supprimer et exécute la suppression."""
    id_maintenance = input("Entrez l'ID de la maintenance à supprimer : ").strip()
    flotte.supprimer_maintenance(id_maintenance)


def lister_maintenances():
    """Liste toutes les maintenances enregistrées."""
    flotte.lister_maintenances()


def rechercher_maintenance():
    """Recherche une maintenance par type ou ID du véhicule."""
    terme = input("Entrez le type de maintenance ou l'ID du véhicule : ").strip()
    flotte.rechercher_maintenance(terme)


# ----------------------------- FONCTIONS POUR VEHICULES-FLOTTE -----------------------------


def ajouter_vehicule():
    """Ajoute un véhicule après saisie des informations utilisateur."""
    id_marque = input("Entrez l'ID de la marque : ").strip()
    id_modele = input("Entrez l'ID du modèle : ").strip()
    id_type = input("Entrez l'ID du type de véhicule : ").strip()
    annee_fab = input("Entrez l'année de fabrication : ").strip()
    couleur = input("Entrez la couleur : ").strip().upper()
    immatriculation = input("Entrez l'immatriculation : ").strip().upper()
    status = input("Entrez le statut (DISPONIBLE / EN MAINTENANCE) : ").strip().upper()
    km = input("Entrez le kilométrage : ").strip()
    type_carbur = input("Entrez le type de carburant : ").strip().upper()

    flotte.ajouter_vehicule(
        id_marque,
        id_modele,
        id_type,
        annee_fab,
        couleur,
        immatriculation,
        status,
        km,
        type_carbur,
    )


def modifier_vehicule():
    """Modifie un véhicule après sélection de son ID."""
    id_vehicule = input("Entrez l'ID du véhicule à modifier : ").strip()

    # Vérification si le véhicule existe
    vehicule = flotte.get_vehicule_par_id(id_vehicule)
    if not vehicule:
        print("Aucun véhicule trouvé avec cet ID.")
        return

    # Affichage des informations avant modification
    print("\nDétails du véhicule sélectionné :")
    print(f"ID : {vehicule[0]}")  # ID_VEHIC
    print(f"Type de carburant : {vehicule[1]}")  # TYPE_CARBUR
    print(f"Année de fabrication : {vehicule[2]}")  # ANNEE_FAB
    print(f"Couleur : {vehicule[3]}")  # COULEUR
    print(f"Immatriculation : {vehicule[4]}")  # IMMATRICULATION
    print(f"Statut : {vehicule[5]}")  # STATUS
    print(f"Kilométrage : {vehicule[6]}")  # KM
    print(f"Marque (ID) : {vehicule[7]}")  # ID_MARQ
    print(f"Modèle (ID) : {vehicule[8]}")  # ID_MOD
    print(f"Type de véhicule (ID) : {vehicule[9]}")  # ID_TP_VEHIC

    # Demander les nouvelles valeurs, conserver les anciennes si vide
    type_carbur = (
        input(f"Nouveau type de carburant ({vehicule[1]}) : ").strip().upper()
        or vehicule[1]
    )
    annee_fab = (
        input(f"Nouvelle année de fabrication ({vehicule[2]}) : ").strip()
        or vehicule[2]
    )
    couleur = (
        input(f"Nouvelle couleur ({vehicule[3]}) : ").strip().upper() or vehicule[3]
    )
    immatriculation = (
        input(f"Nouvelle immatriculation ({vehicule[4]}) : ").strip().upper()
        or vehicule[4]
    )
    status = input(f"Nouveau statut ({vehicule[5]}) : ").strip().upper() or vehicule[5]
    km = input(f"Kilométrage actuel ({vehicule[6]}) : ").strip() or vehicule[6]
    id_marque = (
        input(f"Nouvelle marque (ID actuel: {vehicule[7]}) : ").strip() or vehicule[7]
    )
    id_modele = (
        input(f"Nouveau modèle (ID actuel: {vehicule[8]}) : ").strip() or vehicule[8]
    )
    id_type = (
        input(f"Nouveau type de véhicule (ID actuel: {vehicule[9]}) : ").strip()
        or vehicule[9]
    )

    flotte.modifier_vehicule(
        id_vehicule,
        type_carbur,
        annee_fab,
        couleur,
        immatriculation,
        status,
        km,
        id_marque,
        id_modele,
        id_type,
    )


def supprimer_vehicule():
    """Demande l'ID du véhicule à supprimer et exécute la suppression."""
    id_vehicule = input("Entrez l'ID du véhicule à supprimer : ").strip()
    flotte.supprimer_vehicule(id_vehicule)


def lister_vehicules():
    """Liste tous les véhicules enregistrés."""
    flotte.lister_tous_vehicules()


def rechercher_vehicule():
    """Recherche un véhicule par immatriculation ou modèle."""
    terme = input("Entrez l'immatriculation ou le modèle du véhicule : ").strip()
    flotte.rechercher_vehicule(terme)


# ----------------------------- FONCTIONS POUR VEHICULES-ASSURANCE -----------------------------


def ajouter_assurance():
    """Ajoute une assurance après saisie des informations utilisateur."""
    type_assurance = input("Entrez le type d'assurance : ").strip().upper()
    prix_jour = input("Entrez le prix par jour : ").strip()

    assurances.ajouter_assurance(type_assurance, prix_jour)


def modifier_assurance():
    """Modifie une assurance après sélection de son ID."""
    id_assurance = input("Entrez l'ID de l'assurance à modifier : ").strip()

    # Vérification si l'assurance existe
    assurance = assurances.get_assurance_par_id(id_assurance)
    if not assurance:
        print("Aucune assurance trouvée avec cet ID.")
        return

    # Affichage des informations avant modification
    print("\nDétails de l'assurance sélectionnée :")
    print(f"ID : {assurance[0]}")  # ID_ASSURANCE
    print(f"Type : {assurance[1]}")  # TYPE_ASSURANCE
    print(f"Prix par jour : {assurance[2]}")  # PRIX_JOUR

    # Demander les nouvelles valeurs, conserver les anciennes si vide
    type_assurance = (
        input(f"Nouveau type ({assurance[1]}) : ").strip().upper() or assurance[1]
    )
    prix_jour = input(f"Nouveau prix/jour ({assurance[2]}) : ").strip() or assurance[2]

    assurances.modifier_assurance(id_assurance, type_assurance, prix_jour)


def supprimer_assurance():
    """Supprime une assurance après confirmation."""
    id_assurance = input("Entrez l'ID de l'assurance à supprimer : ").strip()
    assurances.supprimer_assurance(id_assurance)


def lister_assurances():
    """Liste toutes les assurances enregistrées."""
    assurances.lister_toutes_assurances()


def rechercher_assurance():
    """Recherche une assurance par type."""
    terme = input("Entrez le type d'assurance à rechercher : ").strip()
    assurances.rechercher_assurance(terme)


# ----------------------------- LANCEMENT DU PROGRAMME -----------------------------
if __name__ == "__main__":
    menu_principal()
