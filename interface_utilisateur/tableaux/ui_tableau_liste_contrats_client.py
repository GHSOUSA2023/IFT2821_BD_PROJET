from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from fonctions_gestion.contratclient import get_contrats_par_email, get_contrat_par_reservation, get_contrat_par_id_contract
from interface_utilisateur.tableaux.ui_tableau_contrat import TableauContratUI

class TableauListeContratsClientUI(QWidget):
    """ouvrir_contrat_selectionne
    Interface pour rechercher et afficher la liste des contrats d'un client par son e-mail.
    """
    def __init__(self, main_window, mode="client"):
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        self.email_client = None
        self.setWindowTitle("Recherche de contrats client")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Champ de recherche (e-mail)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Entrez l'adresse email du client")
        layout.addWidget(self.email_input)

        # Bouton de recherche
        self.btn_rechercher = QPushButton("🔎 Rechercher les contrats")
        self.btn_rechercher.clicked.connect(self.rechercher_contrats)
        layout.addWidget(self.btn_rechercher)

        # Tableau d'affichage des contrats
        self.tableau_contrats = QTableWidget()
        self.tableau_contrats.setColumnCount(10)
        self.tableau_contrats.setHorizontalHeaderLabels([
            "Nº reservation",
            "Nº contrat", 
            "Date début", 
            "Date fin",
            "Nombre de jours", 
            "Prix total",
            "Status du contrat",
            "Agence", 
            "Nom client", 
            "Véhicule"
        ])
        # Ajustement plus intelligent des colonnes :
        header = self.tableau_contrats.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   # Numéro du Contrat
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)   # Numéro du Contrat
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)   # Date début
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)   # Date fin
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)   # Nombre de jours
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)   # Prix total
        header.setSectionResizeMode(6, QHeaderView.Stretch)            # Agence (étirer)
        header.setSectionResizeMode(7, QHeaderView.Stretch)            # Agence (étirer)
        header.setSectionResizeMode(8, QHeaderView.Stretch)            # Nom Client (étirer)
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)   # Véhicule (ajusté au contenu)

        self.tableau_contrats.cellDoubleClicked.connect(self.ouvrir_contrat_selectionne)
        layout.addWidget(self.tableau_contrats)

        # Bouton retour
        self.btn_retour = QPushButton("🔙 Retour")
        self.btn_retour.clicked.connect(self.retourner)
        layout.addWidget(self.btn_retour)

        self.setLayout(layout)

    def rechercher_contrats(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un email.")
            return

        self.email_client = email # Mémoriser l'email pour rechargement

        contrats = get_contrats_par_email(email)
        self.tableau_contrats.setRowCount(0)

        if contrats:
            for index, contrat in enumerate(contrats):
                self.tableau_contrats.insertRow(index)
                self.tableau_contrats.setItem(index, 0, QTableWidgetItem(str(contrat.ID_RESERV)))
                self.tableau_contrats.setItem(index, 1, QTableWidgetItem(str(contrat.ID_CONTRACT)))
                self.tableau_contrats.setItem(index, 2, QTableWidgetItem(str(contrat.CONTRAT_DATE_DEBUT)))
                self.tableau_contrats.setItem(index, 3, QTableWidgetItem(str(contrat.CONTRAT_DATE_FIN)))
                self.tableau_contrats.setItem(index, 4, QTableWidgetItem(str(contrat.CONTRAT_DUREE_JOURS)))
                self.tableau_contrats.setItem(index, 5, QTableWidgetItem(str(contrat.CONTRAT_PRIX_TOTAL)))
                self.tableau_contrats.setItem(index, 6, QTableWidgetItem(str(contrat.STATUS)))
                self.tableau_contrats.setItem(index, 7, QTableWidgetItem(str(contrat.NOM_AGENCE)))
                self.tableau_contrats.setItem(index, 8, QTableWidgetItem(str(contrat.NOM_CLIENT)))
                self.tableau_contrats.setItem(index, 9, QTableWidgetItem(str(contrat.MODELE_VEHICULE)))

        else:
            QMessageBox.information(self, "Aucun contrat", "Aucun contrat trouvé pour cet email.")


    def ouvrir_contrat_selectionne(self, row, _column):
        try:
            status = self.tableau_contrats.item(row, 6).text()
            id_reserv = int(self.tableau_contrats.item(row, 0).text())

            if status == "EN ATTENTE":
                if self.mode == "client":
                    from interface_utilisateur.clients.gestion_reservations.ui_formulaire_reservation_gerir import FormulaireReservationGerirUI
                    formulaire_gerer = FormulaireReservationGerirUI(self.main_window, id_reserv)
                else:
                    from interface_utilisateur.agences.operations.reservations.ui_formulaire_reservation_gerer_oper import FormulaireReservationGerirOperUI
                    formulaire_gerer = FormulaireReservationGerirOperUI(self.main_window, id_reserv)

                formulaire_gerer.email_client = self.email_client
                self.main_window.central_widget.addWidget(formulaire_gerer)
                self.main_window.central_widget.setCurrentWidget(formulaire_gerer)
                return

            if status in ["CONFIRMEE", "TERMINEE"]:
                contrat_info = get_contrat_par_reservation(id_reserv)
                if contrat_info:
                    tableau_contrat = TableauContratUI(contrat_info, self.main_window, self)
                    self.main_window.central_widget.addWidget(tableau_contrat)
                    self.main_window.central_widget.setCurrentWidget(tableau_contrat)
                else:
                    QMessageBox.warning(self, "Erreur", "Impossible de récupérer les détails du contrat.")
            else:
                QMessageBox.warning(self, "Information", "⚠️ Le contrat n’est disponible que pour les réservations confirmées ou terminées.")
        except Exception as e:
            print(f"Erreur lors de l'ouverture du contrat ou du formulaire : {e}")
            QMessageBox.warning(self, "Erreur", "Problème lors de l'ouverture.")




    def recharger_tableau(self):
        if not self.email_client:
            QMessageBox.warning(self, "Erreur", "Recharger Aucun email de client mémorisé.")
            return

        contrats = get_contrats_par_email(self.email_client)
        self.tableau_contrats.setRowCount(0)

        if contrats:
            for index, contrat in enumerate(contrats):
                self.tableau_contrats.insertRow(index)
                self.tableau_contrats.setItem(index, 0, QTableWidgetItem(str(contrat.ID_RESERV)))
                self.tableau_contrats.setItem(index, 1, QTableWidgetItem(str(contrat.ID_CONTRACT)))
                self.tableau_contrats.setItem(index, 2, QTableWidgetItem(str(contrat.CONTRAT_DATE_DEBUT)))
                self.tableau_contrats.setItem(index, 3, QTableWidgetItem(str(contrat.CONTRAT_DATE_FIN)))
                self.tableau_contrats.setItem(index, 4, QTableWidgetItem(str(contrat.CONTRAT_DUREE_JOURS)))
                self.tableau_contrats.setItem(index, 5, QTableWidgetItem(str(contrat.CONTRAT_PRIX_TOTAL)))
                self.tableau_contrats.setItem(index, 6, QTableWidgetItem(str(contrat.STATUS)))
                self.tableau_contrats.setItem(index, 7, QTableWidgetItem(str(contrat.NOM_AGENCE)))
                self.tableau_contrats.setItem(index, 8, QTableWidgetItem(str(contrat.NOM_CLIENT)))
                self.tableau_contrats.setItem(index, 9, QTableWidgetItem(str(contrat.MODELE_VEHICULE)))
        else:
            QMessageBox.information(self, "Aucun contrat", "Recharger 2 Aucun contrat trouvé pour cet email.")


    def nettoyer_champs(self):
        """Efface le champ e-mail et le contenu du tableau."""
        self.email_input.clear()
        self.tableau_contrats.setRowCount(0)


    def retourner(self):
        self.nettoyer_champs()
        # Sinon, retour à l'interface clients
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_clients)

