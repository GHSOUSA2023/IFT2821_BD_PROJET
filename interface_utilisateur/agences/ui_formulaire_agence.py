from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, TITLE_STYLE
from fonctions_gestion.agences import ajouter_agence, modifier_agence

class FormulaireAgenceUI(QWidget):
    """
    Interface pour ajouter ou modifier une agence.
    Elle est utilisée à la fois pour l'ajout et la modification.
    """
    def __init__(self, main_window, mode="ajouter", agence_data=None):
        """
        :param main_window: Référence à la MainWindow (QStackedWidget)
        :param mode: "ajouter" ou "modifier"
        :param agence_data: Données de l'agence si modification (sinon None)
        """
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        self.agence_data = agence_data  # Si modification, contient les données existantes
        self.setWindowTitle("Ajouter / Modifier une Agence")
        self.setStyleSheet("background-color: #EAEDED;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre dynamique (ajout ou modification)
        self.label_title = QLabel("AJOUTER UNE AGENCE" if self.mode == "ajouter" else "MODIFIER UNE AGENCE")
        self.label_title.setStyleSheet(TITLE_STYLE)
        self.label_title.setAlignment(Qt.AlignCenter)

        # Formulaire
        form_layout = QFormLayout()

        self.nom_input = QLineEdit()
        self.adresse_input = QLineEdit()
        self.ville_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Pré-remplir les champs si mode modification
        if self.mode == "modifier" and self.agence_data:
            self.nom_input.setText(self.agence_data["nom"])
            self.adresse_input.setText(self.agence_data["adresse"])
            self.ville_input.setText(self.agence_data["ville"])
            self.telephone_input.setText(self.agence_data["telephone"])
            self.email_input.setText(self.agence_data["email"])

        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Adresse:", self.adresse_input)
        form_layout.addRow("Ville:", self.ville_input)
        form_layout.addRow("Téléphone:", self.telephone_input)
        form_layout.addRow("Email:", self.email_input)

        # Boutons
        self.btn_valider = QPushButton("✅ Valider")
        self.btn_retour = QPushButton("⬅ Retour")

        self.btn_valider.setStyleSheet(BUTTON_STYLE)
        self.btn_retour.setStyleSheet(BUTTON_STYLE)

        self.btn_valider.clicked.connect(self.valider_agence)
        self.btn_retour.clicked.connect(self.retourner)

        # Ajout au layout principal
        layout.addWidget(self.label_title)
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_valider)
        layout.addWidget(self.btn_retour)

        self.setLayout(layout)

    def valider_agence(self):
        """
        Valide et enregistre les données de l'agence (ajout ou modification).
        """
        nom = self.nom_input.text().strip()
        adresse = self.adresse_input.text().strip()
        ville = self.ville_input.text().strip()
        telephone = self.telephone_input.text().strip()
        email = self.email_input.text().strip()

        if not all([nom, adresse, ville, telephone, email]):
            print("⚠ Tous les champs doivent être remplis.")
            return

        if self.mode == "ajouter":
            ajouter_agence(nom, adresse, ville, telephone, email)
        elif self.mode == "modifier" and self.agence_data:
            modifier_agence(self.agence_data["id"], nom, adresse, ville, telephone, email)

        # Retourner à la gestion des agences après validation
        self.retourner()

    def retourner(self):
        """
        Retourne à l'interface de gestion des agences.
        """
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_agences)
