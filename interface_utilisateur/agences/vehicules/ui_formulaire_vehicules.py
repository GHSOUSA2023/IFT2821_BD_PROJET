from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox
from fonctions_gestion.vehicules import ajouter_vehicule, modifier_vehicule
from fonctions_gestion.marques import lister_marques
from fonctions_gestion.modeles import lister_modeles
from fonctions_gestion.types_vehicules import lister_types_vehicules

class FormulaireVehiculeUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier un véhicule.
    """
    def __init__(self, main_window, mode="ajouter", vehicule=None):
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        self.vehicule = vehicule  # Stocker les données du véhicule si en mode modification
        self.setWindowTitle("Ajouter / Modifier un Véhicule")
        self.setGeometry(100, 100, 600, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.immatriculation_input = QLineEdit()
        self.annee_input = QLineEdit()
        self.couleur_input = QLineEdit()
        self.km_input = QLineEdit()
        
        self.marque_input = QComboBox()
        self.modele_input = QComboBox()
        self.type_input = QComboBox()
        self.status_input = QComboBox()

        # Charger les options disponibles
        self.marque_input.addItem("Sélectionner une marque")
        for marque in lister_marques():
            self.marque_input.addItem(marque[1], marque[0])  # (Nom, ID)

        self.modele_input.addItem("Sélectionner un modèle")
        for modele in lister_modeles():
            self.modele_input.addItem(modele[1], modele[0])  # (Nom, ID)

        self.type_input.addItem("Sélectionner un type")
        for type_veh in lister_types_vehicules():
            self.type_input.addItem(type_veh[1], type_veh[0])  # (Nom, ID)

        self.status_input.addItems(["Disponible", "En maintenance", "Réservé"])

        # Si en mode modification, remplir les champs
        if self.mode == "modifier" and self.vehicule:
            self.immatriculation_input.setText(self.vehicule[1])
            self.annee_input.setText(str(self.vehicule[2]))
            self.couleur_input.setText(self.vehicule[3])
            self.km_input.setText(str(self.vehicule[4]))

            self.marque_input.setCurrentIndex(self.marque_input.findData(self.vehicule[5]))
            self.modele_input.setCurrentIndex(self.modele_input.findData(self.vehicule[6]))
            self.type_input.setCurrentIndex(self.type_input.findData(self.vehicule[7]))
            self.status_input.setCurrentText(self.vehicule[8])

        form_layout.addRow("Immatriculation:", self.immatriculation_input)
        form_layout.addRow("Année de fabrication:", self.annee_input)
        form_layout.addRow("Couleur:", self.couleur_input)
        form_layout.addRow("Kilométrage:", self.km_input)
        form_layout.addRow("Marque:", self.marque_input)
        form_layout.addRow("Modèle:", self.modele_input)
        form_layout.addRow("Type de véhicule:", self.type_input)
        form_layout.addRow("Statut:", self.status_input)

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

    def sauvegarder(self):
        """
        Enregistre les données en fonction du mode (ajouter/modifier).
        """
        immatriculation = self.immatriculation_input.text()
        annee = self.annee_input.text()
        couleur = self.couleur_input.text()
        km = self.km_input.text()

        id_marque = self.marque_input.currentData()
        id_modele = self.modele_input.currentData()
        id_type = self.type_input.currentData()
        status = self.status_input.currentText()

        if not immatriculation or not annee or not couleur or not km:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        if self.mode == "ajouter":
            ajouter_vehicule(immatriculation, annee, couleur, km, id_marque, id_modele, id_type, status)
        elif self.mode == "modifier":
            id_vehicule = self.vehicule[0]
            modifier_vehicule(id_vehicule, immatriculation, annee, couleur, km, id_marque, id_modele, id_type, status)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_vehicules)

    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.immatriculation_input.clear()
        self.annee_input.clear()
        self.couleur_input.clear()
        self.km_input.clear()
        self.marque_input.setCurrentIndex(0)
        self.modele_input.setCurrentIndex(0)
        self.type_input.setCurrentIndex(0)
        self.status_input.setCurrentIndex(0)

    def annuler(self):
        """Annule l'action et retourne à la gestion des véhicules."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_vehicules)
