import gestion


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
            print("Fin du programme.")
            break
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
            break
        else:
            print("Option invalide. Essayez à nouveau.")

# ----------------------------- MENU VÉHICULES -----------------------------

def menu_vehicules():
    """Affiche le menu de gestion des véhicules."""
    while True:
        print("\nGESTION DES VÉHICULES")
        print("1 - Ajouter un véhicule")
        print("2 - Modifier un véhicule")
        print("3 - Supprimer un véhicule")
        print("4 - Lister tous les véhicules")
        print("5 - Rechercher un véhicule")
        print("6 - Retour au menu principal")

        choix = input("👉 Choisissez une option : ").strip()

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
            break
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

    gestion.ajouter_agence(nom, adresse, ville, telephone, email)


def modifier_agence():
    """Modifie une agence après sélection de son ID."""
    print("\nModification d'une agence")
    id_agence = input("Entrez l'ID de l'agence à modifier : ")

    # Vérification si l'agence existe
    agence = gestion.get_agence_par_id(id_agence)  # 🔹 CHANGER ICI
    if not agence:
        print("Aucune agence trouvée avec cet ID.")
        return

    print("\nLaissez vide un champ pour conserver l'ancienne valeur.")
    nom = input(f"Nouveau nom ({agence.NOM_AGE}) : ") or agence.NOM_AGE
    adresse = input(f"Nouvelle adresse ({agence.ADRESSE}) : ") or agence.ADRESSE
    ville = input(f"Nouvelle ville ({agence.VILLE}) : ") or agence.VILLE
    telephone = input(f"Nouveau téléphone ({agence.TELEPHONE}) : ") or agence.TELEPHONE
    email = input(f"Nouvel e-mail ({agence.EMAIL}) : ") or agence.EMAIL

    gestion.modifier_agence(
        id_agence, nom.upper(), adresse.upper(), ville.upper(), telephone, email.lower()
    )


def supprimer_agence():
    """Demande l'ID de l'agence à supprimer et exécute la suppression."""
    print("\nSuppression d'une agence")
    id_agence = input("Entrez l'ID de l'agence à supprimer : ").strip()
    gestion.supprimer_agence(id_agence)


def lister_agences():
    gestion.lister_tout_agences()


def rechercher_agence():
    """Demande un terme de recherche et affiche les résultats."""
    terme = input(
        "Entrez le nom, la ville ou l'adresse de l'agence à rechercher : "
    ).strip()
    gestion.rechercher_agence(terme)


# ----------------------------- FONCTIONS POUR EMPLOYÉS -----------------------------

def ajouter_employe():
    """Ajoute un employé après saisie des informations utilisateur."""
    nas = input("Entrez le NAS de l'employé : ")
    nom = input("Entrez le nom : ").upper()
    prenom = input("Entrez le prénom : ").upper()
    salaire = input("Entrez le salaire : ")
    poste = input("Entrez le poste : ").upper()
    id_age = input("Entrez l'ID de l'agence : ")

    gestion.ajouter_employe(nas, nom, prenom, salaire, poste, id_age)

def modifier_employe():
    """Modifie un employé après sélection de son ID."""
    id_emp = input("Entrez l'ID de l'employé à modifier : ")
    gestion.modifier_employe(id_emp)

def supprimer_employe():
    """Supprime un employé après confirmation."""
    id_emp = input("Entrez l'ID de l'employé à supprimer : ").strip()
    gestion.supprimer_employe(id_emp)

def lister_employes():
    """Liste tous les employés enregistrés."""
    gestion.lister_employes()

def rechercher_employe():
    """Recherche un employé par NAS ou Nom."""
    terme = input("Entrez le NAS ou le nom de l'employé : ").strip()
    gestion.rechercher_employe(terme)



# ----------------------------- LANCEMENT DU PROGRAMME -----------------------------
if __name__ == "__main__":
    menu_principal()
