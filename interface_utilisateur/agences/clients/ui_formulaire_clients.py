from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QHBoxLayout
from fonctions_gestion.clients import ajouter_client, modifier_client
from PyQt5.QtCore import Qt

class FormulaireClientUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier un client.
    """
    def __init__(self, main_window, mode="ajouter", client=None):
        super().__init__()
        # Empêche l'héritage du background depuis le parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Remplit le fond avec la palette courante et définit le background en blanc
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-image: none; background-color: white;")
        self.setPalette(self.style().standardPalette())
        self.main_window = main_window
        self.mode = mode
        self.client = client  # Stocker les données du client en cas de modification
        self.setWindowTitle("Ajouter / Modifier un Client")
        self.setGeometry(100, 100, 600, 400)
        # Supprimer tout background en ne définissant pas de stylesheet
        self.setStyleSheet("")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire (tous NOT NULL dans la table CLIENTS)
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.ville_input = QLineEdit()
        self.adresse_input = QLineEdit()
        self.permis_cond_input = QLineEdit()
        self.hist_accidents_input = QLineEdit()   # Champ numérique (int)
        self.email_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.carte_cred_input = QLineEdit()

        # Remplir les champs si on est en mode "modifier"
        if self.mode == "modifier" and self.client:
            # On suppose que l'ordre de client_data correspond à l'ordre mentionné
            self.nom_input.setText(self.client[1])
            self.prenom_input.setText(self.client[2])
            self.ville_input.setText(self.client[3])
            self.adresse_input.setText(self.client[4])
            self.permis_cond_input.setText(self.client[5])
            self.hist_accidents_input.setText(str(self.client[6]))
            self.email_input.setText(self.client[7])
            self.telephone_input.setText(self.client[8])
            self.carte_cred_input.setText(self.client[9])

        # Ajout des champs au layout du formulaire
        form_layout.addRow("Nom :", self.nom_input)
        form_layout.addRow("Prénom :", self.prenom_input)
        form_layout.addRow("Ville :", self.ville_input)
        form_layout.addRow("Adresse :", self.adresse_input)
        form_layout.addRow("Permis de conduire :", self.permis_cond_input)
        form_layout.addRow("Historique d'accidents :", self.hist_accidents_input)
        form_layout.addRow("Email :", self.email_input)
        form_layout.addRow("Téléphone :", self.telephone_input)
        form_layout.addRow("Carte de crédit :", self.carte_cred_input)

        # Boutons
        self.btn_sauvegarder = QPushButton("💾 Sauvegarder")
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_annuler = QPushButton("❌ Annuler")

        # Définir une largeur fixe pour les boutons
        self.btn_sauvegarder.setFixedWidth(150)
        self.btn_effacer.setFixedWidth(150)
        self.btn_annuler.setFixedWidth(150)

        # Connexions des boutons
        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)
        self.btn_annuler.clicked.connect(self.annuler)

        # Layout horizontal pour centrer les boutons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_sauvegarder, alignment=Qt.AlignHCenter)
        btn_layout.addSpacing(10)  # Espace entre les boutons
        btn_layout.addWidget(self.btn_effacer, alignment=Qt.AlignHCenter)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.btn_annuler, alignment=Qt.AlignHCenter)

        # Ajout du formulaire et du layout des boutons dans le layout principal
        layout.addLayout(form_layout)
        layout.addSpacing(20)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def sauvegarder(self):
        """
        Enregistre les données en fonction du mode (ajouter ou modifier).
        """
        # Récupération des valeurs saisies
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        ville = self.ville_input.text().strip()
        adresse = self.adresse_input.text().strip()
        permis_cond = self.permis_cond_input.text().strip()
        hist_accidents = self.hist_accidents_input.text().strip()
        email = self.email_input.text().strip()
        telephone = self.telephone_input.text().strip()
        carte_cred = self.carte_cred_input.text().strip()

        # Vérification des champs obligatoires
        if not (nom and prenom and ville and adresse and permis_cond and email and telephone and carte_cred):
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        # Vérification de la saisie de l'historique d'accidents (champ int)
        if not hist_accidents.isdigit():
            QMessageBox.warning(self, "Erreur", "Le champ Historique d'accidents doit être un entier (ex: 0).")
            return
        hist_accidents = int(hist_accidents)

        if self.mode == "ajouter":
            # Pour l'ajout, on n'envoie pas hist_accidents
            ajouter_client(nom, prenom, ville, adresse, permis_cond, email, telephone, carte_cred)
        else:  # mode "modifier"
            id_client = self.client[0]
            modifier_client(id_client, nom, prenom, ville, adresse, permis_cond, hist_accidents, email, telephone, carte_cred)

        # Retour à la gestion des clients
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_clients)

    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.nom_input.clear()
        self.prenom_input.clear()
        self.ville_input.clear()
        self.adresse_input.clear()
        self.permis_cond_input.clear()
        self.hist_accidents_input.clear()
        self.email_input.clear()
        self.telephone_input.clear()
        self.carte_cred_input.clear()

    def annuler(self):
        """Annule l'action et retourne à la gestion des clients."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_clients)
