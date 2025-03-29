from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from fonctions_gestion.clients import ajouter_client, modifier_client

class FormulaireClientUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier un client.
    """
    def __init__(self, main_window, mode="ajouter", client=None):
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        self.client = client  # Stocker les données du client en cas de modification
        self.setWindowTitle("Ajouter / Modifier un Client")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.email_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.adresse_input = QLineEdit()

        # Si en mode modification, remplir les champs avec les données existantes
        if self.mode == "modifier" and self.client:
            self.nom_input.setText(self.client[1])
            self.prenom_input.setText(self.client[2])
            self.email_input.setText(self.client[3])
            self.telephone_input.setText(self.client[4])
            self.adresse_input.setText(self.client[5])

        form_layout.addRow("Nom :", self.nom_input)
        form_layout.addRow("Prénom :", self.prenom_input)
        form_layout.addRow("Email :", self.email_input)
        form_layout.addRow("Téléphone :", self.telephone_input)
        form_layout.addRow("Adresse :", self.adresse_input)

        # Boutons
        self.btn_sauvegarder = QPushButton("💾 Sauvegarder")
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_annuler = QPushButton("❌ Annuler")

        # Connexions des boutons
        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)
        self.btn_annuler.clicked.connect(self.annuler)

        # Agencement des boutons dans un sous-layout
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_sauvegarder)
        btn_layout.addWidget(self.btn_effacer)
        btn_layout.addWidget(self.btn_annuler)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def sauvegarder(self):
        """
        Enregistre les données en fonction du mode (ajouter ou modifier).
        """
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        email = self.email_input.text().strip()
        telephone = self.telephone_input.text().strip()
        adresse = self.adresse_input.text().strip()

        # Vérification des champs obligatoires
        if not nom or not prenom or not email:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir les champs obligatoires (Nom, Prénom, Email).")
            return

        # Ici, on fournit des valeurs par défaut pour les champs non présents dans le formulaire
        ville = "N/A"           # Valeur par défaut ou vous pouvez ajouter un champ dans le formulaire
        permis_cond = "N/A"     # Valeur par défaut
        carte_cred = "N/A"      # Valeur par défaut
        hist_accidents = "N/A"  # Pour la modification

        if self.mode == "ajouter":
            ajouter_client(nom, prenom, ville, adresse, permis_cond, email, telephone, carte_cred)
        elif self.mode == "modifier":
            id_client = self.client[0]  # Récupérer l'ID du client existant
            modifier_client(id_client, nom, prenom, ville, adresse, permis_cond, hist_accidents, email, telephone, carte_cred)

        # Retour à la gestion des clients
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_clients)

    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.nom_input.clear()
        self.prenom_input.clear()
        self.email_input.clear()
        self.telephone_input.clear()
        self.adresse_input.clear()

    def annuler(self):
        """Annule l'action et retourne à la gestion des clients."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_clients)
