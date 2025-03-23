from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from fonctions_gestion.reservations import rechercher_reservation, lister_toutes_reservations
from fonctions_gestion.contratclient import get_contrat_par_reservation
from interface_utilisateur.tableaux.ui_tableau_contrat import TableauContratUI

class TableauReservationsUI(QWidget):
    """
    Interface pour rechercher et afficher la liste des réservations avec possibilité d'ouverture des détails.
    """
    def __init__(self, titre, colonnes, donnees, main_window, mode="oper", retour_widget=None):
        super().__init__()
        self.setWindowTitle(titre)
        self.main_window = main_window
        self.colonnes = colonnes
        self.donnees = donnees
        self.mode = mode
        self.retour_widget = retour_widget
        self.terme_recherche = None  # Mémoriser la dernière recherche
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Champ de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par Nom du Client, nº contrat ou nº réservation ...")
        self.search_input.textChanged.connect(self.filtrer_tableau)
        layout.addWidget(QLabel("Recherche réservation :"))
        layout.addWidget(self.search_input)

        # Tableau d'affichage des réservations
        self.tableau_reservations = QTableWidget()
        self.tableau_reservations.setColumnCount(len(self.colonnes))
        self.tableau_reservations.setHorizontalHeaderLabels(self.colonnes)

        header = self.tableau_reservations.horizontalHeader()
        for i in range(len(self.colonnes)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.tableau_reservations.cellDoubleClicked.connect(self.ouvrir_contrat_selectionne)
        layout.addWidget(self.tableau_reservations)

        self.charger_donnees(self.donnees)

        # Bouton retour
        self.btn_retour = QPushButton("🔙 Retour")
        self.btn_retour.clicked.connect(self.retourner)
        layout.addWidget(self.btn_retour)

        self.setLayout(layout)

    def charger_donnees(self, donnees):
        """Charge les données dans le tableau."""
        self.tableau_reservations.setRowCount(0)
        for index, ligne in enumerate(donnees):
            self.tableau_reservations.insertRow(index)
            for col, valeur in enumerate(ligne):
                self.tableau_reservations.setItem(index, col, QTableWidgetItem(str(valeur)))
        self.tableau_reservations.resizeColumnsToContents()

    def filtrer_tableau(self):
        """Filtre le tableau selon la recherche."""
        terme = self.search_input.text().strip().lower()
        self.terme_recherche = terme  # Mémorise le terme de recherche
        if not terme:
            colonnes, reservations = lister_toutes_reservations()
            self.charger_donnees(reservations)
            return

        colonnes, reservations_filtres = rechercher_reservation(terme)
        self.charger_donnees(reservations_filtres)

    def recharger_tableau(self):
        """Recharge les données avec la dernière recherche ou la liste complète."""
        if self.terme_recherche:
            colonnes, reservations_filtres = rechercher_reservation(self.terme_recherche)
            self.charger_donnees(reservations_filtres)
        else:
            colonnes, reservations = lister_toutes_reservations()
            self.charger_donnees(reservations)

    def ouvrir_contrat_selectionne(self, row, _column):
        try:
            status = self.tableau_reservations.item(row, 6).text()
            id_reserv = int(self.tableau_reservations.item(row, 0).text())

            if status == "EN ATTENTE":
                if self.mode == "client":
                    from interface_utilisateur.clients.gestion_reservations.ui_formulaire_reservation_gerir import FormulaireReservationGerirUI
                    formulaire_gerer = FormulaireReservationGerirUI(self.main_window, id_reserv)
                else:
                    from interface_utilisateur.agences.operations.reservations.ui_formulaire_reservation_gerer_oper import FormulaireReservationGerirOperUI
                    formulaire_gerer = FormulaireReservationGerirOperUI(self.main_window, id_reserv)

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
                QMessageBox.warning(self, "Information", "⚠️ La réservation n’est accessible que pour les contrats confirmés ou terminés.")
        except Exception as e:
            print(f"Erreur lors de l'ouverture du contrat ou du formulaire : {e}")
            QMessageBox.warning(self, "Erreur", "Problème lors de l'ouverture.")

    def nettoyer_champs(self):
        """Efface le champ de recherche et le contenu du tableau."""
        self.search_input.clear()
        self.tableau_reservations.setRowCount(0)

    def retourner(self):
        """Retourne à l'écran précédent et recharge les données."""
        self.recharger_tableau()
        if self.retour_widget:
            self.main_window.central_widget.setCurrentWidget(self.retour_widget)
        else:
            # Fallback
            if self.mode == "oper":
                self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_operations)
            else:
                self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_reservations)
