from base_donnees import database
from requetes_sql import views
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from fpdf import FPDF


# Fonction pour récupérer les détails complets d'un contrat par son ID
def get_contrat_par_reservation(id_reservation):
    """Récupère les informations détaillées d'un contrat sous forme de dictionnaire."""
    connexion = database.connecter()
    contrat_details = None

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(views.GET_CONTRAT_PAR_ID, (id_reservation,))
            
            # Récupération dynamique des noms de colonnes
            colonnes = [colonne[0] for colonne in curseur.description]
            resultat = curseur.fetchone()
            
            if resultat:
                # Convertir le résultat en dictionnaire
                contrat_details = dict(zip(colonnes, resultat))
                
        except Exception as erreur:
            print(f"Erreur lors de la récupération du contrat : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return contrat_details


def generer_pdf_contrat(contenu_contrat, chemin_fichier):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    lignes = contenu_contrat.split('\n')
    for ligne in lignes:
        pdf.multi_cell(0, 10, ligne)

    pdf.output(chemin_fichier)
    print(f"PDF enregistré sous {chemin_fichier}")

def envoyer_contrat_email(destinataire, sujet, corps, chemin_pdf):
    expediteur = "tonemail@gmail.com"  # À remplacer par ton adresse Gmail
    mot_de_passe = "ton_mot_de_passe"   # À remplacer par ton mot de passe Gmail ou un mot de passe d’application

    message = MIMEMultipart()
    message['From'] = expediteur
    message['To'] = destinataire
    message['Subject'] = sujet

    message.attach(MIMEText(corps, 'plain'))

    with open(chemin_pdf, "rb") as pdf_file:
        piece = MIMEApplication(pdf_file.read(), _subtype="pdf")
        piece.add_header('Content-Disposition', 'attachment', filename=os.path.basename(chemin_pdf))
        message.attach(piece)

    try:
        serveur = smtplib.SMTP('smtp.gmail.com', 587)
        serveur.starttls()
        serveur.login(expediteur, mot_de_passe)
        serveur.send_message(message)
        serveur.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def remplir_contrat(donnees):
    # Construire le chemin absolu vers le fichier contrat_modele.txt
    chemin_modele = os.path.join(os.path.dirname(__file__), "../interface_utilisateur/contrats/contrat_modele.txt")
    chemin_modele = os.path.abspath(chemin_modele)

    contrat_modele = open(chemin_modele, "r", encoding="utf-8").read()
    contrat_rempli = contrat_modele.format(**donnees)
    return contrat_rempli

def get_contrats_par_email(email_client):
    connexion = database.connecter()
    contrats = []

    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(views.GET_CONTRATS_PAR_EMAIL, (email_client,))
            resultats = curseur.fetchall()
            for contrat in resultats:
                contrats.append(contrat)
        except Exception as erreur:
            print(f"Erreur lors de la récupération des contrats pour l'email {email_client} : {erreur}")
        finally:
            database.fermer_connexion(connexion)

    return contrats

def get_contrat_par_id_contract(id_reservation):
    """Récupère les détails d'un contrat par l'ID de réservation et retourne un dictionnaire."""
    connexion = database.connecter()
    contrat_details = None
    if connexion:
        try:
            curseur = connexion.cursor()
            curseur.execute(views.GET_CONTRAT_PAR_ID_CONTRACT, (id_reservation,))
            resultat = curseur.fetchone()
            if resultat:
                colonnes = [desc[0] for desc in curseur.description]
                contrat_details = dict(zip(colonnes, resultat))
        except Exception as erreur:
            print(f"Erreur lors de la récupération du contrat : {erreur}")
        finally:
            database.fermer_connexion(connexion)
    return contrat_details
