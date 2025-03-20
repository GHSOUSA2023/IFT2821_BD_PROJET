import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QDateEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDateEdit, QApplication
from PyQt5.QtCore import Qt, QTimer, QDate
from interface_utilisateur.clients.reservations.ui_formulaire_client import FormulaireClientUI
from fonctions_gestion.clients import rechercher_client_par_email, ajouter_client
from fonctions_gestion.reservations import ajouter_reservation_via_procedure, confirmer_reservation
from interface_utilisateur.tableaux.ui_tableau_assurance import TableauAssurancesUI
from interface_utilisateur.tableaux.ui_tableau_optionnel import TableauOptionnelsUI
from interface_utilisateur.tableaux.ui_tableau_tarifications import TableauTarificationsUI
from interface_utilisateur.tableaux.ui_tableau_vehicules import TableauVehiculesUI
from fonctions_gestion.vehicules import lister_tous_vehicules, lister_vehicules_disponibles
from fonctions_gestion.tarifications import lister_toutes_tarifications
from fonctions_gestion.assurances import lister_toutes_assurances
from fonctions_gestion.optionnels import lister_tout_optionnels

# Classe personnalisée pour afficher automatiquement le calendrier au focus
class CustomDateEdit(QDateEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.ouvrir_calendrier)

    def ouvrir_calendrier(self):
        # Simuler Alt + Down pour ouvrir le calendrier
        event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Down, Qt.AltModifier)
        QApplication.postEvent(self, event)



