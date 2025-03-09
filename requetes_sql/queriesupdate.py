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

# Requête pour modifier un véhicule existant
MODIFIER_VEHICULE = """
UPDATE FLOTTE
SET TYPE_CARBUR = ?, ID_MARQ = ?, ID_MOD = ?, ID_TP_VEHIC = ?, ANNEE_FAB = ?, COULEUR = ?, IMMATRICULATION = ?, STATUS = ?, KM = ?
WHERE ID_VEHIC = ?;
"""

# Requête pour modifier une assurance
MODIFIER_ASSURANCE = """
UPDATE ASSURANCE 
SET TYPE_ASSURANCE = ?, PRIX_JOUR = ? 
WHERE ID_ASSURANCE = ?;
"""



