# Modifier une agence
MODIFIER_AGENCE = """
UPDATE AGENCES
SET NOM_AGE = ?, ADRESSE = ?, VILLE = ?, TELEPHONE = ?, EMAIL = ?
WHERE ID_AGE = ?;
"""

# Modifier un employé
MODIFIER_EMPLOYE = """
UPDATE EMPLOYES 
SET NAS = ?, NOM = ?, PRENOM = ?, SALAIRE = ?, POSTE = ?, ID_AGE = ?
WHERE ID_EMP = ?;
"""

# Modifier une marque existante
MODIFIER_MARQUE = """
UPDATE MARQUE_VEHIC
SET MARQUE = ?
WHERE ID_MARQ = ?;
"""

# Modifier un modèle
MODIFIER_MODELE = """
UPDATE MODELE_VEHIC SET MODELE = ? WHERE ID_MOD = ?;
"""

# Modifier un optionnel
MODIFIER_OPTIONNEL = """
UPDATE OPTIONNELS SET NOM_OPTIO = ?, PRIX_OPTIO_JOUR = ? WHERE ID_OPTIO = ?;
"""

# Modifier une maintenance
MODIFIER_MAINTENANCE = """
UPDATE MAINTENANCE
SET TYPE_MAINTEN = ?, DATE_MAINTEN_FIN = ?, DESC_MAINTEN = ?, STATUS_MAINT = ?
WHERE ID_MAINTEN = ?;
"""

# Requête pour modifier une assurance
MODIFIER_ASSURANCE = """
UPDATE ASSURANCE 
SET TYPE_ASSURANCE = ?, PRIX_JOUR = ? 
WHERE ID_ASSURANCE = ?;
"""

# Requête pour modifier une reservation
MODIFIER_RESERVATION = """
UPDATE RESERVATIONS
SET DATE_DEBUT = ?, 
    DATE_FIN = ?, 
    STATUS_RESER = ?, 
    ID_VEHIC = ?, 
    ID_TARIF = ?, 
    ID_ASSURANCE = ?, 
    ID_OPTIO = ?
WHERE ID_RESERV = ?;
"""

# Requete update status reservation
UPDATE_STATUS_RESERVATION = """
UPDATE RESERVATIONS SET STATUS_RESER = 'CONFIRMEE' 
WHERE ID_RESERV = ?;
"""

# Requete update status reservation
UPDATE_STATUS_RESERVATION_ANNULEE = """
UPDATE RESERVATIONS SET STATUS_RESER = 'ANNULEE'
WHERE ID_RESERV = ?;
""" 

# Modifier un client
MODIFIER_CLIENT = """
UPDATE CLIENTS
SET NOM = ?, PRENOM = ?, ADRESSE = ?, PERMIS_COND = ?, HIST_ACCIDENTS = ?, EMAIL = ?, TELEPHONE = ?, CARTE_CRED = ?
WHERE ID_CLIENT = ?;
"""

#Modifier un véhicule
MODIFIER_VEHICULE_FLOTTE = """
UPDATE FLOTTE
SET ID_MARQ = ?, ID_MOD = ?, ID_TP_VEHIC = ?, ANNEE_FAB = ?, COULEUR = ?, IMMATRICULATION = ?, STATUS = ?, KM = ?, TYPE_CARBUR = ?       
WHERE ID_VEHIC = ?;        
"""

MODIFIER_DISPO_VEHICULE = """
UPDATE DISPO_VEHICULE
SET ID_AGE = ?
WHERE ID_VEHIC = ?;
"""

# Modifier une tarification existante
MODIFIER_TARIFICATION = """
    UPDATE TARIFICATIONS
    SET KM_JOUR = ?, PRIX_LOCAT_JOUR = ?, ID_TP_VEHIC = ?
    WHERE ID_TARIF = ?
"""

# Requête pour modifier une contrat
MODIFIER_CONTRAT = """
UPDATE CONTRACTS
SET DATE_FIN = ?, 
    STATUS_CONTRACT = ?, 
    DUREE_JOURS = ?,
    PRIX_TOTAL = ?
WHERE ID_RESERV = ?;
"""

# Terminer une maintenance (mise à jour)
TERMINER_MAINTENANCE = """
UPDATE MAINTENANCE
SET DATE_MAINTEN_FIN = ?, DESC_MAINTEN = ?, STATUS_MAINT = 'TERMINEE'
WHERE ID_VEHIC = ? AND STATUS_MAINT = 'EN MAINTENANCE';
"""
