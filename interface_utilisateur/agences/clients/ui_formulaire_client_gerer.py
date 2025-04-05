from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from fonctions_gestion.clients import modifier_client
import re
from PyQt5.QtCore import Qt
from fonctions_gestion.clients import lister_tous_clients


class FormulaireClientGererUI(QWidget):
    """
    Formulaire pour modifier un client existant.
    """

    def __init__(self, parent, mode=None):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.parent_form = parent
        self.setWindowTitle("Modifier client")
        self.setGeometry(150, 150, 500, 400)
        self.mode = mode
        self.id_client = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.ville_input = QLineEdit()
        self.adresse_input = QLineEdit()
        self.permis_cond_input = QLineEdit()
        self.email_input = QLineEdit()
        self.email_input.setReadOnly(True)
        self.email_input.setStyleSheet("background-color: lightgray;")
        self.telephone_input = QLineEdit()
        self.carte_cred_input = QLineEdit()

        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("Ville:", self.ville_input)
        form_layout.addRow("Adresse:", self.adresse_input)
        form_layout.addRow("Permis de conduire:", self.permis_cond_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Téléphone:", self.telephone_input)
        form_layout.addRow("Carte de crédit:", self.carte_cred_input)

        self.btn_valider = QPushButton("💾 Enregistrer les modifications")
        self.btn_valider.clicked.connect(self.valider)


        self.btn_annuler = QPushButton("⬅️ Retourner")
        self.btn_annuler.clicked.connect(self.retourner_arriere)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_valider)
        layout.addWidget(self.btn_annuler)
        self.setLayout(layout)

    def set_info_client_complet(self, client):
        """Préremplit tous les champs avec les infos du client complet."""
        self.id_client = client[0]
        self.nom_input.setText(client[1])
        self.prenom_input.setText(client[2])
        self.ville_input.setText(client[3])
        self.adresse_input.setText(client[4])
        self.permis_cond_input.setText(client[5])
        self.email_input.setText(client[7])  # email
        self.telephone_input.setText(client[8])
        self.carte_cred_input.setText(client[9])


    def valider(self):
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        ville = self.ville_input.text().strip()
        adresse = self.adresse_input.text().strip()
        permis_cond = self.permis_cond_input.text().strip()
        email = self.email_input.text().strip()
        telephone = self.telephone_input.text().strip()
        carte_cred = self.carte_cred_input.text().strip()

        if not nom or not prenom or not ville or not adresse:
            QMessageBox.warning(self, "Erreur", "Tous les champs obligatoires doivent être remplis.")
            return

        if not permis_cond or len(permis_cond) > 17:
            QMessageBox.warning(self, "Erreur", "Numéro de permis invalide.")
            return

        if '@' not in email or '.' not in email.split('@')[-1]:
            QMessageBox.warning(self, "Erreur", "L'email est invalide.")
            return

        if not re.match(r'^[1-9]\d{2}-[1-9]\d{2}-\d{4}$', telephone):
            QMessageBox.warning(self, "Erreur", "Format de téléphone invalide.")
            return

        if not re.match(r'^\d{4,}', carte_cred):
            QMessageBox.warning(self, "Erreur", "Numéro de carte de crédit invalide.")
            return

        result = modifier_client(self.id_client, nom, prenom, ville, adresse, permis_cond, email, telephone, carte_cred)

        if result and result != "EMAIL_EXISTE":
            QMessageBox.information(self, "Succès", "Client modifié avec succès.")
            self.retourner_arriere()
        elif result == "EMAIL_EXISTE":
            QMessageBox.warning(self, "Erreur", "Cet email est déjà utilisé.")
        else:
            QMessageBox.warning(self, "Erreur", "La modification a échoué.")

    def effacer_formulaire(self):
        self.nom_input.clear()
        self.prenom_input.clear()
        self.ville_input.clear()
        self.adresse_input.clear()
        self.permis_cond_input.clear()
        self.telephone_input.clear()
        self.carte_cred_input.clear()

        if isinstance(self.parent_form, QWidget):
            self.parent_form.charger_donnees(lister_tous_clients())

        self.retourner_arriere()

    def retourner_arriere(self):
        if isinstance(self.parent_form, QWidget):
            self.parent_form.charger_donnees(lister_tous_clients())
            self.parent_form.main_window.central_widget.setCurrentWidget(self.parent_form)
