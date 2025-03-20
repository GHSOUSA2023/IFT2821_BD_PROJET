from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate
from interface_utilisateur.clients.reservations.ui_formulaire_client import FormulaireClientUI
from fonctions_gestion.clients import rechercher_client_par_email, ajouter_client
from fonctions_gestion.reservations import ajouter_reservation_via_procedure, confirmer_reservation

class FormulaireReservationUI(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.id_client = None
        self.id_reservation = None
        self.setWindowTitle("Faire une Réservation")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.email_input = QLineEdit()
        self.btn_rechercher_client = QPushButton("🔎 Rechercher client")
        self.btn_rechercher_client.clicked.connect(self.rechercher_client)

        self.btn_nouveau_client = QPushButton("➕ Ajouter un nouveau client")
        self.btn_nouveau_client.clicked.connect(self.ouvrir_formulaire_nouveau_client)

        self.nom_label = QLabel("")
        self.prenom_label = QLabel("")
        self.adresse_label = QLabel("")
        self.ville_label = QLabel("")
        self.telephone_label = QLabel("")

        form_layout.addRow("Email client:", self.email_input)
        form_layout.addRow("", self.btn_rechercher_client)
        form_layout.addRow("", self.btn_nouveau_client)
        form_layout.addRow("Nom:", self.nom_label)
        form_layout.addRow("Prénom:", self.prenom_label)
        form_layout.addRow("Adresse:", self.adresse_label)
        form_layout.addRow("Ville:", self.ville_label)
        form_layout.addRow("Téléphone:", self.telephone_label)

        self.date_debut_input = QDateEdit()
        self.date_debut_input.setDate(QDate.currentDate())
        self.date_debut_input.setCalendarPopup(True)

        self.date_fin_input = QDateEdit()
        self.date_fin_input.setDate(QDate.currentDate())
        self.date_fin_input.setCalendarPopup(True)

        self.id_vehic_input = QLineEdit()
        self.id_tarif_input = QLineEdit()
        self.id_assurance_input = QLineEdit()
        self.id_optio_input = QLineEdit()

        form_layout.addRow("Date de début:", self.date_debut_input)
        form_layout.addRow("Date de fin:", self.date_fin_input)
        form_layout.addRow("ID Véhicule:", self.id_vehic_input)
        form_layout.addRow("ID Tarif:", self.id_tarif_input)
        form_layout.addRow("ID Assurance:", self.id_assurance_input)
        form_layout.addRow("ID Optionnel:", self.id_optio_input)

        self.btn_sauvegarder = QPushButton("💾 Sauvegarder pour plus tard")
        self.btn_sauvegarder.clicked.connect(self.sauvegarder_reservation)

        self.btn_confirmer = QPushButton("✅ Confirmer la réservation")
        self.btn_confirmer.clicked.connect(self.confirmer_reservation)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_sauvegarder)
        layout.addWidget(self.btn_confirmer)
        self.setLayout(layout)

    def rechercher_client(self):
        email = self.email_input.text()
        client = rechercher_client_par_email(email)
        if client:
            self.id_client = client[0]
            self.nom_label.setText(client[1])
            self.prenom_label.setText(client[2])
            self.adresse_label.setText(client[3])
            self.ville_label.setText(client[4])
            self.telephone_label.setText(client[5])
        else:
            QMessageBox.warning(self, "Erreur", "Aucun client trouvé avec cet email.")

    def ouvrir_formulaire_nouveau_client(self):
        if not hasattr(self.main_window, 'ui_formulaire_client'):
            self.main_window.ui_formulaire_client = FormulaireClientUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_formulaire_client)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_formulaire_client)

    def sauvegarder_reservation(self):
        if not self.id_client:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner ou créer un client avant de sauvegarder.")
            return

        date_debut = self.date_debut_input.date().toString("yyyy-MM-dd")
        date_fin = self.date_fin_input.date().toString("yyyy-MM-dd")
        self.id_reservation = ajouter_reservation_via_procedure(
            self.id_client,
            int(self.id_vehic_input.text()),
            date_debut,
            date_fin,
            int(self.id_tarif_input.text()),
            int(self.id_assurance_input.text()),
            int(self.id_optio_input.text()) if self.id_optio_input.text() else None
        )

        if self.id_reservation:
            QMessageBox.information(self, "Succès", f"Réservation sauvegardée (ID: {self.id_reservation}).")
        else:
            QMessageBox.warning(self, "Erreur", "La réservation n'a pas pu être créée.")

    def confirmer_reservation(self):
        if not self.id_reservation:
            if not self.id_client:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner ou créer un client avant de confirmer.")
                return

            date_debut = self.date_debut_input.date().toString("yyyy-MM-dd")
            date_fin = self.date_fin_input.date().toString("yyyy-MM-dd")

            self.id_reservation = ajouter_reservation_via_procedure(
                self.id_client,
                int(self.id_vehic_input.text()),
                date_debut,
                date_fin,
                int(self.id_tarif_input.text()),
                int(self.id_assurance_input.text()),
                int(self.id_optio_input.text()) if self.id_optio_input.text() else None
            )

            if not self.id_reservation:
                QMessageBox.warning(self, "Erreur", "La réservation n'a pas pu être créée pour confirmation.")
                return

        confirmer_reservation(self.id_reservation)
        QMessageBox.information(self, "Succès", f"Réservation confirmée (ID: {self.id_reservation}).")
