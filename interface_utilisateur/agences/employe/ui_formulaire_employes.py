from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox
from fonctions_gestion.employes import ajouter_employe, modifier_employe
from fonctions_gestion.agences import lister_tout_agences  # Pour récupérer les agences
from constantes import constantes  # Pour récupérer les postes
from PyQt5.QtCore import Qt
import re

class FormulaireEmployeUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier un employé.
    """
    def __init__(self, main_window, mode="ajouter", employe=None):
        super().__init__()
        # Empêche l'héritage du background depuis le parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Remplit le fond avec la palette courante et définit le background en blanc
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-image: none; background-color: white;")
        self.setPalette(self.style().standardPalette())

        self.main_window = main_window
        self.mode = mode
        self.employe = employe  # Stocker les données de l'employé si en mode modification
        self.setWindowTitle("Ajouter / Modifier un Employé")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.nas_input = QLineEdit()
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.salaire_input = QLineEdit()
        self.poste_input = QComboBox()  
        self.agence_input = QComboBox()

        # Charger les postes disponibles dans le ComboBox
        self.poste_input.addItem("Sélectionner un poste")  # Option vide par défaut
        for poste in constantes.POSTES_EMPLOYES:
            self.poste_input.addItem(poste)

        # Charger la liste des agences dans le ComboBox
        agences = lister_tout_agences()
        self.agence_input.addItem("Sélectionner une agence", None)  # Option vide
        for agence in agences:
            self.agence_input.addItem(f"{agence[0]} - {agence[1]}", agence[0])  # ID et Nom

        # Si en mode modification, remplir les champs
        if self.mode == "modifier" and self.employe:
            self.nas_input.setText(str(self.employe[1]))
            self.nom_input.setText(self.employe[2])
            self.prenom_input.setText(self.employe[3])
            self.salaire_input.setText(str(self.employe[4]))

            index_poste = self.poste_input.findText(self.employe[5])
            if index_poste >= 0:
                self.poste_input.setCurrentIndex(index_poste)

            index_agence = self.agence_input.findData(self.employe[6])  
            if index_agence >= 0:
                self.agence_input.setCurrentIndex(index_agence)

        form_layout.addRow("NAS:", self.nas_input)
        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("Salaire:", self.salaire_input)
        form_layout.addRow("Poste:", self.poste_input)
        form_layout.addRow("Agence:", self.agence_input)

        # ✅ Ajouter les boutons
        self.btn_sauvegarder = QPushButton("💾 Ajouter l'employee")
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_retour = QPushButton("⬅️ Retourner")

        # ✅ Uniformiser la taille des boutons
        self.btn_sauvegarder.setFixedWidth(150)
        self.btn_effacer.setFixedWidth(150)
        self.btn_retour.setFixedWidth(150)

        # ✅ Connexions des boutons
        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)
        self.btn_retour.clicked.connect(self.annuler)

        # ✅ Créer un layout vertical pour centrer les boutons
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter)  # Centrer les boutons horizontalement

        # ✅ Ajouter les boutons au layout avec espacement
        btn_layout.addWidget(self.btn_sauvegarder, alignment=Qt.AlignHCenter)
        btn_layout.addSpacing(10)  # Espace entre les boutons
        btn_layout.addWidget(self.btn_effacer, alignment=Qt.AlignHCenter)
        btn_layout.addSpacing(10)  # Espace entre les boutons
        btn_layout.addWidget(self.btn_retour, alignment=Qt.AlignHCenter)

        # ✅ Ajouter le layout des boutons au layout principal
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def sauvegarder(self):
        """
        Valide chaque champ individuellement et enregistre les données si tout est correct.
        """
        nas = self.nas_input.text().strip()
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        salaire = self.salaire_input.text().strip()
        poste = self.poste_input.currentText()
        id_agence = self.agence_input.currentData()

        # 🔍 Validations
        if not nas:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'NAS' est obligatoire.")
            return
        if not re.match(r'^\d{9}$', nas):
            QMessageBox.warning(self, "Format invalide", "Le NAS doit être une chaîne de 9 chiffres (ex: 111111114).")
            return

        if not nom:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Nom' est obligatoire.")
            return

        if not prenom:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Prénom' est obligatoire.")
            return

        if not salaire:
            QMessageBox.warning(self, "Champ manquant", "Le champ 'Salaire' est obligatoire.")
            return
        try:
            salaire_float = float(salaire)
            if salaire_float < 0:
                QMessageBox.warning(self, "Valeur invalide", "Le salaire doit être un nombre positif.")
                return
        except ValueError:
            QMessageBox.warning(self, "Format invalide", "Le salaire doit être un nombre valide.")
            return

        if poste == "Sélectionner un poste":
            QMessageBox.warning(self, "Champ manquant", "Veuillez sélectionner un poste valide.")
            return

        if id_agence is None:
            QMessageBox.warning(self, "Champ manquant", "Veuillez sélectionner une agence valide.")
            return

        # 🔐 Tentative d'enregistrement dans la base de données
        try:
            if self.mode == "ajouter":
                ajouter_employe(nas, nom, prenom, salaire_float, poste, id_agence)
                QMessageBox.information(self, "Succès", "Employé ajouté avec succès.")
            elif self.mode == "modifier":
                id_emp = self.employe[0]
                modifier_employe(id_emp, nas, nom, prenom, salaire_float, poste, id_agence)
                QMessageBox.information(self, "Succès", "Employé modifié avec succès.")

            # ✅ Retour uniquement après succès
            self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_employes)

        except Exception as e:
            erreur_str = str(e)
            if "Violation of UNIQUE KEY constraint 'UQ__EMPLOYES" in erreur_str:
                QMessageBox.critical(self, "NAS existant", f"Le NAS {nas} appartient déjà à un autre employé.")
            else:
                print(f"❌ Erreur lors de l'ajout ou modification de l'employé : {e}")
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue :\n{e}")




    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.nas_input.clear()
        self.nom_input.clear()
        self.prenom_input.clear()
        self.salaire_input.clear()
        self.poste_input.setCurrentIndex(0)  # Remettre à "Sélectionner un poste"
        self.agence_input.setCurrentIndex(0)  # Remettre à "Sélectionner une agence"

    def annuler(self):
        """Annule l'action et retourne à la gestion des employés."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_employes)
