import gestion


def menu():
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
    agence = gestion.get_agence_par_id(id_agence)
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


# Lancer le menu
if __name__ == "__main__":
    menu()
