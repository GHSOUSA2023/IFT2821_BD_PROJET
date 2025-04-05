from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QDateTime
from fonctions_gestion.vehicules import rechercher_vehicule, get_vehicule_par_id, lister_tous_vehicules
from fonctions_gestion.flotte import lister_vehicules_en_maintenance
from interface_utilisateur.agences.operations.maintenance.ui_formulaire_maintenance_gerer import FormulaireMaintenanceGererUI


class TableauVehiculesMaintUI(QWidget):
    """
    Interface pour afficher les véhicules avec un champ de recherche et double-clic pour modifier.
    """
    def __init__(self, titre, colonnes, donnees, main_window, retour_widget):
        super().__init__()
        self.main_window = main_window
        self.retour_widget = retour_widget
        self.setWindowTitle(titre)
        self.colonnes = colonnes
        self.donnees = donnees
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        #Champ de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par immatriculation ou modèle...")
        self.search_input.textChanged.connect(self.filtrer_tableau)

        #Tableau des véhicules
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)
        self.table_widget.cellDoubleClicked.connect(self.ouvrir_selec_formulaire_modification)

        self.charger_donnees(self.donnees)

        #Bouton retour
        self.btn_retour = QPushButton("⬅ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        #Ajout au layout
        layout.addWidget(QLabel("Recherche Véhicule:"))
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

        colonnes, vehicules_filtres = rechercher_vehicule(terme)
        self.charger_donnees(vehicules_filtres)


    def ouvrir_selec_formulaire_modification(self, row, column):
        """
        Ouvre le formulaire de maintenance lorsqu'une ligne est double-cliquée.
        """
        id_vehicule = self.table_widget.item(row, 0).text()

        formulaire_maintenance = FormulaireMaintenanceGererUI(
            self.main_window,
            id_vehicule,
            self
        )
        self.main_window.central_widget.addWidget(formulaire_maintenance)
        self.main_window.central_widget.setCurrentWidget(formulaire_maintenance)


    def tb_mt_recharger_tableau(self):
        """Recharge les données du tableau."""
        vehicules = lister_vehicules_en_maintenance()
        self.charger_donnees(vehicules)


    def retourner(self):
        """Retourne à l'écran précédent."""
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)