class FormulaireReservationUI(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.id_client = None
        self.id_reservation = None
        self.id_vehic = None
        self.id_tarif = None
        self.id_assurance = None
        self.id_optio = None
        self.setWindowTitle("Faire une Réservation")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs pour recherche de client
        self.email_input = QLineEdit()
        self.btn_rechercher_client = QPushButton("🔎 Rechercher client")
        self.btn_rechercher_client.clicked.connect(self.rechercher_client)

        self.btn_nouveau_client = QPushButton("➕ Ajouter un nouveau client")
        self.btn_nouveau_client.clicked.connect(self.ouvrir_formulaire_nouveau_client)

        # Informations du client
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

        # Dates de début
        self.date_debut_input = CustomDateEdit()
        self.date_debut_input.setDate(QDate.currentDate())
        self.date_debut_input.setMinimumDate(QDate.currentDate())
        self.date_debut_input.dateChanged.connect(self.mettre_a_jour_date_fin)

        # Date de fin
        self.date_fin_input = CustomDateEdit()
        self.date_fin_input.setDate(QDate.currentDate())
        self.date_fin_input.setMinimumDate(QDate.currentDate())
        self.date_fin_input.dateChanged.connect(self.calculer_total)


        # Sélections
        self.vehicule_label = QLabel("Aucun véhicule sélectionné")
        self.btn_vehicule = QPushButton("Sélectionner un véhicule")
        self.btn_vehicule.clicked.connect(self.afficher_tableau_vehicules)

        self.tarif_label = QLabel("Aucun tarif sélectionné")
        self.btn_tarif = QPushButton("Sélectionner un tarif")
        self.btn_tarif.clicked.connect(self.afficher_tableau_tarifications)

        self.assurance_label = QLabel("Aucune assurance sélectionnée")
        self.btn_assurance = QPushButton("Sélectionner une assurance")
        self.btn_assurance.clicked.connect(self.afficher_tableau_assurances)

        self.optionnel_label = QLabel("Aucune option sélectionnée")
        self.btn_optionnel = QPushButton("Sélectionner un optionnel")
        self.btn_optionnel.clicked.connect(self.afficher_tableau_optionnels)

        # Ajout des champs au formulaire
        form_layout.addRow("Date de début:", self.date_debut_input)
        form_layout.addRow("Date de fin:", self.date_fin_input)
        form_layout.addRow("Véhicule:", self.vehicule_label)
        form_layout.addRow("", self.btn_vehicule)
        form_layout.addRow("Tarif:", self.tarif_label)
        form_layout.addRow("", self.btn_tarif)
        form_layout.addRow("Assurance:", self.assurance_label)
        form_layout.addRow("", self.btn_assurance)
        form_layout.addRow("Optionnel:", self.optionnel_label)
        form_layout.addRow("", self.btn_optionnel)

        # Labels pour afficher le nombre de jours et total
        self.nb_jours_label = QLabel("Nombre de jours : 0")
        self.total_label = QLabel("Total : 0.00 $")
        form_layout.addRow(self.nb_jours_label)
        form_layout.addRow(self.total_label)

        # Boutons de navigation et action
        self.btn_annuler = QPushButton("❌ Annuler")
        self.btn_annuler.clicked.connect(self.retourner_arriere)

        self.btn_sauvegarder = QPushButton("💾 Sauvegarder pour plus tard")
        self.btn_sauvegarder.clicked.connect(self.sauvegarder_reservation)

        self.btn_confirmer = QPushButton("✅ Confirmer la réservation")
        self.btn_confirmer.clicked.connect(self.confirmer_reservation)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_annuler)
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

    # Méthodes d'affichage des tableaux
    def afficher_tableau_vehicules(self):
        donnees = lister_vehicules_disponibles()
        tableau = TableauVehiculesUI(
            "Liste des véhicules disponibles",
            ["ID", "Marque", "Modele", "Couleur", "Type carburant", "Type véhicule"],
            donnees,
            self.main_window,
            self
        )
        self.main_window.central_widget.addWidget(tableau)
        self.main_window.central_widget.setCurrentWidget(tableau)


    def afficher_tableau_tarifications(self):
        donnees = lister_toutes_tarifications()
        tableau = TableauTarificationsUI("Liste des tarifications", 
            ["ID", "KM/Jour", "Prix/Jour", "Type Véhicule"], donnees, self.main_window, self)
        self.main_window.central_widget.addWidget(tableau)
        self.main_window.central_widget.setCurrentWidget(tableau)

    def afficher_tableau_assurances(self):
        donnees = lister_toutes_assurances()
        tableau = TableauAssurancesUI("Liste des assurances", 
            ["ID", "Type", "Prix/Jour"], donnees, self.main_window, self)
        self.main_window.central_widget.addWidget(tableau)
        self.main_window.central_widget.setCurrentWidget(tableau)

    def afficher_tableau_optionnels(self):
        donnees = lister_tout_optionnels()
        tableau = TableauOptionnelsUI("Liste des optionnels", 
            ["ID", "Nom", "Prix/Jour"], donnees, self.main_window, self)
        self.main_window.central_widget.addWidget(tableau)
        self.main_window.central_widget.setCurrentWidget(tableau)

    # Calcul automatique du total
    def calculer_total(self):
        date_debut = self.date_debut_input.date()
        date_fin = self.date_fin_input.date()
        nb_jours = date_debut.daysTo(date_fin)
        if nb_jours <= 0:
            nb_jours = 1
        self.nb_jours_label.setText(f"Nombre de jours : {nb_jours}")

        prix_tarif = self.extraire_prix(self.tarif_label.text())
        prix_assurance = self.extraire_prix(self.assurance_label.text())
        prix_optionnel = self.extraire_prix(self.optionnel_label.text())

        total = (prix_tarif + prix_assurance + prix_optionnel) * nb_jours
        self.total_label.setText(f"Total : {total:.2f} $")

    def extraire_prix(self, label_text):
        match = re.search(r"([\d\.]+)\$", label_text)
        return float(match.group(1)) if match else 0.0

    def mettre_a_jour_date_fin(self):
        self.date_fin_input.setMinimumDate(self.date_debut_input.date())
        if self.date_fin_input.date() < self.date_debut_input.date():
            self.date_fin_input.setDate(self.date_debut_input.date())
        self.calculer_total()

    ################################# Boutons action #################################

    def retourner_arriere(self):
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_clients)

    def sauvegarder_reservation(self):
        if not self.id_client:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner ou créer un client avant de sauvegarder.")
            return

        date_debut = self.date_debut_input.date().toString("yyyy-MM-dd")
        date_fin = self.date_fin_input.date().toString("yyyy-MM-dd")
        self.id_reservation = ajouter_reservation_via_procedure(
            self.id_client, self.id_vehic, date_debut, date_fin, self.id_tarif, self.id_assurance, self.id_optio)

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
                self.id_client, self.id_vehic, date_debut, date_fin, self.id_tarif, self.id_assurance, self.id_optio)

            if not self.id_reservation:
                QMessageBox.warning(self, "Erreur", "La réservation n'a pas pu être créée pour confirmation.")
                return

        confirmer_reservation(self.id_reservation)
        QMessageBox.information(self, "Succès", f"Réservation confirmée (ID: {self.id_reservation}).")
