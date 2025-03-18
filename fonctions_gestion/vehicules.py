from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ----------------------------- FONCTIONS POUR VÉHICULES -----------------------------

# 🔹 Ajouter un véhicule
def ajouter_vehicule(immatriculation, type_carbur, annee_fab, couleur, status, km, id_marq, id_mod, id_tp_vehic):
    """Ajoute un véhicule à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_VEHICULE,
                (immatriculation, type_carbur, annee_fab, couleur, status, km, id_marq, id_mod, id_tp_vehic),
            )
            connexion.commit()
            print("🚗 Véhicule ajouté avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de l'ajout du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# 🔹 Modifier un véhicule
def modifier_vehicule(id_vehic, immatriculation, type_carbur, annee_fab, couleur, status, km, id_marq, id_mod, id_tp_vehic):
    """Modifie les informations d'un véhicule existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            # Vérifier si le véhicule existe avant modification
            vehicule = get_vehicule_par_id(id_vehic)
            if not vehicule:
                print("❌ Aucun véhicule trouvé avec cet ID.")
                return

            curseur.execute(
                queriesupdate.MODIFIER_VEHICULE,
                (immatriculation, type_carbur, annee_fab, couleur, status, km, id_marq, id_mod, id_tp_vehic, id_vehic),
            )
            connexion.commit()
            print("🚗 Véhicule modifié avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de la modification du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# 🔹 Supprimer un véhicule
def supprimer_vehicule(id_vehic):
    """Supprime un véhicule par son ID après vérification de son existence."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesdelete.SUPPRIMER_VEHICULE, (id_vehic,))
            connexion.commit()
            print("🚗 Véhicule supprimé avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de la suppression du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# 🔹 Lister tous les véhicules
def lister_tous_vehicules():
    """Retourne une liste de tous les véhicules enregistrés avec détails associés."""
    connexion = database.connecter()
    vehicules = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_VEHICULES)
            resultats = curseur.fetchall()

            for vehicule in resultats:
                vehicules.append((
                    vehicule.ID_VEHIC,
                    vehicule.IMMATRICULATION,
                    vehicule.TYPE_CARBUR,
                    vehicule.ANNEE_FAB,
                    vehicule.COULEUR,
                    vehicule.STATUS,
                    vehicule.KM,
                    vehicule.NOM_MARQUE,
                    vehicule.NOM_MODELE,
                    vehicule.TYPE_VEHICULE,
                ))

        except Exception as erreur:
            print(f"❌ Erreur lors de la récupération des véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return vehicules

# 🔹 Rechercher un véhicule par immatriculation ou modèle
def rechercher_vehicule(terme_recherche):
    """Recherche un véhicule par immatriculation ou modèle et retourne les résultats sous forme de tableau."""
    connexion = database.connecter()
    colonnes = ["ID", "Immatriculation", "Carburant", "Année", "Couleur", "Statut", "KM", "Marque", "Modèle", "Type"]
    vehicules = []

    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"
            curseur.execute(queries.RECHERCHER_VEHICULE, (terme, terme))
            resultats = curseur.fetchall()

            for vehicule in resultats:
                vehicules.append([
                    vehicule.ID_VEHIC,
                    vehicule.IMMATRICULATION,
                    vehicule.TYPE_CARBUR,
                    vehicule.ANNEE_FAB,
                    vehicule.COULEUR,
                    vehicule.STATUS,
                    vehicule.KM,
                    vehicule.NOM_MARQUE,
                    vehicule.NOM_MODELE,
                    vehicule.TYPE_VEHICULE
                ])

        except Exception as erreur:
            print(f"❌ Erreur lors de la recherche de véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, vehicules

# 🔹 Récupérer un véhicule par ID
def get_vehicule_par_id(id_vehic):
    """Récupère les informations d'un véhicule spécifique."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_VEHICULE_PAR_ID, (id_vehic,))
            vehicule = curseur.fetchone()
            return vehicule
        except Exception as erreur:
            print(f"❌ Erreur lors de la récupération du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None
