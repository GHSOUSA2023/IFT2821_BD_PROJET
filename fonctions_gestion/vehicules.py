from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ----------------------------- FONCTIONS POUR VÉHICULES -----------------------------

# Ajouter un véhicule
def ajouter_vehicule(id_marq, id_mod, id_tp_vehic, annee_fab, couleur, immatriculation, status, km, type_carbur, id_age):
    """Ajoute un véhicule à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_VEHICULE,
                (id_marq, id_mod, id_tp_vehic, annee_fab, couleur.upper(), immatriculation.upper(), status, km, type_carbur, id_age)
            )
            connexion.commit()
            print("🚗 Véhicule ajouté avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de l'ajout du véhicule : {erreur}")
            raise erreur  # 🔥 Propaga o erro para a UI capturar
        finally:
            database.fermer_connexion(connexion)


# Modifier un véhicule
def modifier_vehicule(id_vehic, id_marq, id_mod, id_tp_vehic, annee_fab, couleur, immatriculation, status, km, type_carbur, id_age):
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()

            vehicule = get_vehicule_par_id(id_vehic)
            if not vehicule:
                print("❌ Aucun véhicule trouvé avec cet ID.")
                return

            # Mise à jour de FLOTTE
            curseur.execute(
                queriesupdate.MODIFIER_VEHICULE_FLOTTE,
                (
                    id_marq, id_mod, id_tp_vehic,
                    annee_fab, couleur, immatriculation,
                    status, km, type_carbur, id_vehic
                )
            )

            # Mise à jour de DISPO_VEHICULE
            curseur.execute(
                queriesupdate.MODIFIER_DISPO_VEHICULE,
                (id_age, id_vehic)
            )

            connexion.commit()
            print("🚗 Véhicule modifié avec succès !")

        except Exception as erreur:
            print(f"❌ Erreur lors de la modification du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)


# 🔹 Supprimer un véhicule

def supprimer_vehicule(id_vehic):
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queriesdelete.SUPPRIMER_DISPO_VEICHUL, (id_vehic,))
            
            curseur.execute(queriesdelete.SUPPRIMER_VEHICULE, (id_vehic,))
            
            connexion.commit()
            print("Véhicule supprimé avec succès!")
        except Exception as erreur:
            connexion.rollback()
            print(f"Erreur lors de la suppression du véhicule: {erreur}")
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
                    vehicule.MARQUE,
                    vehicule.MODELE,
                    vehicule.TYPE_VEHIC,
                ))

        except Exception as erreur:
            print(f"❌ Erreur lors de la récupération des véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return vehicules


# Lister les véhicules disponibles depuis la vue
def lister_vehicules_disponibles():
    """Retourne la liste des véhicules disponibles depuis la vue."""
    connexion = database.connecter()
    vehicules = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_VEHICULES_DISPONIBLES)
            resultats = curseur.fetchall()

            for vehicule in resultats:
                vehicules.append((
                    vehicule.ID_VEHIC,
                    vehicule.MARQUE,
                    vehicule.MODELE,
                    vehicule.COULEUR,
                    vehicule.TYPE_CARBUR,
                    vehicule.TYPE_VEHIC,
                    vehicule.ANNEE_FAB,
                    vehicule.IMMATRICULATION,
                    vehicule.DISPON_STOCK,
                    vehicule.NOM_AGE                
                ))
        except Exception as erreur:
            print(f"Erreur lors de la récupération des véhicules disponibles : {erreur}")
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
                    vehicule.MARQUE,
                    vehicule.MODELE,
                    vehicule.TYPE_VEHIC,
                ])

        except Exception as erreur:
            print(f"❌ Erreur lors de la recherche de véhicules : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, vehicules

# Récupérer un véhicule par ID
def get_vehicule_par_id(id_vehic):
    """Récupère les informations d'un véhicule spécifique sous forme de dictionnaire."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_VEHICULE_PAR_ID, (id_vehic,))
            row = curseur.fetchone()
            if row:
                colonnes = [desc[0] for desc in curseur.description]
                vehicule = dict(zip(colonnes, row))
                return vehicule
        except Exception as erreur:
            print(f"❌ Erreur lors de la récupération du véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

