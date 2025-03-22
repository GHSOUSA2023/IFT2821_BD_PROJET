import re
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QDateEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDateEdit, QApplication
from PyQt5.QtCore import Qt, QTimer, QDate
from interface_utilisateur.clients.reservations.ui_formulaire_client import FormulaireClientUI
from fonctions_gestion.clients import rechercher_client_par_email, ajouter_client, get_client_par_id
from fonctions_gestion.reservations import ajouter_reservation_via_procedure, confirmer_reservation, get_reservation_par_id, annuler_reservation
from fonctions_gestion.vehicules import lister_tous_vehicules, lister_vehicules_disponibles, get_vehicule_par_id
from fonctions_gestion.tarifications import lister_toutes_tarifications, get_tarif_par_id
from fonctions_gestion.assurances import lister_toutes_assurances, get_assurance_par_id
from fonctions_gestion.optionnels import lister_tout_optionnels, get_optionnel_par_id
from fonctions_gestion.contratclient import get_contrat_par_reservation
from interface_utilisateur.tableaux.ui_tableau_assurance import TableauAssurancesUI
from interface_utilisateur.tableaux.ui_tableau_optionnel import TableauOptionnelsUI
from interface_utilisateur.tableaux.ui_tableau_tarifications import TableauTarificationsUI
from interface_utilisateur.tableaux.ui_tableau_vehicules import TableauVehiculesUI
from interface_utilisateur.tableaux.ui_tableau_contrat import TableauContratUI



# Classe personnalisée pour afficher automatiquement le calendrier au focus
class CustomDateEdit(QDateEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.ouvrir_calendrier)

    def ouvrir_calendrier(self):
        # Simuler Alt + Down pour ouvrir le calendrier
        event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Down, Qt.AltModifier)
        QApplication.postEvent(self, event)

