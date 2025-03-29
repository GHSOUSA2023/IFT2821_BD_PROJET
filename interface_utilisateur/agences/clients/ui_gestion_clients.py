from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.clients import (
    ajouter_client, modifier_client, supprimer_client,
    lister_tous_clients, rechercher_client, afficher_liste_clients_modifier,
    afficher_liste_clients_supprimer
)
from interface_utilisateur.tableaux.ui_tableau_liste_contrats_client import TableauListeContratsClientUI
from interface_utilisateur.agences.clients.ui_formulaire_clients import FormulaireClientUI
from interface_utilisateur.clients.reservations.ui_formulaire_client import FormulaireClientUI
from interface_utilisateur.tableaux.ui_tableau_liste_contrats_client import TableauListeContratsClientUI


class GestionClientsUI(QWidget):
    """
    Interface pour la gestion des clients.
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Gestion des Clients")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES CLIENTS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur principal
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons
        btn_ajouter = QPushButton("➕ Ajouter un Client")
        btn_modifier = QPushButton("✏ Modifier un Client")
        btn_supprimer = QPushButton("🗑 Supprimer un Client")
        btn_lister = QPushButton("📋 Lister les Clients")
        btn_rechercher = QPushButton("🔍 Rechercher un Client")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_clients_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_clients_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_clients)
        btn_rechercher.clicked.connect(self.rechercher_client)
        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_agences))

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ------------------- Fonctions de gestion des clients -------------------

    def ouvrir_formulaire_ajouter(self):
        """
        Ouvre le formulaire pour ajouter un nouveau client.
        """
        self.formulaire_client = FormulaireClientUI(self.main_window, mode="ajouter")
        self.main_window.central_widget.addWidget(self.formulaire_client)
        self.main_window.central_widget.setCurrentWidget(self.formulaire_client)

    def afficher_liste_clients_modifier(self):
        """
        Affiche la liste des clients avec option de modification.
        """
        colonnes, clients = afficher_liste_clients_modifier()

        if clients:
            self.tableau_clients_modifier = TableauClientsUI("Modifier un Client", colonnes, clients, self.main_window)

            # Connecter le clic sur une ligne à l'ouverture du formulaire de modification
            self.tableau_clients_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)

            self.main_window.central_widget.addWidget(self.tableau_clients_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_clients_modifier)

    def ouvrir_formulaire_modifier(self, row, column):
        """
        Ouvre le formulaire de modification lorsqu'un client est sélectionné.
        """
        id_client = self.tableau_clients_modifier.table_widget.item(row, 0).text()  # ID du client sélectionné

        # Récupérer les données du client sélectionné
        client_data = None
        for client in self.tableau_clients_modifier.donnees:
            if client[0] == id_client:
                client_data = client
                break

        if client_data:
            self.formulaire_modification = FormulaireClientUI(self.main_window, mode="modifier", client=client_data)
            self.main_window.central_widget.addWidget(self.formulaire_modification)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_modification)

    def afficher_liste_clients_supprimer(self):
        """
        Affiche la liste des clients avec option de suppression.
        """
        colonnes, clients = afficher_liste_clients_supprimer()

        if clients:
            self.tableau_clients_supprimer = TableauClientsUI("Supprimer un Client", colonnes, clients,
                                                              self.main_window)

            # Connecter le clic à l'ouverture de la confirmation de suppression
            self.tableau_clients_supprimer.table_widget.cellClicked.connect(self.confirmer_suppression)

            self.main_window.central_widget.addWidget(self.tableau_clients_supprimer)
            self.main_window.central_widget.setCurrentWidget(self.tableau_clients_supprimer)

    def confirmer_suppression(self, row, column):
        """
        Demande confirmation avant suppression d'un client.
        """
        id_client = self.tableau_clients_supprimer.table_widget.item(row, 0).text()
        nom_client = self.tableau_clients_supprimer.table_widget.item(row, 1).text()  # Par exemple, le nom du client

        # Boîte de confirmation
        reponse = QMessageBox.question(
            None,
            "Confirmation",
            f"Souhaitez-vous réellement supprimer le client '{nom_client}' ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            # Supprimer le client
            supprimer_client(id_client)
            print("Client supprimé avec succès!")

            # Retirer le client de la liste
            self.tableau_clients_supprimer.table_widget.removeRow(row)

    def afficher_liste_clients(self):
        """
        Récupère tous les clients et les affiche dans le tableau `TableauClientsUI`.
        """
        # Vous pouvez adapter les colonnes en fonction des informations clients disponibles
        colonnes = ["ID", "Nom", "Prénom", "Email", "Téléphone"]
        clients = lister_tous_clients()

        if clients:
            self.tableau_clients = TableauClientsUI("Liste des Clients", colonnes, clients, self.main_window)
            self.main_window.central_widget.addWidget(self.tableau_clients)
            self.main_window.central_widget.setCurrentWidget(self.tableau_clients)

    def rechercher_client(self):
        """
        Affiche un champ de recherche et affiche les résultats dans le tableau.
        """
        from PyQt5.QtWidgets import QInputDialog, QMessageBox
        from fonctions_gestion.clients import rechercher_client
        from interface_utilisateur.tableaux.ui_tableau_clients import TableauClientsUI

        # Demande à l'utilisateur de saisir un terme de recherche
        terme, ok = QInputDialog.getText(self, "Recherche de Client", "Entrez un nom ou un email:")

        if ok and terme.strip():
            # Récupérer les résultats
            colonnes, clients = rechercher_client(terme.strip())

            if clients:
                self.tableau_resultats_recherche = TableauClientsUI(
                    "Résultats de la Recherche", colonnes, clients, self.main_window
                )
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                QMessageBox.information(self, "Résultat", "Aucun client trouvé.")
