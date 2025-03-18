from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete
import io
import sys



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

# Modifier une agence lister touts

def afficher_liste_agences_modifier():
    """
    Récupère la liste des agences sous forme de tableau de données.
    """
    colonnes = ["ID", "Nom", "Ville", "Adresse", "Téléphone", "Email"]
    agences = []

    # Connexion à la base de données
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_AGENCES)
            agences_bd = curseur.fetchall()

            # Ajouter les données à la liste
            for agence in agences_bd:
                agences.append([
                    str(agence.ID_AGE),  # ID doit être une chaîne pour PyQt
                    agence.NOM_AGE,
                    agence.VILLE,
                    agence.ADRESSE,
                    agence.TELEPHONE,
                    agence.EMAIL
                ])

        except Exception as erreur:
            print(f"Erreur lors de la récupération des agences : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, agences



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


def afficher_liste_agences_supprimer():
    """
    Récupère la liste des agences sous forme de tableau de données pour suppression.
    """
    colonnes = ["ID", "Nom", "Ville", "Adresse", "Téléphone", "Email"]
    agences = lister_tout_agences()

    return colonnes, agences


def confirmer_suppression(self, row, column):
    """
    Demande confirmation avant suppression d'une agence.
    """
    from PyQt5.QtWidgets import QMessageBox

    id_agence = self.tableau_agences_supprimer.table_widget.item(row, 0).text()  # ID de l'agence
    nom_agence = self.tableau_agences_supprimer.table_widget.item(row, 1).text()  # Nom de l'agence

    # Boîte de confirmation
    reponse = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment supprimer l'agence '{nom_agence}' ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reponse == QMessageBox.Yes:
        supprimer_agence(id_agence)  # Appeler la fonction de suppression
        QMessageBox.information(self, "Succès", "L'agence a été supprimée avec succès.")
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_agences)  # Retour


# Supprimer une agence
def supprimer_agence(id_agence):
    """Supprime une agence par son ID après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            # Verificar se a agencia existe
            curseur.execute(queries.GET_AGENCE_PAR_ID, (id_agence,))
            agence = curseur.fetchone()

            if not agence:
                print("Aucune agence trouvée avec cet ID.")
                return

            # Apenas imprime no console como debug:
            print("\nDétails de l'agence sélectionnée :")
            print(f"ID : {agence.ID_AGE}")
            print(f"Nom : {agence.NOM_AGE}")
            print(f"Ville : {agence.VILLE}")

            # Remove a chamada de input(...) – usamos a confirmação da UI
            # if confirmation != "O": ... etc

            # Executa a remoção
            curseur.execute(queriesdelete.SUPPRIMER_AGENCE, (id_agence,))
            connexion.commit()
            print("Agence supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de l'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)



# Lister toutes les agences
def lister_tout_agences(direct=True):
    """Récupère toutes les agences et les retourne sous forme de liste de tuples."""
    connexion = database.connecter()
    agences = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_AGENCES)
            resultats = curseur.fetchall()

            if direct:
                for agence in resultats:
                    agences.append((
                        agence.ID_AGE,   # ID
                        agence.NOM_AGE,  # Nom
                        agence.VILLE,    # Ville
                        agence.ADRESSE,  # Adresse
                        agence.TELEPHONE, # Téléphone
                        agence.EMAIL     # Email
                    ))
                return agences

        except Exception as erreur:
            print(f"Erreur lors de la récupération des agences : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return []



# Rechercher une agence par nom, ville ou adresse
def rechercher_agence(terme_recherche):
    """
    Recherche les agences correspondant au terme donné et retourne les résultats sous forme de tableau.
    """
    connexion = database.connecter()
    colonnes = ["ID", "Nom", "Ville", "Adresse", "Téléphone", "Email"]
    agences = []

    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"  # Ajoute les wildcards pour la recherche
            curseur.execute(queries.RECHERCHER_AGENCE, (terme, terme, terme))
            resultats = curseur.fetchall()

            for agence in resultats:
                agences.append((
                    agence.ID_AGE,
                    agence.NOM_AGE,
                    agence.VILLE,
                    agence.ADRESSE,
                    agence.TELEPHONE,
                    agence.EMAIL
                ))

        except Exception as erreur:
            print(f"Erreur lors de la recherche d'agence : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, agences
