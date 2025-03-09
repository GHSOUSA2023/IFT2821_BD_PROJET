# Supprimer une agence
SUPPRIMER_AGENCE = """
DELETE FROM AGENCES WHERE ID_AGE = ?;
"""

# Supprimer un employé
SUPPRIMER_EMPLOYE = """
DELETE FROM EMPLOYES WHERE ID_EMP = ?;
"""

# Supprimer une marque par ID
SUPPRIMER_MARQUE = """
DELETE FROM MARQUE_VEHIC
WHERE ID_MARQ = ?;
"""

# Supprimer un modèle
SUPPRIMER_MODELE = """
DELETE FROM MODELE_VEHIC WHERE ID_MOD = ?;
"""

# Supprimer un optionnel
SUPPRIMER_OPTIONNEL = """
DELETE FROM OPTIONNELS WHERE ID_OPTIO = ?;
"""

# Supprimer une maintenance
SUPPRIMER_MAINTENANCE = """
DELETE FROM MAINTENANCE WHERE ID_MAINTEN = ?;
"""

# Requête pour supprimer un véhicule
SUPPRIMER_VEHICULE = """
DELETE FROM FLOTTE WHERE ID_VEHIC = ?;
"""

# Requête pour supprimer une assurance
SUPPRIMER_ASSURANCE = """
DELETE FROM ASSURANCE WHERE ID_ASSURANCE = ?;
"""
