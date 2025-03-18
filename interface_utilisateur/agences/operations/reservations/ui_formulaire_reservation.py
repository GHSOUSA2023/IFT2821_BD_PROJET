from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox
from fonctions_gestion.reservations import ajouter_reservation, modifier_reservation
from fonctions_gestion.clients import lister_tous_clients  # Pour récupérer les clients
from fonctions_gestion.vehicules import lister_tous_vehicules  # Pour récupérer les véhicules
from fonctions_gestion.tarifications import lister_toutes_tarifications  # Pour récupérer les tarifs
from fonctions_gestion.assurances import lister_toutes_assurances  # Pour récupérer les assurances
from fonctions_gestion.optionnels import lister_tout_optionnels  # Pour récupérer les options
from constantes import constantes  # Pour récupérer les statuts des réservations

class FormulaireReservationUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier une réservation.
    """
    def __init__(self, main_window, mode="ajouter", reservation=None):
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        self.reservation = reservation  # Stocker les données de la réservation si en mode modification
        self.setWindowTitle("Ajouter / Modifier une Réservation")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.date_debut_input = QLineEdit()
        self.date_fin_input = QLineEdit()
        self.status_input = QComboBox()
        self.duree_input = QLineEdit()
        self.client_input = QComboBox()
        self.vehicule_input = QComboBox()
        self.tarif_input = QComboBox()
        self.assurance_input = QComboBox()
        self.optionnel_input = QComboBox()
        self.prix_total_input = QLineEdit()

        # Charger les statuts de réservation
        self.status_input.addItem("Sélectionner un statut")
        for status in constantes.STATUS_RESERVATION:
            self.status_input.addItem(status)

        # Charger la liste des clients
        clients = lister_tous_clients()
        self.client_input.addItem("Sélectionner un client", None)  
        for client in clients:
            self.client_input.addItem(f"{client[0]} - {client[1]} {client[2]}", client[0])  

        # Charger la liste des véhicules
        vehicules = lister_tous_vehicules()
        self.vehicule_input.addItem("Sélectionner un véhicule", None)  
        for vehicule in vehicules:
            self.vehicule_input.addItem(f"{vehicule[0]} - {vehicule[1]}", vehicule[0])  

        # Charger la liste des tarifs
        tarifs = lister_toutes_tarifications()
        self.tarif_input.addItem("Sélectionner un tarif", None)  
        for tarif in tarifs:
            self.tarif_input.addItem(f"{tarif[0]} - {tarif[1]}", tarif[0])  

        # Charger la liste des assurances
        assurances = lister_toutes_assurances()
        self.assurance_input.addItem("Sélectionner une assurance", None)  
        for assurance in assurances:
            self.assurance_input.addItem(f"{assurance[0]} - {assurance[1]}", assurance[0])  

        # Charger la liste des options
        optionnels = lister_tout_optionnels()
        self.optionnel_input.addItem("Aucune option", None)  
        for option in optionnels:
            self.optionnel_input.addItem(f"{option[0]} - {option[1]}", option[0])  

        # Si en mode modification, remplir les champs
        if self.mode == "modifier" and self.reservation:
            self.date_debut_input.setText(self.reservation[1])
            self.date_fin_input.setText(self.reservation[2])
            self.duree_input.setText(str(self.reservation[4]))
            self.prix_total_input.setText(str(self.reservation[10]))

            index_status = self.status_input.findText(self.reservation[3])
            if index_status >= 0:
                self.status_input.setCurrentIndex(index_status)

            index_client = self.client_input.findData(self.reservation[5])  
            if index_client >= 0:
                self.client_input.setCurrentIndex(index_client)

            index_vehicule = self.vehicule_input.findData(self.reservation[6])  
            if index_vehicule >= 0:
                self.vehicule_input.setCurrentIndex(index_vehicule)

            index_tarif = self.tarif_input.findData(self.reservation[7])  
            if index_tarif >= 0:
                self.tarif_input.setCurrentIndex(index_tarif)

            index_assurance = self.assurance_input.findData(self.reservation[8])  
            if index_assurance >= 0:
                self.assurance_input.setCurrentIndex(index_assurance)

            index_optionnel = self.optionnel_input.findData(self.reservation[9])  
            if index_optionnel >= 0:
                self.optionnel_input.setCurrentIndex(index_optionnel)

        form_layout.addRow("Date Début (YYYY-MM-DD):", self.date_debut_input)
        form_layout.addRow("Date Fin (YYYY-MM-DD):", self.date_fin_input)
        form_layout.addRow("Statut:", self.status_input)
        form_layout.addRow("Durée (jours):", self.duree_input)
        form_layout.addRow("Client:", self.client_input)
        form_layout.addRow("Véhicule:", self.vehicule_input)
        form_layout.addRow("Tarif:", self.tarif_input)
        form_layout.addRow("Assurance:", self.assurance_input)
        form_layout.addRow("Optionnel:", self.optionnel_input)
        form_layout.addRow("Prix Total (€):", self.prix_total_input)

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
        date_debut = self.date_debut_input.text()
        date_fin = self.date_fin_input.text()
        status = self.status_input.currentText()
        duree = self.duree_input.text()
        id_client = self.client_input.currentData()
        id_vehicule = self.vehicule_input.currentData()
        id_tarif = self.tarif_input.currentData()
        id_assurance = self.assurance_input.currentData()
        id_optionnel = self.optionnel_input.currentData()
        prix_total = self.prix_total_input.text()

        if status == "Sélectionner un statut":
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un statut valide.")
            return

        if id_client is None or id_vehicule is None or id_tarif is None or id_assurance is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner toutes les informations obligatoires.")
            return

        if self.mode == "ajouter":
            ajouter_reservation(date_debut, date_fin, status, duree, id_client, id_vehicule, id_tarif, id_assurance, id_optionnel, prix_total)
        elif self.mode == "modifier":
            id_reserv = self.reservation[0]
            modifier_reservation(id_reserv, date_debut, date_fin, status, duree, id_client, id_vehicule, id_tarif, id_assurance, id_optionnel, prix_total)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_reservations)

    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.date_debut_input.clear()
        self.date_fin_input.clear()
        self.duree_input.clear()
        self.prix_total_input.clear()

    def annuler(self):
        """Annule l'action et retourne à la gestion des réservations."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_reservations)
