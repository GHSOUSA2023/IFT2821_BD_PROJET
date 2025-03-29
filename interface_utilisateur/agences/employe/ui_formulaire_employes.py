from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox
from fonctions_gestion.employes import ajouter_employe, modifier_employe
from fonctions_gestion.agences import lister_tout_agences  # Pour récupérer les agences
from constantes import constantes  # Pour récupérer les postes
from PyQt5.QtCore import Qt

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
        self.btn_sauvegarder = QPushButton("💾 Sauvegarder")
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_annuler = QPushButton("❌ Annuler")

        # ✅ Connexions des boutons
        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)
        self.btn_annuler.clicked.connect(self.annuler)

        # ✅ Ajout des boutons dans un sous-layout
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_sauvegarder)
        btn_layout.addWidget(self.btn_effacer)
        btn_layout.addWidget(self.btn_annuler)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def valider(self):
        """
        Enregistre les données en fonction du mode (ajouter/modifier).
        """
        nas = self.nas_input.text()
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        salaire = self.salaire_input.text()
        poste = self.poste_input.currentText()  # Correction pour récupérer l'option sélectionnée
        id_agence = self.agence_input.currentData()  # ID de l'agence sélectionnée

        if self.mode == "ajouter":
            ajouter_employe(nas, nom, prenom, salaire, poste, id_agence)
        elif self.mode == "modifier":
            id_emp = self.employe[0]  # Récupérer l'ID de l'employé
            modifier_employe(id_emp, nas, nom, prenom, salaire, poste, id_agence)

        # Retourner à la gestion des employés
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_employes)


    def sauvegarder(self):
        """
        Enregistre les données en fonction du mode (ajouter/modifier).
        """
        nas = self.nas_input.text()
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        salaire = self.salaire_input.text()
        poste = self.poste_input.currentText()  
        id_agence = self.agence_input.currentData()  

        if poste == "Sélectionner un poste":
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un poste valide.")
            return

        if id_agence is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une agence valide.")
            return

        if self.mode == "ajouter":
            ajouter_employe(nas, nom, prenom, salaire, poste, id_agence)
        elif self.mode == "modifier":
            id_employe = self.employe[0]  # Récupérer l'ID de l'employé
            modifier_employe(id_employe, nas, nom, prenom, salaire, poste, id_agence)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_employes)

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
