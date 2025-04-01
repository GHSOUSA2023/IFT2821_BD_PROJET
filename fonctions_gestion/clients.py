from base_donnees import database
from requetes_sql import queries, queriesinputs, queriesupdate, queriesdelete

# ------------------- GESTION DES CLIENTS -------------------

# Ajouter un client
def ajouter_client(nom, prenom, ville, adresse, permis_cond, email, telephone, carte_cred):
    """Ajoute un client à la base de données et gère les erreurs de duplication."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(
                queriesinputs.AJOUTER_CLIENT,
                (nom.upper(), prenom.upper(), ville.upper(), adresse.upper(), permis_cond.upper(),email.lower(), telephone, carte_cred),
            )
            connexion.commit()

            # Récupérer l'ID du nouveau client ajouté
            curseur.execute("SELECT MAX(ID_CLIENT) FROM CLIENTS WHERE EMAIL = ?", (email.lower(),))
            id_client = curseur.fetchone()[0]

            print("Client ajouté avec succès !")
            return id_client

        except Exception as erreur:
            print(f"Erreur SQL complète : {erreur}")
            if "violation of unique key constraint" in str(erreur).lower() and "clients" in str(erreur).lower():
                print("Cet email existe déjà.")
                return "EMAIL_EXISTE"

            print(f"Erreur lors de l'ajout du client : {erreur}")
            return None


# Récupérer un client par ID
def get_client_par_id(id_client):
    """Récupère les informations d'un client spécifique."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_CLIENT_PAR_ID, (id_client,))
            client = curseur.fetchone()
            return client
        except Exception as erreur:
            print(f"Erreur lors de la récupération du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

# Modifier un client
def modifier_client(id_client, nom, prenom, ville, adresse, permis_cond, email, telephone, carte_cred):
    """Modifie les informations d'un client existant."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            client = get_client_par_id(id_client)
            if not client:
                print("Aucun client trouvé avec cet ID.")
                return

            hist_accidents = client[6]  # On garde la valeur existante

            curseur.execute(
                queriesupdate.MODIFIER_CLIENT,
                (
                    nom.upper(),              # NOM
                    prenom.upper(),           # PRENOM
                    adresse.upper(),          # ADRESSE
                    permis_cond.upper(),      # PERMIS_COND
                    hist_accidents,           # HIST_ACCIDENTS (inchangé)
                    email.lower(),            # EMAIL
                    telephone,                # TELEPHONE
                    carte_cred,               # CARTE_CRED
                    id_client                 # WHERE ID_CLIENT = ?
                )
            )
            connexion.commit()
            print("✅ Client modifié avec succès !")
            return True

        except Exception as erreur:
            print(f"❌ Erreur lors de la modification du client : {erreur}")
            return None

        finally:
            database.fermer_connexion(connexion)


# Supprimer un client
def supprimer_client(id_client):
    """Supprime un client par son ID après vérification."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.GET_CLIENT_PAR_ID, (id_client,))
            client = curseur.fetchone()

            if not client:
                print("Aucun client trouvé avec cet ID.")
                return

            curseur.execute(queriesdelete.SUPPRIMER_CLIENT, (id_client,))
            connexion.commit()
            print("✅ Client supprimé avec succès !")
        except Exception as erreur:
            print(f"❌ Erreur lors de la suppression du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)

# Lister tous les clients
def lister_tous_clients():
    """Retourne une liste de tous les clients."""
    connexion = database.connecter()
    clients = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(queries.LISTER_CLIENTS)
            resultats = curseur.fetchall()

            for client in resultats:
                clients.append((
                    client.ID_CLIENT,
                    client.NOM,
                    client.PRENOM,
                    client.VILLE,
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

# Rechercher un client par nom, prénom ou email
def rechercher_client(terme_recherche):
    """Recherche un client par nom, prénom ou email et retourne les résultats sous forme de tableau."""
    connexion = database.connecter()
    colonnes = ["ID", "Nom", "Prénom", "Ville", "Adresse", "Permis", "Accidents", "Email", "Téléphone", "Carte Crédit"]
    clients = []

    if connexion:
        try:
            curseur = connexion.cursor()
            terme = f"%{terme_recherche}%"
            curseur.execute(queries.RECHERCHER_CLIENT, (terme, terme, terme))
            resultats = curseur.fetchall()

            for client in resultats:
                clients.append([
                    client.ID_CLIENT,
                    client.NOM,
                    client.PRENOM,
                    client.VILLE,
                    client.ADRESSE,
                    client.PERMIS_COND,
                    client.HIST_ACCIDENTS,
                    client.EMAIL,
                    client.TELEPHONE,
                    client.CARTE_CRED
                ])

        except Exception as erreur:
            print(f"❌ Erreur lors de la recherche du client : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return colonnes, clients

# Rechercher un client par email
def rechercher_client_par_email(email):
    """Recherche un client par son email et retourne ses informations principales."""
    connexion = database.connecter()
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute("""
                SELECT ID_CLIENT, NOM, PRENOM, ADRESSE, VILLE, TELEPHONE
                FROM CLIENTS
                WHERE EMAIL = ?
            """, (email,))
            client = curseur.fetchone()
            return client
        except Exception as erreur:
            print(f"❌ Erreur lors de la recherche du client par email : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return None

# fonctions_gestion/clients.py

def afficher_liste_clients_modifier():
    """
    Retourne les colonnes et la liste des clients pour la modification.
    Vous pouvez adapter les colonnes selon les informations souhaitées.
    """
    colonnes = ["ID", "Nom", "Prénom", "Ville", "Adresse", "Permis", "Accidents", "Email", "Téléphone", "Carte Crédit"]
    clients = lister_tous_clients()  # Utilise votre fonction existante pour lister tous les clients
    return colonnes, clients

def afficher_liste_clients_supprimer():
    """
    Retourne les colonnes et la liste des clients pour la suppression.
    Vous pouvez adapter les colonnes selon les informations souhaitées.
    """
    colonnes = ["ID", "Nom", "Prénom", "Email", "Téléphone"]
    clients = lister_tous_clients()  # Utilise votre fonction existante pour lister tous les clients
    return colonnes, clients
