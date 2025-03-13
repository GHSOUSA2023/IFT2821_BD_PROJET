from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.agences import (
    ajouter_agence, modifier_agence, supprimer_agence,
    lister_tout_agences, rechercher_agence
)
from interface_utilisateur.tableaux.ui_tableau_agences import TableauAgencesUI
from interface_utilisateur.agences.ui_formulaire_agence import FormulaireAgenceUI


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
        btn_ajouter.clicked.connect(self.ajouter_agence)
        btn_modifier.clicked.connect(self.modifier_agence)
        btn_supprimer.clicked.connect(self.supprimer_agence)
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

    def ajouter_agence(self):
        """Ajoute une nouvelle agence."""
        ajouter_agence()

    def modifier_agence(self):
        """Modifie une agence existante."""
        modifier_agence()

    def supprimer_agence(self):
        """Supprime une agence."""
        supprimer_agence()

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
        """Recherche une agence."""
        rechercher_agence()
