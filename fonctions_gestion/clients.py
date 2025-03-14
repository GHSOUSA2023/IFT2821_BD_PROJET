from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ------------------- GESTION DES CLIENTS -------------------

def ajouter_client(nom, prenom, adresse, permis_cond, hist_accidents, email, telephone, carte_cred):
    """Ajoute un nouveau client dans la base de données."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queries_clients.AJOUTER_CLIENT,
                (nom.upper(), prenom.upper(), adresse, permis_cond, hist_accidents, email.lower(), telephone, carte_cred),
            )
            connexion.commit()
            print("✅ Client ajouté avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de l'ajout du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)


def modifier_client(id_client, nom, prenom, adresse, permis_cond, hist_accidents, email, telephone, carte_cred):
    """Modifie les informations d'un client existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queries_clients.MODIFIER_CLIENT,
                (nom.upper(), prenom.upper(), adresse, permis_cond, hist_accidents, email.lower(), telephone, carte_cred, id_client),
            )
            connexion.commit()
            print("✅ Client modifié avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de la modification du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)


def supprimer_client(id_client):
    """Supprime un client par son ID."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries_clients.SUPPRIMER_CLIENT, (id_client,))
            connexion.commit()
            print("✅ Client supprimé avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de la suppression du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)


def lister_tous_clients():
    """Retourne une liste de tous les clients."""
    connexion = database.connecter()
    clients = []
    
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries_clients.LISTER_CLIENTS)
            resultats = curseur.fetchall()
            
            for client in resultats:
                clients.append((
                    client.ID_CLIENT,
                    client.NOM,
                    client.PRENOM,
                    client.ADRESSE,
                    client.PERMIS_COND,
                    client.HIST_ACCIDENTS,
                    client.EMAIL,
                    client.TELEPHONE,
                    client.CARTE_CRED
                ))
            
        except Exception as erreur:
            print(f"❌ Erreur lors de la récupération des clients : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    
    return clients


def rechercher_client(terme_recherche):
    """Recherche un client par nom, prénom ou permis de conduire."""
    connexion = database.connecter()
    colonnes = ["ID", "Nom", "Prénom", "Adresse", "Permis", "Historique Accidents", "Email", "Téléphone", "Carte Crédit"]
    clients = []
    
    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"
            curseur.execute(queries_clients.RECHERCHER_CLIENT, (terme, terme, terme))
            resultats = curseur.fetchall()
            
            for client in resultats:
                clients.append((
                    client.ID_CLIENT,
                    client.NOM,
                    client.PRENOM,
                    client.ADRESSE,
                    client.PERMIS_COND,
                    client.HIST_ACCIDENTS,
                    client.EMAIL,
                    client.TELEPHONE,
                    client.CARTE_CRED
                ))
        
        except Exception as erreur:
            print(f"❌ Erreur lors de la recherche du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    
    return colonnes, clients
