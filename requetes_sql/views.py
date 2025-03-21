# Récupérer les détails complets du contrat par ID
GET_CONTRAT_PAR_ID = """
    SELECT * 
    FROM VIEW_CONTRAT_DETAILS
    WHERE ID_RESERV = ?
"""
