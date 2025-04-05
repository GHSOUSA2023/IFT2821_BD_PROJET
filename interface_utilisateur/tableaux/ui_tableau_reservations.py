from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from fonctions_gestion.reservations import rechercher_reservation, lister_toutes_reservations
from fonctions_gestion.contratclient import get_contrat_par_reservation
from interface_utilisateur.tableaux.ui_tableau_contrat import TableauContratUI

from interface_utilisateur.agences.operations.contrats.ui_formulaire_contrat_gerer import FormulaireContratGererUI
from interface_utilisateur.agences.operations.reservations.ui_formulaire_reservation_oper import FormulaireReservationOperUI
from interface_utilisateur.agences.operations.reservations.ui_formulaire_reservation_gerer_oper import FormulaireReservationGerirOperUI



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
        self.search_input.textChanged.connect(self.tb_op_filtrer_tableau)
        layout.addWidget(QLabel("Recherche réservation :"))
        layout.addWidget(self.search_input)

        # Tableau
        self.tb_op_tableau_reservations = QTableWidget()
        self.tb_op_tableau_reservations.setColumnCount(len(self.colonnes))
        self.tb_op_tableau_reservations.setHorizontalHeaderLabels(self.colonnes)

        header = self.tb_op_tableau_reservations.horizontalHeader()
        for i in range(len(self.colonnes)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.tb_op_tableau_reservations.cellDoubleClicked.connect(self.tb_op_ouvrir_contrat_selectionne)
        layout.addWidget(self.tb_op_tableau_reservations)

        self.tb_op_charger_donnees(self.donnees)


        # Bouton retour
        self.btn_retour = QPushButton("🔙 Retour")
        self.btn_retour.clicked.connect(self.tb_op_retourner)
        layout.addWidget(self.btn_retour)

        self.setLayout(layout)

    def tb_op_charger_donnees(self, donnees):
        self.tb_op_tableau_reservations.setRowCount(0)
        for index, ligne in enumerate(donnees):
            self.tb_op_tableau_reservations.insertRow(index)
            for col, valeur in enumerate(ligne):
                self.tb_op_tableau_reservations.setItem(index, col, QTableWidgetItem(str(valeur)))
        self.tb_op_tableau_reservations.resizeColumnsToContents()

    def tb_op_filtrer_tableau(self):
        terme = self.search_input.text().strip().lower()
        self.terme_recherche = terme
        if not terme:
            colonnes, reservations = lister_toutes_reservations()
            self.tb_op_charger_donnees(reservations)
            return
        colonnes, reservations_filtres = rechercher_reservation(terme)
        self.tb_op_charger_donnees(reservations_filtres)

    def tb_op_recharger_tableau(self):
        if self.terme_recherche:
            colonnes, reservations_filtres = rechercher_reservation(self.terme_recherche)
            self.tb_op_charger_donnees(reservations_filtres)
        else:
            colonnes, reservations = lister_toutes_reservations()
            self.tb_op_charger_donnees(reservations)

    def tb_op_ouvrir_contrat_selectionne(self, row, _column):
        try:
            status = self.tb_op_tableau_reservations.item(row, 6).text()
            id_reserv = int(self.tb_op_tableau_reservations.item(row, 0).text())

            if self.mode == "contrat":
                if status == "CONFIRMEE":                
                    formulaire_gerer = FormulaireContratGererUI(self.main_window, id_reserv, retour_widget=self)
                    self.main_window.central_widget.addWidget(formulaire_gerer)
                    self.main_window.central_widget.setCurrentWidget(formulaire_gerer)    
                else:
                    QMessageBox.information(self, "Information", "Aucun contrat n’a été généré pour cette réservation.")
                return  # Termina aqui se for mode contrat

            # Comportamento normal (mode oper)
            if status == "EN ATTENTE":
                formulaire_gerer = FormulaireReservationGerirOperUI(self.main_window, id_reserv, retour_widget=self)
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
                QMessageBox.warning(self, "Information", "La réservation n’est accessible que pour les contrats confirmés ou terminés.")

        except Exception as e:
            print(f"Erreur lors de l'ouverture du contrat ou du formulaire : {e}")
            QMessageBox.warning(self, "Erreur", "Problème lors de l'ouverture.")


    def tb_op_retourner(self):
        # Recharge le tableau avant de revenir
        self.terme_recherche = None
        self.search_input.clear()

        self.tb_op_recharger_tableau()
        
        if self.retour_widget:
            # Si un widget de retour est défini, on y retourne
            self.main_window.central_widget.setCurrentWidget(self.retour_widget)
        elif self.mode == "contrat":
            # Si le mode est 'contrat', retour à la gestion des opérations
            self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_operations)
        elif self.mode == "oper":
            # Si le mode est 'oper', retour à la gestion des réservations
            self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_reservations)
        else:
            # Sinon, retour par défaut vers le tableau général des réservations
            if hasattr(self.main_window, 'ui_tableau_g_reservation'):
                self.main_window.central_widget.setCurrentWidget(self.main_window.ui_tableau_g_reservation)



    def tb_op_nettoyer_champs(self):
        self.search_input.clear()
        self.tb_op_tableau_reservations.setRowCount(0)
