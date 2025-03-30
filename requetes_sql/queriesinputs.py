# Requête pour ajouter une agence
AJOUTER_AGENCE = """
INSERT INTO AGENCES (NOM_AGE, ADRESSE, VILLE, TELEPHONE, EMAIL)
VALUES (?, ?, ?, ?, ?);
"""

# Requête pour ajouter un employé
AJOUTER_EMPLOYE = """
INSERT INTO EMPLOYES (NAS, NOM, PRENOM, SALAIRE, POSTE, ID_AGE)
VALUES (?, ?, ?, ?, ?, ?);
"""

# Requête pour ajouter une marque de véhicule
AJOUTER_MARQUE = """
INSERT INTO MARQUE_VEHIC (MARQUE)
VALUES (?);
"""

# Requête pour ajouter un modèle de véhicule
AJOUTER_MODELE = """
INSERT INTO MODELE_VEHIC (MODELE)
VALUES (?);
"""

# Requête pour ajouter un type de véhicule
AJOUTER_TYPE_VEHICULE = """
INSERT INTO TYPE_VEHIC (TYPE_VEHIC)
VALUES (?);
"""

# Requête pour ajouter un véhicule avec disponibilité
AJOUTER_VEHICULE = """
DECLARE @nouvel_id INT;

-- Insérer dans la table FLOTTE
INSERT INTO FLOTTE (
    ID_MARQ, ID_MOD, ID_TP_VEHIC, ANNEE_FAB, COULEUR, IMMATRICULATION, STATUS, KM, TYPE_CARBUR
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);

-- Récupérer l'ID généré automatiquement
SET @nouvel_id = SCOPE_IDENTITY();

-- Insérer dans la table DISPO_VEHICULE avec l'ID de l'agence
INSERT INTO DISPO_VEHICULE (ID_VEHIC, ID_AGE, DISPON_STOCK)
VALUES (@nouvel_id, ?, 'DISPONIBLE');
"""



# Requête pour ajouter un optionnel
AJOUTER_OPTIONNEL = """
INSERT INTO OPTIONNELS (NOM_OPTIO, PRIX_OPTIO_JOUR)
VALUES (?, ?);
"""
# Ajouter une maintenance
AJOUTER_MAINTENANCE = """
INSERT INTO MAINTENANCE (ID_VEHIC, ID_EMP, TYPE_MAINTEN, DATE_MAINTEN, DESC_MAINTEN, STATUS_MAINT)
VALUES (?, ?, ?, ?, ?, ?);
"""

# Requête pour ajouter une assurance
AJOUTER_ASSURANCE = """
INSERT INTO ASSURANCE (TYPE_ASSURANCE, PRIX_JOUR)
VALUES (?, ?);
"""

# Requête pour ajouter une reservation
AJOUTER_RESERVATION = """
INSERT INTO RESERVATIONS (DATE_DEBUT, DATE_FIN, STATUS_RESER, ID_CLIENT, ID_VEHIC, ID_TARIF, ID_ASSURANCE, ID_OPTIO)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

# Ajouter un client
AJOUTER_CLIENT = """
INSERT INTO CLIENTS (NOM, PRENOM, VILLE, ADRESSE, PERMIS_COND, EMAIL, TELEPHONE, CARTE_CRED)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

#Ajouter une nouvelle tarification
AJOUTER_TARIFICATION = """
    INSERT INTO TARIFICATIONS (KM_JOUR, PRIX_LOCAT_JOUR, ID_TP_VEHIC)
    VALUES (?, ?, ?)
"""

# Ajouter un incident
AJOUTER_INCIDENT = """
INSERT INTO INCIDENTS (TYPE_INCIDENT, DATE_INCIDENT, COUTS, DETAILS, ID_CONTRACT)
VALUES (?, ?, ?, ?, ?)
"""