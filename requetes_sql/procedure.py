#procedures stockées par ajouter reservation
PROCEDURE_CREE_RESERVATION = """""
EXEC AjouterNouvelleReservation @ID_CLIENT = ?, @ID_VEHIC = ?, @DATE_DEBUT = ?, @DATE_FIN = ?, @ID_TARIF = ?, @ID_ASSURANCE = ?, @ID_OPTIO = ?;
"""""