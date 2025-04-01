from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.vehicules import (
    ajouter_vehicule, modifier_vehicule, supprimer_vehicule, lister_tous_vehicules, rechercher_vehicule, get_vehicule_par_id)
from fonctions_gestion.flotte import lister_marques, lister_tout_modeles, lister_tout_tp_vehic, lister_vehicules_en_maintenance
from interface_utilisateur.tableaux.ui_tableau_vehicules import TableauVehiculesUI
from interface_utilisateur.agences.vehicules.ui_formulaire_vehicules import FormulaireVehiculeUI
from interface_utilisateur.tableaux.ui_tableau_vehicules_maintenance import TableauVehiculesMaintUI


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
        btn_maintenance = QPushButton("🛠️ Maintenance du Véhicule")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_maintenance, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions des boutons aux actions
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_vehicules_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_vehicules_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_vehicules)
        btn_maintenance.clicked.connect(self.gerer_maintenance_vehicule)
        btn_rechercher.clicked.connect(self.rechercher_vehicule)

        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_agences))

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_maintenance, btn_retour]:
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
        self.ui_formulaire_vehicules = FormulaireVehiculeUI(self.main_window, mode="ajouter")
        self.main_window.central_widget.addWidget(self.ui_formulaire_vehicules)
        self.main_window.central_widget.setCurrentWidget(self.ui_formulaire_vehicules)

    def afficher_liste_vehicules_modifier(self):
        vehicules = lister_tous_vehicules()
        colonnes = ["ID", "Immatriculation", "Carburant", "Année", "Couleur", "Statut", "KM", "Marque", "Modèle", "Type"]

        if vehicules:
            self.tableau_vehicules_modifier = TableauVehiculesUI("Modifier un Véhicule", colonnes, vehicules, self.main_window, self)
            self.tableau_vehicules_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)
            self.main_window.central_widget.addWidget(self.tableau_vehicules_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_vehicules_modifier)



    def ouvrir_formulaire_modifier(self, row, column):
        """
        Récupère tous les véhicules et les affiche dans le tableau.
        """
        colonnes = ["ID", "Immatriculation", "Carburant", "Année", "Couleur", "Statut", "KM", "Marque", "Modèle", "Type"]
        
        # 🔹 Récupération des données
        vehicules = lister_tous_vehicules()

        # 🔹 Vérification des données avant affichage
        if vehicules:
            self.tableau_vehicules = TableauVehiculesUI("Liste des Véhicules", colonnes, vehicules, self.main_window, retour_widget=self, mode="modifier")
            self.main_window.central_widget.addWidget(self.tableau_vehicules)
            self.main_window.central_widget.setCurrentWidget(self.tableau_vehicules)

    def afficher_liste_vehicules_supprimer(self):
        """
        Exibe a lista de veículos no quadro com possibilidade de exclusão por duplo clique.
        """
        # Define as colunas manualmente:
        colonnes = ["ID", "Immatriculation", "Carburant", "Année", "Couleur", "Statut", "KM", "Marque", "Modèle", "Type"]
        
        # Obtenha os veículos (assumindo que lister_tous_vehicules() retorna apenas a lista de veículos)
        vehicules = lister_tous_vehicules()

        if vehicules:
            self.tableau_vehicules_supprimer = TableauVehiculesUI("Supprimer un Véhicule", colonnes, vehicules, self.main_window, self)
            # Conecta o duplo clique para confirmar a exclusão
            self.tableau_vehicules_supprimer.table_widget.cellDoubleClicked.connect(self.confirmer_suppression)
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
            f"Voulez-vous vraiment supprimer le véhicule '{immatriculation}' ?",
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
            self.tableau_vehicules = TableauVehiculesUI("Liste des Véhicules", colonnes, vehicules, self.main_window, retour_widget=self)
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
                    "Résultats de la Recherche", colonnes, vehicules, self.main_window, retour_widget=self
                )
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Résultat", "Aucun véhicule trouvé.")


    def gerer_maintenance_vehicule(self):
        """
        Affiche la liste des véhicules en maintenance dans un tableau dédié.
        """
        colonnes = [
            "ID", "Agence", "Marque", "Modèle", "Année", "Couleur", 
            "Kilométrage", "Immatriculation", "Carburant", "Type", "Statut"
        ]

        # 🔹 Récupération des données depuis la BD
        donnees = lister_vehicules_en_maintenance()

        # 🔹 Vérification et affichage
        if donnees:
            self.tableau_vehicules_maintenance = TableauVehiculesMaintUI(
                "Véhicules en Maintenance",
                colonnes,
                donnees,
                self.main_window,
                retour_widget=self
            )
            self.main_window.central_widget.addWidget(self.tableau_vehicules_maintenance)
            self.main_window.central_widget.setCurrentWidget(self.tableau_vehicules_maintenance)
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Information", "Aucun véhicule en maintenance trouvé.")
