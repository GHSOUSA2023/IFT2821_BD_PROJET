#procedures stockées par ajouter reservation
AJOUTER_RESERVATION_PROCEDURE = """
    DECLARE @res INT;
    EXEC AjouterNouvelleReservation 
        @ID_CLIENT=?, 
        @ID_VEHIC=?, 
        @DATE_DEBUT=?, 
        @DATE_FIN=?, 
        @ID_TARIF=?, 
        @ID_ASSURANCE=?, 
        @ID_OPTIO=?, 
        @ID_RESERV=@res OUTPUT;
    SELECT @res AS ID_RESERV;
"""
