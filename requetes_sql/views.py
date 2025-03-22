# Récupérer les détails complets du contrat par ID
GET_CONTRAT_PAR_ID = """
    SELECT * 
    FROM VIEW_CONTRAT_DETAILS
    WHERE ID_RESERV = ?
"""

############################# GESTION CONTRATS #############################

# Lister tous les contrats de location par email
GET_CONTRATS_PAR_EMAIL = """
SELECT * 
FROM VIEW_RESERVATION_DETAILS
WHERE EMAIL_CLIENT = ?
ORDER BY CONTRAT_DATE_DEBUT DESC
"""


# Récupérer les détails complets du contrat par ID
GET_CONTRAT_PAR_ID_CONTRACT = """
    SELECT * 
    FROM VIEW_RESERVATION_DETAILS
    WHERE ID_RESERV = ?
"""

