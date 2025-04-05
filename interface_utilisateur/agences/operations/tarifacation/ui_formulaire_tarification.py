from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox
from fonctions_gestion.tarifications import ajouter_tarification, modifier_tarification, 
from fonctions_gestion.vehicules import lister_types_vehicules  # Pour récupérer les types de véhicules

class FormulaireTarificationUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier une tarification.
    """
    def __init__(self, main_window, mode="ajouter", tarification=None):
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        self.tarification = tarification  # Stocker les données de la tarification si en mode modification
        self.setWindowTitle("Ajouter / Modifier une Tarification")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.km_jour_input = QLineEdit()
        self.prix_locat_input = QLineEdit()
        self.type_vehicule_input = QComboBox()  

        # Charger les types de véhicules dans le ComboBox
        self.type_vehicule_input.addItem("Sélectionner un type")  # Option vide par défaut
        types_vehicules = lister_types_vehicules()
        for type_veh in types_vehicules:
            self.type_vehicule_input.addItem(type_veh[1], type_veh[0])  # ID et Nom

        # Si en mode modification, remplir les champs
        if self.mode == "modifier" and self.tarification:
            self.km_jour_input.setText(str(self.tarification[1]))
            self.prix_locat_input.setText(str(self.tarification[2]))

            index_type = self.type_vehicule_input.findData(self.tarification[3])  
            if index_type >= 0:
                self.type_vehicule_input.setCurrentIndex(index_type)

        form_layout.addRow("KM/Jour:", self.km_jour_input)
        form_layout.addRow("Prix/Locat/Jour:", self.prix_locat_input)
        form_layout.addRow("Type Véhicule:", self.type_vehicule_input)

        #Ajouter les boutons
        self.btn_sauvegarder = QPushButton("💾 Sauvegarder")
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_annuler = QPushButton("⬅️ Retourner")

        #Connexions des boutons
        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)
        self.btn_annuler.clicked.connect(self.annuler)

        #Ajout des boutons dans un sous-layout
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
        km_jour = self.km_jour_input.text()
        prix_locat_jour = self.prix_locat_input.text()
        id_tp_vehic = self.type_vehicule_input.currentData()  

        if id_tp_vehic is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un type de véhicule valide.")
            return

        if self.mode == "ajouter":
            ajouter_tarification(km_jour, prix_locat_jour, id_tp_vehic)
        elif self.mode == "modifier":
            id_tarif = self.tarification[0]  # Récupérer l'ID de la tarification
            modifier_tarification(id_tarif, km_jour, prix_locat_jour, id_tp_vehic)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_tarifications)

    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.km_jour_input.clear()
        self.prix_locat_input.clear()
        self.type_vehicule_input.setCurrentIndex(0)  # Remettre à "Sélectionner un type"

    def annuler(self):
        """Annule l'action et retourne à la gestion des tarifications."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_tarifications)
