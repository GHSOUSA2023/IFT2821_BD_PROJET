# Supprimer une agence
SUPPRIMER_AGENCE = """
DELETE FROM AGENCES WHERE ID_AGE = ?;
"""

# Supprimer un employé
SUPPRIMER_EMPLOYE = """
DELETE FROM EMPLOYES WHERE ID_EMP = ?;
"""