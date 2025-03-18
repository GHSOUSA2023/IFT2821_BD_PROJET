from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.agences import (
    ajouter_agence, modifier_agence, supprimer_agence,
    lister_tout_agences, rechercher_agence, afficher_liste_agences_modifier, afficher_liste_agences_supprimer, confirmer_suppression
)
from interface_utilisateur.tableaux.ui_tableau_agences import TableauAgencesUI
from interface_utilisateur.agences.agence.ui_formulaire_agence import FormulaireAgenceUI
from PyQt5.QtWidgets import QMessageBox


import io
import sys

class GestionAgencesUI(QWidget):
    """
    Interface avancée pour la gestion des agences, utilisant le QStackedWidget
    pour afficher un tableau sans ouvrir de nouvelle fenêtre.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Référence à la MainWindow
        self.setWindowTitle("Gestion des Agences")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES AGENCES - AVANCÉE")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur (Card)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons
        btn_ajouter = QPushButton("➕ Ajouter une Agence")
        btn_modifier = QPushButton("✏ Modifier une Agence")
        btn_supprimer = QPushButton("🗑 Supprimer une Agence")
        btn_lister = QPushButton("📋 Lister les Agences")
        btn_rechercher = QPushButton("🔍 Rechercher une Agence")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_agences_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_agences_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_agences)
        btn_rechercher.clicked.connect(self.rechercher_agence)
        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_agences))

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ------------------- Fonctions -------------------

    def ouvrir_formulaire_ajouter(self):
        """
        Ouvre le formulaire pour ajouter une nouvelle agence.
        """
        self.formulaire_agence = FormulaireAgenceUI(self.main_window, mode="ajouter")
        self.main_window.central_widget.addWidget(self.formulaire_agence)
        self.main_window.central_widget.setCurrentWidget(self.formulaire_agence)

    def afficher_liste_agences_modifier(self):
        """
        Affiche la liste des agences avec option de modification.
        """
        colonnes, agences = afficher_liste_agences_modifier()

        if agences:
            self.tableau_agences_modifier = TableauAgencesUI("Modifier une Agence", colonnes, agences, self.main_window)
            
            # Connecter le clic sur une ligne à l'ouverture du formulaire de modification
            self.tableau_agences_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)
            
            self.main_window.central_widget.addWidget(self.tableau_agences_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_agences_modifier)


    def ouvrir_formulaire_modifier(self, row, column):
        """
        Ouvre le formulaire de modification d'une agence lorsqu'une ligne est cliquée.
        """
        id_agence = self.tableau_agences_modifier.table_widget.item(row, 0).text()  # ID de l'agence sélectionnée

        # Charger les informations de l'agence sélectionnée
        agence_data = None
        for agence in self.tableau_agences_modifier.donnees:
            if agence[0] == id_agence:
                agence_data = agence
                break

        if agence_data:
            self.formulaire_modification = FormulaireAgenceUI(self.main_window, mode="modifier", agence=agence_data)
            self.main_window.central_widget.addWidget(self.formulaire_modification)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_modification)



    def afficher_liste_agences_supprimer(self):
        """
        Affiche la liste des agences dans le tableau avec possibilité de suppression.
        """
        colonnes, agences = afficher_liste_agences_supprimer()

        if agences:
            self.tableau_agences_supprimer = TableauAgencesUI("Supprimer une Agence", colonnes, agences, self.main_window)
            self.tableau_agences_supprimer.table_widget.cellClicked.connect(self.confirmer_suppression)
            self.main_window.central_widget.addWidget(self.tableau_agences_supprimer)
            self.main_window.central_widget.setCurrentWidget(self.tableau_agences_supprimer)


    def confirmer_suppression(self, row, column):
        from PyQt5.QtWidgets import QMessageBox

        id_agence = self.tableau_agences_supprimer.table_widget.item(row, 0).text()
        nom_agence = self.tableau_agences_supprimer.table_widget.item(row, 1).text()

        # question fixe
        reponse = QMessageBox.question(
            None, 
            "Confirmation",
            f"Deseja realmente excluir '{nom_agence}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            # supprimer
            supprimer_agence(id_agence)
            print("Excluído com sucesso!")

        # returner a liste d'agences
        self.tableau_agences_supprimer.table_widget.removeRow(row)



    def executer_suppression(self, button, id_agence):
        if button.text() == "&Yes":
            supprimer_agence(id_agence)
            print("Agence supprimée avec succès!")  # Mensagem apenas no console

            # Retornar à tela principal
            self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_agences)

            

    def afficher_liste_agences(self):
        """
        Récupère toutes les agences et les affiche dans le tableau TableauAgencesUI.
        """
        colonnes = ["ID", "Nom", "Ville", "Adresse", "Téléphone", "Email"]
        
        # 🔹 Récupération propre des données
        agences = lister_tout_agences()

        # 🔹 Vérification des données avant affichage
        if agences:
            self.tableau_agences = TableauAgencesUI("Liste des Agences", colonnes, agences, self.main_window)
            self.main_window.central_widget.addWidget(self.tableau_agences)
            self.main_window.central_widget.setCurrentWidget(self.tableau_agences)

    def rechercher_agence(self):
        """
        Affiche un champ de recherche et affiche les résultats dans le tableau.
        """
        from PyQt5.QtWidgets import QInputDialog

        # Demande à l'utilisateur de saisir un terme de recherche
        terme, ok = QInputDialog.getText(self, "Recherche d'Agence", "Entrez un nom, une ville ou une adresse:")
        
        if ok and terme.strip():
            # Récupérer les résultats
            colonnes, agences = rechercher_agence(terme.strip())

            if agences:
                self.tableau_resultats_recherche = TableauAgencesUI(
                    "Résultats de la Recherche", colonnes, agences, self.main_window
                )
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Résultat", "Aucune agence trouvée.")

