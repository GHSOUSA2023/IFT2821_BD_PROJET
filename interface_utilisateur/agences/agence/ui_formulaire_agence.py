from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from fonctions_gestion.agences import ajouter_agence, modifier_agence
from PyQt5.QtCore import Qt
import re


class FormulaireAgenceUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier une agence.
    """
    def __init__(self, main_window, mode="ajouter", agence=None):
        super().__init__()
        # Empêche l'héritage du background depuis le parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Permet de remplir le fond avec la palette courante
        self.setAutoFillBackground(True)
        # On définit ici le background voulu (blanc)
        self.setStyleSheet("background-image: none; background-color: white;")
        self.setPalette(self.style().standardPalette())
        self.main_window = main_window
        self.mode = mode
        self.agence = agence  # Stocker les données de l'agence si en mode modification
        self.setWindowTitle("Ajouter / Modifier une Agence")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.nom_input = QLineEdit()
        self.adresse_input = QLineEdit()
        self.ville_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Si en mode modification, remplir les champs
        if self.mode == "modifier" and self.agence:
            self.nom_input.setText(self.agence[1])  # Nom
            self.ville_input.setText(self.agence[2])  # Ville
            self.adresse_input.setText(self.agence[3])  # Adresse
            self.telephone_input.setText(self.agence[4])  # Téléphone
            self.email_input.setText(self.agence[5])  # Email

        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Ville:", self.ville_input)
        form_layout.addRow("Adresse:", self.adresse_input)
        form_layout.addRow("Téléphone:", self.telephone_input)
        form_layout.addRow("Email:", self.email_input)

        # Bouton de validation
        self.btn_valider = QPushButton("Valider")
        self.btn_valider.clicked.connect(self.valider)
        self.btn_valider.setFixedWidth(150)

        # Bouton de retour
        self.btn_retour = QPushButton("Retour")
        self.btn_retour.clicked.connect(self.retour)
        self.btn_retour.setFixedWidth(150)

        # Ajout des widgets au layout
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_valider)
        layout.addWidget(self.btn_retour)
        self.setLayout(layout)


        # Créer un layout horizontal pour centrer les boutons
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_valider, alignment=Qt.AlignHCenter)
        layout.addSpacing(10)  # Espace entre les boutons
        layout.addWidget(self.btn_retour, alignment=Qt.AlignHCenter)
        self.setLayout(layout)


    def valider(self):
        """
        Valide chaque champ individuellement et enregistre les données si tout est correct.
        """
        nom = self.nom_input.text().strip()
        adresse = self.adresse_input.text().strip()
        ville = self.ville_input.text().strip()
        telephone = self.telephone_input.text().strip()
        email = self.email_input.text().strip()

        # Validation individuelle
        if not nom:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Nom' est obligatoire.")
            return

        if not adresse:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Adresse' est obligatoire.")
            return

        if not ville:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Ville' est obligatoire.")
            return

        if not telephone:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Téléphone' est obligatoire.")
            return
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', telephone):
            QMessageBox.warning(self, "Format invalide", "Le format du téléphone doit être 123-456-7890.")
            return

        if not email:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Email' est obligatoire.")
            return
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            QMessageBox.warning(self, "Format invalide", "Le format de l'email est invalide.")
            return

        # Si tout est valide, procéder
        if self.mode == "ajouter":
            ajouter_agence(nom, adresse, ville, telephone, email)
            QMessageBox.information(self, "Succès", "Agence ajoutée avec succès.")
        elif self.mode == "modifier":
            id_agence = self.agence[0]
            modifier_agence(id_agence, nom, adresse, ville, telephone, email)
            QMessageBox.information(self, "Succès", "Agence modifiée avec succès.")

        # Retour à la gestion des agences
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_agences)


    def retour(self):
        """
        Retourne à l'interface de gestion des agences.
        """
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_agences)
