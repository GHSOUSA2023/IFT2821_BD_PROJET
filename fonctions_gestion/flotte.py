from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

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
            curseur.execute(queriesupdate.MODIFIER_MARQUE, (nouveau_nom.upper(), id_marque))
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
            curseur.execute(queriesdelete.SUPPRIMER_MARQUE, (id_marque,))
            connexion.commit()
            print("Marque supprimée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression de la marque : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Lister toutes les marques
def lister_marques():
    """Retourne la liste de toutes les marques enregistrées."""
    connexion = database.connecter()
    if connexion:
        curseur = connexion.cursor()
        curseur.execute(queries.LISTER_MARQUES)
        marques = curseur.fetchall()
        database.fermer_connexion(connexion)
        return marques
    return []

# Rechercher une marque par nom
def rechercher_marque(nom_marque):
    """Recherche une marque par son nom (partiel ou complet)."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.RECHERCHER_MARQUE, (f"%{nom_marque.upper()}%",))
            marques = curseur.fetchall()
            return marques
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
            curseur.execute(queriesupdate.MODIFIER_MODELE, (nouveau_nom.upper(), id_modele))
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
            curseur.execute(queriesdelete.SUPPRIMER_MODELE, (id_modele,))
            connexion.commit()
            print("Modèle supprimé avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la suppression du modèle : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Lister tous les modèles
def lister_tout_modeles():
    """Retourne tous les modèles enregistrés."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_TOUT_MODELES)
            return curseur.fetchall()
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
            return curseur.fetchall()
        except Exception as erreur:
            print(f"Erreur lors de la recherche de modèles : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# ----------------------------- FONCTIONS POUR VEHICULES-TYPE-VEHICULE -----------------------------

def get_tp_vehic_par_id(id_tp_vehic):
    """Récupère un type de véhicule par ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_TYPE_VEHIC_PAR_ID, (id_tp_vehic,))
            return curseur.fetchone()
        except Exception as erreur:
            print(f"Erreur lors de la récupération du type de véhicule : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

def lister_tout_tp_vehic():
    """Retourne tous les types de véhicules."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_TOUT_TYPE_VEHIC)
            return curseur.fetchall()
        finally:
            database.fermer_connexion(connexion)

# ----------------------------- FONCTIONS POUR MAINTENANCE -----------------------------

def ajouter_maintenance(id_vehic, id_emp, type_maintenance, date_maintenance, description, status):
    """Ajoute une nouvelle maintenance à la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_MAINTENANCE,
                (id_vehic, id_emp, type_maintenance.upper(), date_maintenance, description, status.upper())
            )
            connexion.commit()
            print("Maintenance ajoutée avec succès !")
            return True
        except Exception as erreur:
            print(f"Erreur lors de l'ajout de la maintenance : {erreur}")
            return False
        finally:
            database.fermer_connexion(connexion)
    return False


def terminer_maintenance(id_vehicule, date_fin_maintenance, description):
    """Termine une maintenance pour un véhicule donné."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesupdate.TERMINER_MAINTENANCE,
                (date_fin_maintenance, description, id_vehicule)
            )
            connexion.commit()
            print("Maintenance terminée avec succès !")
        except Exception as erreur:
            print(f"Erreur lors de la terminaison de la maintenance : {erreur}")
        finally:
            database.fermer_connexion(connexion)

def get_infos_maint_vehicule_par_id(id_vehicule):
    """Retourne les informations complètes du véhicule pour affichage dans le formulaire de maintenance."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_INFO_VEHIC_MAINT, (id_vehicule,))
            result = curseur.fetchone()
            if result:
                colonnes = [col[0] for col in curseur.description]
                return dict(zip(colonnes, result))
        finally:
            database.fermer_connexion(connexion)
    return None


def get_infos_maint_vehicule_par_id_maint(id_vehicule):
    """Retourne les informations complètes du véhicule pour affichage dans le formulaire de maintenance."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_INFO_VEHIC_MAINT_BT_MAINT, (id_vehicule,))
            result = curseur.fetchone()
            if result:
                colonnes = [col[0] for col in curseur.description]
                return dict(zip(colonnes, result))
        finally:
            database.fermer_connexion(connexion)
    return None


def lister_vehicules_en_maintenance():
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_TOUT_VEHICULES_MAINT_BT_MAINT)
            return curseur.fetchall()
        finally:
            database.fermer_connexion(connexion)