class FormulaireReservationGerirUI(QWidget):

    def __init__(self, main_window, id_reservation=None):
        super().__init__()
        self.main_window = main_window
        self.ui_tableau_liste_contrats_client = self.main_window.ui_tableau_liste_contrats_client
        self.email_client = None
        self.id_client = None
        self.id_reservation = id_reservation
        self.id_vehic = None
        self.id_tarif = None
        self.id_assurance = None
        self.id_optio = None
        self.setWindowTitle("Gérer une réservation")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()
        if self.id_reservation:
            self.charger_reservation(self.id_reservation)

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

        # Date de fin — on initialise avec date debut + 1
        date_min_fin = self.date_debut_input.date().addDays(1)
        self.date_fin_input = CustomDateEdit()
        self.date_fin_input.setDate(date_min_fin)
        self.date_fin_input.setMinimumDate(date_min_fin)
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

        self.btn_annuler = QPushButton("🚫 Annuler la réservation")
        self.btn_annuler.clicked.connect(self.annuler_reservation)

        self.btn_sauvegarder = QPushButton("💾 Sauvegarder pour plus tard")
        self.btn_sauvegarder.clicked.connect(self.sauvegarder_reservation)

        self.btn_confirmer = QPushButton("✅ Confirmer la réservation")
        self.btn_confirmer.clicked.connect(self.confirmer_reservation)

        self.btn_retour = QPushButton("🔙 Retour")
        self.btn_retour.clicked.connect(self.retourner_arriere)


        layout.addLayout(form_layout)
        layout.addWidget(self.btn_annuler)
        layout.addWidget(self.btn_sauvegarder)
        layout.addWidget(self.btn_confirmer)
        layout.addWidget(self.btn_retour)
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
        date_min_fin = self.date_debut_input.date().addDays(1)
        self.date_fin_input.setMinimumDate(date_min_fin)
        self.date_fin_input.setDate(date_min_fin)
        self.calculer_total()

    def charger_reservation(self, id_reservation):
        reservation = get_reservation_par_id(id_reservation)
        if reservation:
            # Remplir les infos client
            self.id_client = reservation['ID_CLIENT']
            self.email_input.setText(str(reservation['EMAIL_CLIENT']))
            self.nom_label.setText(str(reservation['NOM_CLIENT']))
            self.prenom_label.setText(str(reservation['PRENOM_CLIENT']))
            self.adresse_label.setText(str(reservation['ADRESSE_CLIENT']))
            self.ville_label.setText(str(reservation['VILLE_CLIENT']))
            self.telephone_label.setText(str(reservation['TELEPHONE_CLIENT']))

            # Remplir les dates
            date_debut = QDate.fromString(str(reservation['DATE_DEBUT']), "yyyy-MM-dd")
            date_fin = QDate.fromString(str(reservation['DATE_FIN']), "yyyy-MM-dd")
            self.date_debut_input.setDate(date_debut)
            self.date_fin_input.setDate(date_fin)

            # Remplir les IDs
            self.id_vehic = reservation['ID_VEHIC']
            self.id_tarif = reservation['ID_TARIF']
            self.id_assurance = reservation['ID_ASSURANCE']
            self.id_optio = reservation['ID_OPTIO']

            # Véhicule
            vehicule_info = get_vehicule_par_id(self.id_vehic)
            if vehicule_info:
                self.vehicule_label.setText(
                    f"{vehicule_info['MARQUE']} {vehicule_info['MODELE']}, "
                    f"{vehicule_info['COULEUR']}, carburant: {vehicule_info['TYPE_CARBUR']}, "
                    f"type: {vehicule_info['TYPE_VEHIC']}"
                )
            else:
                self.vehicule_label.setText(f"Véhicule sélectionné (ID: {self.id_vehic})")

            # Tarif
            tarif_info = get_tarif_par_id(self.id_tarif)
            if tarif_info:
                self.tarif_label.setText(
                    f"{tarif_info['KM_JOUR']} km/jour, {tarif_info['PRIX_LOCAT_JOUR']:.2f}$ /jour "
                    f"({tarif_info['TYPE_VEHIC']})"
                )
            else:
                self.tarif_label.setText(f"Tarif sélectionné (ID: {self.id_tarif})")

            # Assurance
            assurance_info = get_assurance_par_id(self.id_assurance)
            if assurance_info:
                self.assurance_label.setText(
                    f"{assurance_info['TYPE_ASSURANCE']}, {assurance_info['PRIX_JOUR']:.2f}$ /jour"
                )
            else:
                self.assurance_label.setText(f"Assurance sélectionnée (ID: {self.id_assurance})")

            # Optionnel
            optionnel_info = get_optionnel_par_id(self.id_optio)
            if optionnel_info:
                self.optionnel_label.setText(
                    f"{optionnel_info['NOM_OPTIO']}, {optionnel_info['PRIX_OPTIO_JOUR']:.2f}$ /jour"
                )
            else:
                self.optionnel_label.setText(f"Optionnel sélectionné (ID: {self.id_optio})")

            # Recalculer le total
            self.calculer_total()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de charger la réservation.")


    ################################# Boutons action #################################

    def reinitialiser_formulaire(self):
        self.email_input.clear()
        self.nom_label.setText("")
        self.prenom_label.setText("")
        self.adresse_label.setText("")
        self.ville_label.setText("")
        self.telephone_label.setText("")

        self.date_debut_input.setDate(QDate.currentDate())
        self.date_fin_input.setDate(QDate.currentDate().addDays(1))

        self.vehicule_label.setText("Aucun véhicule sélectionné")
        self.tarif_label.setText("Aucun tarif sélectionné")
        self.assurance_label.setText("Aucune assurance sélectionnée")
        self.optionnel_label.setText("Aucune option sélectionnée")

        self.id_client = None
        self.id_reservation = None
        self.id_vehic = None
        self.id_tarif = None
        self.id_assurance = None
        self.id_optio = None

        self.nb_jours_label.setText("Nombre de jours : 0")
        self.total_label.setText("Total : 0.00 $")

    def sauvegarder_reservation(self):
        if not self.id_client:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner ou créer un client avant de sauvegarder.")
            return

        date_debut = self.date_debut_input.date().toString("yyyy-MM-dd")
        date_fin = self.date_fin_input.date().toString("yyyy-MM-dd")
        prix_tarif = self.extraire_prix(self.tarif_label.text())
        prix_assurance = self.extraire_prix(self.assurance_label.text())
        prix_optionnel = self.extraire_prix(self.optionnel_label.text())
        nb_jours = self.date_debut_input.date().daysTo(self.date_fin_input.date())
        if nb_jours <= 0:
            nb_jours = 1
        prix_total = (prix_tarif + prix_assurance + prix_optionnel) * nb_jours

        if not self.id_reservation:
            # INSERT
            self.id_reservation = ajouter_reservation_via_procedure(
                self.id_client, self.id_vehic, date_debut, date_fin,
                self.id_tarif, self.id_assurance, self.id_optio
            )
        else:
            # UPDATE
            from fonctions_gestion.reservations import modifier_reservation
            modifier_reservation(
                self.id_reservation, date_debut, date_fin, "EN ATTENTE", 
                self.id_vehic, self.id_tarif, 
                self.id_assurance, self.id_optio
            )

        if self.id_reservation:
            QMessageBox.information(self, "Succès", f"Réservation sauvegardée (ID: {self.id_reservation}, statut : EN ATTENTE).")
        else:
            QMessageBox.warning(self, "Erreur", "La réservation n'a pas pu être sauvegardée.")

    def confirmer_reservation(self):
        print("➡ Début de la confirmation de la réservation.")

        if not self.id_reservation:
            QMessageBox.warning(self, "Erreur", "Aucune réservation à confirmer.")
            return

        # Atualizar a reserva com status CONFIRMEE
        date_debut = self.date_debut_input.date().toString("yyyy-MM-dd")
        date_fin = self.date_fin_input.date().toString("yyyy-MM-dd")
        prix_tarif = self.extraire_prix(self.tarif_label.text())
        prix_assurance = self.extraire_prix(self.assurance_label.text())
        prix_optionnel = self.extraire_prix(self.optionnel_label.text())
        nb_jours = self.date_debut_input.date().daysTo(self.date_fin_input.date())
        if nb_jours <= 0:
            nb_jours = 1
        prix_total = (prix_tarif + prix_assurance + prix_optionnel) * nb_jours

        from fonctions_gestion.reservations import modifier_reservation
        modifier_reservation(
            self.id_reservation, date_debut, date_fin, "CONFIRMEE",
            self.id_vehic, self.id_tarif, self.id_assurance, self.id_optio
        )

        print(f"➡ Confirmation de la réservation ID: {self.id_reservation}")
        QMessageBox.information(self, "Succès", f"Réservation confirmée (ID: {self.id_reservation}).")

        print("➡ Tentative de récupération du contrat associé...")
        contrat_info = get_contrat_par_reservation(self.id_reservation)
        if not contrat_info:
            print("⏳ Attente de 2 secondes avant une deuxième tentative...")
            time.sleep(2)
            contrat_info = get_contrat_par_reservation(self.id_reservation)

        if contrat_info:
            print("✅ Contrat récupéré avec succès après attente, ouverture du tableau contrat.")
            self.reinitialiser_formulaire()
            tableau_contrat = TableauContratUI(contrat_info, self.main_window, self)
            self.main_window.central_widget.addWidget(tableau_contrat)
            self.main_window.central_widget.setCurrentWidget(tableau_contrat)
        else:
            print("❌ Aucun contrat trouvé même après une deuxième tentative.")
            QMessageBox.warning(self, "Erreur", "Le contrat n'a pas pu être récupéré.")


    def annuler_reservation(self):
        if not self.id_reservation:
            QMessageBox.warning(self, "Erreur", "Aucune réservation sélectionnée à annuler.")
            return

        confirmation = QMessageBox.question(
            self, 
            "Confirmation", 
            f"Voulez-vous vraiment annuler la réservation ID {self.id_reservation} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            from fonctions_gestion.reservations import annuler_reservation
            annuler_reservation(self.id_reservation)
            QMessageBox.information(self, "Succès", "Réservation annulée avec succès.")
            self.reinitialiser_formulaire()
            self.retourner_arriere()

    def retourner_arriere(self):
        if hasattr(self.main_window, 'ui_tableau_liste_contrats_client'):
            self.main_window.central_widget.setCurrentWidget(self.main_window.ui_tableau_liste_contrats_client)

            # Auto-remplir l'email et lancer la recherche
            if self.email_client:
                self.main_window.ui_tableau_liste_contrats_client.email_input.setText(self.email_client)
                self.main_window.ui_tableau_liste_contrats_client.rechercher_contrats()
        else:
            self.main_window.central_widget.setCurrentWidget(self.main_window.ui_clients)

