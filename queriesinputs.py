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

# Requête pour ajouter un véhicule
AJOUTER_VEHICULE = """
INSERT INTO FLOTTE (TYPE_CARBUR, ANNEE_FAB, COULEUR, IMMATRICULATION, STATUS, KM, ID_MARQ, ID_MOD, ID_TP_VEHIC)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

# Requête pour ajouter un optionnel
AJOUTER_OPTIONNEL = """
INSERT INTO OPTIONNELS (NOM_OPTIO, PRIX_OPTIO_JOUR)
VALUES (?, ?);
"""

# Requête pour ajouter une assurance
AJOUTER_ASSURANCE = """
INSERT INTO ASSURANCE (TYPE_ASSURANCE, PRIX_JOUR)
VALUES (?, ?);
"""
