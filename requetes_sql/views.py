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

# Lister tous les contrats de location par email
GET_CONTRATS_TOUT = """
SELECT * 
FROM VIEW_RESERVATION_DETAILS
ORDER BY CONTRAT_DATE_DEBUT DESC
"""

# Rechercher dans la vue des détails des réservations
RECHERCHER_RESERVATIONS = """
SELECT * 
FROM VIEW_RESERVATION_DETAILS
WHERE CONVERT(VARCHAR, ID_RESERV) LIKE ? 
   OR CONVERT(VARCHAR, ID_CONTRACT) LIKE ? 
   OR LOWER(NOM_CLIENT) LIKE ?
ORDER BY CONTRAT_DATE_DEBUT DESC
"""

