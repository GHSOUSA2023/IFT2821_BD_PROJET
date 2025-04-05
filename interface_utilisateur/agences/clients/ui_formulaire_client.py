from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from fonctions_gestion.clients import ajouter_client
import re
from PyQt5.QtCore import Qt

class FormulaireClientUI(QWidget):
    """
    Formulaire pour ajouter un nouveau client, intégré dans le QStackedWidget principal.
    """
    def __init__(self, parent, mode=None):
        super().__init__()
        # Empêche l'héritage du background depuis le parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Remplit le fond avec la palette courante et définit le background en blanc
        self.setAutoFillBackground(True)
        self.parent_form = parent
        self.setWindowTitle("Ajouter un nouveau client")
        self.setGeometry(150, 150, 500, 400)
        self.mode = mode
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

        #Bouton "Ajouter client"
        self.btn_valider = QPushButton("💾 Ajouter le client")
        self.btn_valider.setFixedWidth(150)
        self.btn_valider.clicked.connect(self.valider)

        #Bouton "Effacer"
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_effacer.setFixedWidth(150)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)

        #Bouton "Annuler"
        self.btn_annuler = QPushButton("⬅️ Retourner")
        self.btn_annuler.setFixedWidth(150)
        self.btn_annuler.clicked.connect(self.retourner_arriere)

        #Créer un layout vertical pour centrer les boutons
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter)  # Centrer les boutons horizontalement

        #Ajouter les boutons au layout avec espacement
        btn_layout.addWidget(self.btn_valider, alignment=Qt.AlignHCenter)
        btn_layout.addSpacing(10)  # Espace entre les boutons
        btn_layout.addWidget(self.btn_effacer, alignment=Qt.AlignHCenter)
        btn_layout.addSpacing(10)  # Espace entre les boutons
        btn_layout.addWidget(self.btn_annuler, alignment=Qt.AlignHCenter)

        #Ajouter le layout des boutons au layout principal
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def valider(self):
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        ville = self.ville_input.text().strip()
        adresse = self.adresse_input.text().strip()
        permis_cond = self.permis_cond_input.text().strip()
        email = self.email_input.text().strip()
        telephone = self.telephone_input.text().strip()
        carte_cred = self.carte_cred_input.text().strip()

        if not nom:
            QMessageBox.warning(self, "Erreur", "Le champ **Nom** est obligatoire.")
            return
        if not prenom:
            QMessageBox.warning(self, "Erreur", "Le champ **Prénom** est obligatoire.")
            return
        if not ville:
            QMessageBox.warning(self, "Erreur", "Le champ **Ville** est obligatoire.")
            return
        if not adresse:
            QMessageBox.warning(self, "Erreur", "Le champ **Adresse** est obligatoire.")
            return
        if not permis_cond or len(permis_cond) > 17:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un numéro de permis valide (maximum 17 caractères).")
            return
        if '@' not in email or '.' not in email.split('@')[-1]:
            QMessageBox.warning(self, "Erreur", "L'email est invalide. Format attendu : exemple@domaine.com")
            return
        if not re.match(r'^[1-9]\d{2}-[1-9]\d{2}-\d{4}$', telephone):
            QMessageBox.warning(self, "Erreur", "Le téléphone doit être au format XXX-XXX-XXXX.")
            return
        if not re.match(r'^\d{4,}', carte_cred):
            QMessageBox.warning(self, "Erreur", "Le numéro de carte de crédit doit commencer par au moins 4 chiffres.")
            return

        id_client = ajouter_client(nom, prenom, ville, adresse, permis_cond, email, telephone, carte_cred)

        if id_client and id_client != "EMAIL_EXISTE":
            QMessageBox.information(self, "Succès", "Client ajouté avec succès.")
            if hasattr(self.parent_form, 'main_window'):
                self.parent_form.id_client = id_client
                # Remplir les champs du formulaire de réservation
                self.parent_form.nom_label.setText(nom.upper())
                self.parent_form.prenom_label.setText(prenom.upper())
                self.parent_form.adresse_label.setText(adresse.upper())
                self.parent_form.ville_label.setText(ville.upper())
                self.parent_form.telephone_label.setText(telephone)
            self.effacer_formulaire()
            self.retourner_arriere()

        elif id_client == "EMAIL_EXISTE":
            QMessageBox.warning(self, "Erreur", "Cet email est déjà utilisé par un autre client.")
        else:
            QMessageBox.warning(self, "Erreur", "Échec de l'ajout du client.")

    def effacer_formulaire(self):
        self.nom_input.clear()
        self.prenom_input.clear()
        self.ville_input.clear()
        self.adresse_input.clear()
        self.permis_cond_input.clear()
        self.email_input.clear()
        self.telephone_input.clear()
        self.carte_cred_input.clear()


    def retourner_arriere(self):
        if hasattr(self.parent_form, 'main_window'):
            # Retourner au formulaire précédent (par exemple, le formulaire de réservation)
            self.parent_form.main_window.central_widget.setCurrentWidget(self.parent_form)
        elif hasattr(self.parent_form, 'central_widget'):
            # Retourner à l'interface des clients si ouvert depuis la fenêtre principale
            self.parent_form.central_widget.setCurrentWidget(self.parent_form.ui_gestion_clients)
        else:
            # En cas de problème inattendu
            print("Impossible de retourner à l'écran précédent.")
