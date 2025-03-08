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