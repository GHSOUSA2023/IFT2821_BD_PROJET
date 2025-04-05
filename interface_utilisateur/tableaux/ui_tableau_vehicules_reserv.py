from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from fonctions_gestion.vehicules import get_vehicule_par_id


class TableauVehiculesUI(QWidget):
    """
    Tableau pour afficher les véhicules disponibles avec recherche et retour au formulaire de réservation.
    """
    def __init__(self, titre, colonnes, donnees, main_window, retour_widget):
        super().__init__()
        self.titre = titre
        self.colonnes = colonnes
        self.donnees = donnees
        self.main_window = main_window
        self.retour_widget = retour_widget  # Widget qui recevra les données sélectionnées
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titre
        label_titre = QLabel(self.titre)
        label_titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_titre)

        # Champ de recherche
        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText("🔍 Rechercher un véhicule...")
        self.champ_recherche.textChanged.connect(self.filtrer_tableau)
        layout.addWidget(self.champ_recherche)

        # Tableau
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.colonnes))
        self.table_widget.setHorizontalHeaderLabels(self.colonnes)
        self.table_widget.cellDoubleClicked.connect(self.ouvrir_selec_formulaire_modification)
        self.charger_donnees(self.donnees)
        layout.addWidget(self.table_widget)

        # Bouton de retour
        btn_retour = QPushButton("⬅️ Retour")
        btn_retour.clicked.connect(self.retourner)
        layout.addWidget(btn_retour)

        self.setLayout(layout)

    def charger_donnees(self, donnees):
        """Charge les données dans le tableau."""
        self.table_widget.setRowCount(len(donnees))
        for ligne, valeurs in enumerate(donnees):
            for col, valeur in enumerate(valeurs):
                item = QTableWidgetItem(str(valeur))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setItem(ligne, col, item)
        self.table_widget.resizeColumnsToContents()

    def filtrer_tableau(self):
        """Filtre les lignes du tableau en fonction du terme de recherche."""
        terme = self.champ_recherche.text().lower()
        if not terme:
            self.charger_donnees(self.donnees)
            return
        resultats = [
            ligne for ligne in self.donnees
            if any(terme in str(valeur).lower() for valeur in ligne)
        ]
        self.charger_donnees(resultats)

    def ouvrir_selec_formulaire_modification(self, row, column):
        """
        Lors d’un double-clic, envoie toutes les infos du véhicule sélectionné au formulaire.
        """
        id_vehic = self.table_widget.item(row, 0).text()
        marque = self.table_widget.item(row, 1).text()
        modele = self.table_widget.item(row, 2).text()
        couleur = self.table_widget.item(row, 3).text()
        carburant = self.table_widget.item(row, 4).text()
        type_vehic = self.table_widget.item(row, 5).text()

        # Appel au formulaire avec les données complètes
        if hasattr(self.retour_widget, "set_info_vehicule"):
            self.retour_widget.set_info_vehicule([
                id_vehic, marque, modele, couleur, carburant, type_vehic
            ])
            self.main_window.central_widget.setCurrentWidget(self.retour_widget)


    def retourner(self):
        """
        Retourne au widget précédent (formulaire de réservation).
        """
        if self.retour_widget:
            self.main_window.central_widget.setCurrentWidget(self.retour_widget)

