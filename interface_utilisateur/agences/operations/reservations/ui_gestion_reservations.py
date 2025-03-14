from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.reservations import (
    ajouter_reservation, modifier_reservation, supprimer_reservation,
    lister_toutes_reservations, rechercher_reservation, 
    afficher_liste_reservations_modifier, afficher_liste_reservations_supprimer
)
from interface_utilisateur.tableaux.ui_tableau_reservations import TableauReservationsUI
from interface_utilisateur.agences.operations.reservations.ui_formulaire_reservation import FormulaireReservationUI
from PyQt5.QtWidgets import QMessageBox

class GestionReservationsUI(QWidget):
    """
    Interface avancée pour la gestion des réservations.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Référence à la MainWindow
        self.setWindowTitle("Gestion des Réservations")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES RÉSERVATIONS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur (Card)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons
        btn_ajouter = QPushButton("➕ Nouvelle Réservation")
        btn_modifier = QPushButton("✏ Modifier une Réservation")
        btn_supprimer = QPushButton("🗑 Supprimer une Réservation")
        btn_lister = QPushButton("📋 Lister les Réservations")
        btn_rechercher = QPushButton("🔍 Rechercher une Réservation")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_reservations_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_reservations_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_reservations)
        btn_rechercher.clicked.connect(self.rechercher_reservation)
        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_gestion_operations))

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ------------------- Fonctions -------------------

    def ouvrir_formulaire_ajouter(self):
        """Ouvre le formulaire pour ajouter une nouvelle réservation."""
        self.formulaire_reservation = FormulaireReservationUI(self.main_window, mode="ajouter")
        self.main_window.central_widget.addWidget(self.formulaire_reservation)
        self.main_window.central_widget.setCurrentWidget(self.formulaire_reservation)

    def afficher_liste_reservations_modifier(self):
        """
        Affiche la liste des réservations avec option de modification.
        """
        colonnes, reservations = afficher_liste_reservations_modifier()

        if reservations:
            self.tableau_reservations_modifier = TableauReservationsUI("Modifier une Réservation", colonnes, reservations, self.main_window)
            self.tableau_reservations_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)
            self.main_window.central_widget.addWidget(self.tableau_reservations_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_reservations_modifier)

    def ouvrir_formulaire_modifier(self, row, column):
        """Ouvre le formulaire de modification lorsqu'une ligne est cliquée."""
        id_reserv = self.tableau_reservations_modifier.table_widget.item(row, 0).text()
        
        reservation_data = None
        for reservation in self.tableau_reservations_modifier.donnees:
            if reservation[0] == id_reserv:
                reservation_data = reservation
                break

        if reservation_data:
            self.formulaire_modification = FormulaireReservationUI(self.main_window, mode="modifier", reservation=reservation_data)
            self.main_window.central_widget.addWidget(self.formulaire_modification)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_modification)

    def afficher_liste_reservations_supprimer(self):
        """
        Affiche la liste des réservations dans le tableau avec possibilité de suppression.
        """
        colonnes, reservations = afficher_liste_reservations_supprimer()

        if reservations:
            self.tableau_reservations_supprimer = TableauReservationsUI("Supprimer une Réservation", colonnes, reservations, self.main_window)
            self.tableau_reservations_supprimer.table_widget.cellClicked.connect(self.confirmer_suppression)
            self.main_window.central_widget.addWidget(self.tableau_reservations_supprimer)
            self.main_window.central_widget.setCurrentWidget(self.tableau_reservations_supprimer)

    def confirmer_suppression(self, row, column):
        """
        Confirmation avant suppression d'une réservation.
        """
        id_reserv = self.tableau_reservations_supprimer.table_widget.item(row, 0).text()
        date_debut = self.tableau_reservations_supprimer.table_widget.item(row, 1).text()

        reponse = QMessageBox.question(
            None, 
            "Confirmation",
            f"Voulez-vous vraiment supprimer la réservation du {date_debut} ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            supprimer_reservation(id_reserv)
            print("Réservation supprimée avec succès !")
            self.tableau_reservations_supprimer.table_widget.removeRow(row)

    def afficher_liste_reservations(self):
        """
        Récupère toutes les réservations et les affiche dans le tableau TableauReservationsUI.
        """
        colonnes = ["ID", "Début", "Fin", "Statut", "Durée", "Client", "Véhicule", "Tarif", "Assurance", "Optionnel", "Prix Total"]
        reservations = lister_toutes_reservations()

        if reservations:
            self.tableau_reservations = TableauReservationsUI("Liste des Réservations", colonnes, reservations, self.main_window)
            self.main_window.central_widget.addWidget(self.tableau_reservations)
            self.main_window.central_widget.setCurrentWidget(self.tableau_reservations)

    def rechercher_reservation(self):
        """
        Affiche un champ de recherche et affiche les résultats dans le tableau.
        """
        from PyQt5.QtWidgets import QInputDialog

        terme, ok = QInputDialog.getText(self, "Recherche de Réservation", "Entrez un ID Client, ID Véhicule ou Date de Début:")
        
        if ok and terme.strip():
            colonnes, reservations = rechercher_reservation(terme.strip())

            if reservations:
                self.tableau_resultats_recherche = TableauReservationsUI(
                    "Résultats de la Recherche", colonnes, reservations, self.main_window
                )
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Résultat", "Aucune réservation trouvée.")

