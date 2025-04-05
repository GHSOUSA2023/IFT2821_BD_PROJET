from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from fonctions_gestion.tarifications import rechercher_tarification  # Import de la fonction de recherche

class TableauTarificationsUI(QWidget):
    """
    Interface générique pour afficher les tarifications avec un champ de recherche.
    """
    def __init__(self, titre, colonnes, donnees, main_window, retour_widget):
        super().__init__()
        self.main_window = main_window  # Référence au MainWindow
        self.retour_widget = retour_widget  # Widget de retour
        self.setWindowTitle(titre)
        self.colonnes = colonnes
        self.donnees = donnees
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Champ de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par Prix ou Type de Véhicule...")
        self.search_input.textChanged.connect(self.filtrer_tableau)


        # Tableau
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)
        self.table_widget.cellDoubleClicked.connect(self.selectionner_ligne)


        self.charger_donnees(self.donnees)

        # Bouton retour
        self.btn_retour = QPushButton("⬅️ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        # Ajout au layout
        layout.addWidget(QLabel("Recherche Tarification:"))
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
        
        colonnes, tarifications_filtres = rechercher_tarification(terme)
        self.charger_donnees(tarifications_filtres)

    def selectionner_ligne(self, row, column):
        id_tarif = int(self.table_widget.item(row, 0).text())
        km_jour = self.table_widget.item(row, 1).text()
        prix_jour = self.table_widget.item(row, 2).text()
        type_vehic = self.table_widget.item(row, 3).text()
        self.retour_widget.calculer_total()


        # Retourner au formulaire et mettre à jour
        self.retour_widget.id_tarif = id_tarif
        self.retour_widget.tarif_label.setText(
            f"Tarif sélectionné : {km_jour} km/jour, {prix_jour}$ /jour ({type_vehic})"
        )
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)


    def retourner(self):
        """Retourne à l'écran de gestion des tarifications."""
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)