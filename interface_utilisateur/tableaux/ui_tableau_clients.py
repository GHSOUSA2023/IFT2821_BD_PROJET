from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from fonctions_gestion.clients import rechercher_client, lister_tous_clients
from interface_utilisateur.agences.clients.ui_formulaire_client_gerer import FormulaireClientGererUI


class TableauClientsUI(QWidget):
    """
    Tableau des clients avec recherche, double-clic pour modification et retour à la gestion.
    """

    def __init__(self, titre, colonnes, donnees, main_window):
        super().__init__()
        self.setWindowTitle(titre)
        self.main_window = main_window
        self.colonnes = colonnes
        self.donnees = donnees
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par Nom ou Email...")
        self.search_input.textChanged.connect(self.filtrer_tableau)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)
        self.table_widget.cellDoubleClicked.connect(self.ouvrir_formulaire_client)

        self.charger_donnees(self.donnees)

        self.btn_retour = QPushButton("⬅️ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        layout.addWidget(QLabel("Recherche Client:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.btn_retour)
        self.setLayout(layout)

    def charger_donnees(self, donnees):
        self.donnees = donnees
        self.table_widget.setRowCount(len(donnees))
        for row, ligne in enumerate(donnees):
            for col, valeur in enumerate(ligne):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(valeur)))
        self.table_widget.resizeColumnsToContents()

    def filtrer_tableau(self):
        terme = self.search_input.text().strip().lower()
        if not terme:
            self.charger_donnees(self.donnees)
            return

        colonnes, clients_filtres = rechercher_client(terme)
        self.donnees = clients_filtres
        self.charger_donnees(clients_filtres)

    def ouvrir_formulaire_client(self, row, column):
        """Ouvre le formulaire pour modifier un client existant avec toutes ses données."""
        id_client = self.table_widget.item(row, 0).text()

        from fonctions_gestion.clients import get_client_par_id
        client = get_client_par_id(id_client)

        if client:
            formulaire = FormulaireClientGererUI(parent=self)
            formulaire.set_info_client_complet(client)
            self.main_window.central_widget.addWidget(formulaire)
            self.main_window.central_widget.setCurrentWidget(formulaire)
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erreur", "Impossible de récupérer les données du client.")


    def retourner(self):
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_clients)
