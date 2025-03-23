from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from fonctions_gestion.optionnels import rechercher_optionnel, lister_tout_optionnels

class TableauOptionnelsUI(QWidget):
    """
    Interface générique pour afficher les optionnels avec un champ de recherche.
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

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par nom d'optionnel...")
        self.search_input.textChanged.connect(self.filtrer_tableau)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)
        self.table_widget.cellDoubleClicked.connect(self.selectionner_ligne)


        self.charger_donnees(self.donnees)

        self.btn_retour = QPushButton("⬅ Retour")
        self.btn_retour.clicked.connect(self.retourner)

        layout.addWidget(QLabel("Recherche Optionnel:"))
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

        optionnels = lister_tout_optionnels()
        optionnels_filtrees = [opt for opt in optionnels if terme in opt[1].lower()]
        self.charger_donnees(optionnels_filtrees)

    def selectionner_ligne(self, row, column):
        id_optionnel = int(self.table_widget.item(row, 0).text())
        nom_optionnel = self.table_widget.item(row, 1).text()
        prix_jour = self.table_widget.item(row, 2).text()

        # Retour au formulaire et mise à jour
        self.retour_widget.id_optio = id_optionnel
        self.retour_widget.optionnel_label.setText(
            f"Optionnel : {nom_optionnel}, {prix_jour}$ / jour"
        )
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)
        self.retour_widget.calculer_total()



    def retourner(self):
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)