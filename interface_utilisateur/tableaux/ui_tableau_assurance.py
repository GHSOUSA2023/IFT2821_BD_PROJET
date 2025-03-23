from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from fonctions_gestion.assurances import rechercher_assurance, lister_toutes_assurances

class TableauAssurancesUI(QWidget):
    """
    Interface générique pour afficher les assurances avec un champ de recherche.
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

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par type d'assurance...")
        self.search_input.textChanged.connect(self.filtrer_tableau)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)
        self.table_widget.cellDoubleClicked.connect(self.selectionner_ligne)


        self.charger_donnees(self.donnees)



        self.btn_retour = QPushButton("⬅ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        layout.addWidget(QLabel("Recherche Assurance:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.btn_retour)
        self.setLayout(layout)

    def charger_donnees(self, donnees):
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

        # Busca diretamente na base
        connexion = lister_toutes_assurances()
        assures_filtrees = [a for a in connexion if terme in a[1].lower()]
        self.charger_donnees(assures_filtrees)

    def selectionner_ligne(self, row, column):
        id_assurance = int(self.table_widget.item(row, 0).text())
        type_assurance = self.table_widget.item(row, 1).text()
        prix_jour = self.table_widget.item(row, 2).text()

        # Retour au formulaire et mise à jour
        self.retour_widget.id_assurance = id_assurance
        self.retour_widget.assurance_label.setText(
            f"Assurance : {type_assurance}, {prix_jour}$ / jour"
        )
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)
        self.retour_widget.calculer_total()



    def retourner(self):
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)