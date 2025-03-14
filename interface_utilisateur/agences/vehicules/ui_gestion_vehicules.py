from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.vehicules import (
    ajouter_vehicule, modifier_vehicule, supprimer_vehicule,
    lister_tous_vehicules, rechercher_vehicule, 
    afficher_liste_vehicules_modifier, afficher_liste_vehicules_supprimer
)
from interface_utilisateur.tableaux.ui_tableau_vehicules import TableauVehiculesUI
from interface_utilisateur.agences.vehicules.ui_formulaire_vehicule import FormulaireVehiculeUI


class GestionVehiculesUI(QWidget):
    """
    Interface avancée pour la gestion des véhicules, utilisant le QStackedWidget
    pour afficher un tableau sans ouvrir de nouvelle fenêtre.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Référence à la MainWindow
        self.setWindowTitle("Gestion des Véhicules")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES VÉHICULES - AVANCÉE")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur (Card)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons
        btn_ajouter = QPushButton("➕ Ajouter un Véhicule")
        btn_modifier = QPushButton("✏ Modifier un Véhicule")
        btn_supprimer = QPushButton("🗑 Supprimer un Véhicule")
        btn_lister = QPushButton("📋 Lister les Véhicules")
        btn_rechercher = QPushButton("🔍 Rechercher un Véhicule")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions des boutons aux actions
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_vehicules_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_vehicules_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_vehicules)
        btn_rechercher.clicked.connect(self.rechercher_vehicule)
        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_agences_mere))

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ------------------- Fonctions -------------------

    def ouvrir_formulaire_ajouter(self):
        """
        Ouvre le formulaire pour ajouter un nouveau véhicule.
        """
        self.formulaire_vehicule = FormulaireVehiculeUI(self.main_window, mode="ajouter")
        self.main_window.central_widget.addWidget(self.formulaire_vehicule)
        self.main_window.central_widget.setCurrentWidget(self.formulaire_vehicule)

    def afficher_liste_vehicules_modifier(self):
        """
        Affiche la liste des véhicules avec option de modification.
        """
        colonnes, vehicules = afficher_liste_vehicules_modifier()

        if vehicules:
            self.tableau_vehicules_modifier = TableauVehiculesUI("Modifier un Véhicule", colonnes, vehicules, self.main_window)
            self.tableau_vehicules_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)
            self.main_window.central_widget.addWidget(self.tableau_vehicules_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_vehicules_modifier)

    def ouvrir_formulaire_modifier(self, row, column):
        """
        Ouvre le formulaire de modification d'un véhicule lorsqu'une ligne est cliquée.
        """
        id_vehic = self.tableau_vehicules_modifier.table_widget.item(row, 0).text()

        # Charger les informations du véhicule sélectionné
        vehicule_data = None
        for vehicule in self.tableau_vehicules_modifier.donnees:
            if vehicule[0] == id_vehic:
                vehicule_data = vehicule
                break

        if vehicule_data:
            self.formulaire_modification = FormulaireVehiculeUI(self.main_window, mode="modifier", vehicule=vehicule_data)
            self.main_window.central_widget.addWidget(self.formulaire_modification)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_modification)

    def afficher_liste_vehicules_supprimer(self):
        """
        Affiche la liste des véhicules dans le tableau avec possibilité de suppression.
        """
        colonnes, vehicules = afficher_liste_vehicules_supprimer()

        if vehicules:
            self.tableau_vehicules_supprimer = TableauVehiculesUI("Supprimer un Véhicule", colonnes, vehicules, self.main_window)
            self.tableau_vehicules_supprimer.table_widget.cellClicked.connect(self.confirmer_suppression)
            self.main_window.central_widget.addWidget(self.tableau_vehicules_supprimer)
            self.main_window.central_widget.setCurrentWidget(self.tableau_vehicules_supprimer)

    def confirmer_suppression(self, row, column):
        from PyQt5.QtWidgets import QMessageBox

        id_vehic = self.tableau_vehicules_supprimer.table_widget.item(row, 0).text()
        immatriculation = self.tableau_vehicules_supprimer.table_widget.item(row, 1).text()

        # Boîte de confirmation
        reponse = QMessageBox.question(
            None, 
            "Confirmation",
            f"Voulez-vous vraiment supprimer le véhicule '{immatriculation}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            supprimer_vehicule(id_vehic)
            print("🚗 Véhicule supprimé avec succès!")

        self.tableau_vehicules_supprimer.table_widget.removeRow(row)

    def afficher_liste_vehicules(self):
        """
        Récupère tous les véhicules et les affiche dans le tableau.
        """
        colonnes = ["ID", "Immatriculation", "Carburant", "Année", "Couleur", "Statut", "KM", "Marque", "Modèle", "Type"]
        
        # 🔹 Récupération des données
        vehicules = lister_tous_vehicules()

        # 🔹 Vérification des données avant affichage
        if vehicules:
            self.tableau_vehicules = TableauVehiculesUI("Liste des Véhicules", colonnes, vehicules, self.main_window)
            self.main_window.central_widget.addWidget(self.tableau_vehicules)
            self.main_window.central_widget.setCurrentWidget(self.tableau_vehicules)

    def rechercher_vehicule(self):
        """
        Affiche un champ de recherche et affiche les résultats dans le tableau.
        """
        from PyQt5.QtWidgets import QInputDialog

        terme, ok = QInputDialog.getText(self, "Recherche de Véhicule", "Entrez une immatriculation ou un modèle:")
        
        if ok and terme.strip():
            colonnes, vehicules = rechercher_vehicule(terme.strip())

            if vehicules:
                self.tableau_resultats_recherche = TableauVehiculesUI(
                    "Résultats de la Recherche", colonnes, vehicules, self.main_window
                )
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Résultat", "Aucun véhicule trouvé.")
