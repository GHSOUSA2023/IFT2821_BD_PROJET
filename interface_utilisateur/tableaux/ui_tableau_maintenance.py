from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from fonctions_gestion.flotte import rechercher_maintenance  # Fonction de recherche maintenance

class TableauMaintenanceUI(QWidget):
    """
    Interface générique pour afficher les maintenances avec un champ de recherche.
    """
    def __init__(self, titre, colonnes, donnees, main_window):
        super().__init__()
        self.setWindowTitle(titre)
        self.main_window = main_window  # Référence au MainWindow
        self.colonnes = colonnes
        self.donnees = donnees
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Champ de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par type de maintenance ou ID véhicule...")
        self.search_input.textChanged.connect(self.filtrer_tableau)

        # Tableau
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)

        self.charger_donnees(self.donnees)

        #  Bouton retour
        self.btn_retour = QPushButton("⬅️ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        #  Ajout au layout
        layout.addWidget(QLabel("Recherche Maintenance :"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.btn_retour)
        self.setLayout(layout)

    def charger_donnees(self, donnees):
        """Charge les données dans le tableau."""
        self.table_widget.setRowCount(len(donnees))
        for row, ligne in enumerate(donnees):
            for col, valeur in enumerate(ligne):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(valeur)))
                self.table_widget.resizeColumnsToContents()

    def filtrer_tableau(self):
        """Filtre le tableau selon la recherche."""
        terme = self.search_input.text().strip().lower()
        
        if not terme:
            self.charger_donnees(self.donnees)  # Réinitialiser si champ vide
            return
        
        colonnes, maintenances_filtrees = rechercher_maintenance(terme)
        self.charger_donnees(maintenances_filtrees)

    def retourner(self):
        """Retourne à l'écran de gestion de flotte."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_flotte)
