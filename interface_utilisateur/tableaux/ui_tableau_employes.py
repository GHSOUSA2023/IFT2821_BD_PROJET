from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt

class TableauEmployesUI(QWidget):
    """
    Interface générique (mais nommée pour agences) pour afficher le tableau
    dans le même QStackedWidget, sans ouvrir de nouvelle fenêtre.
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

        # Création du QTableWidget
        from PyQt5.QtWidgets import QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)

        self.charger_donnees(self.donnees)

        # Bouton retour
        self.btn_retour = QPushButton("⬅ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        layout.addWidget(self.table_widget)
        layout.addWidget(self.btn_retour)
        self.setLayout(layout)

    def charger_donnees(self, donnees):
        """Charge correctement les données dans le tableau."""
        self.table_widget.setRowCount(len(donnees))
        for row, ligne in enumerate(donnees):
            for col, valeur in enumerate(ligne):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(valeur)))
                self.table_widget.resizeColumnsToContents()  # Ajuste automatique des colonnes



    def retourner(self):
        """
        Retourne à l'écran de gestion des agences (ui_gestion_agences)
        dans le QStackedWidget.
        """
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_employes)
