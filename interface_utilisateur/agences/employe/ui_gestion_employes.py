from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.employes import (
    ajouter_employe, modifier_employe, supprimer_employe,
    lister_employes, rechercher_employe, afficher_liste_employes_modifier,
    afficher_liste_employes_supprimer
)
from interface_utilisateur.tableaux.ui_tableau_employes import TableauEmployesUI
from interface_utilisateur.agences.employe.ui_formulaire_employes import FormulaireEmployeUI 

class GestionEmployesUI(QWidget):
    """
    Interface pour la gestion des employés.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Gestion des Employés")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES EMPLOYÉS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur principal
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons
        btn_ajouter = QPushButton("➕ Ajouter un Employé")
        btn_modifier = QPushButton("✏ Modifier un Employé")
        btn_supprimer = QPushButton("🗑 Supprimer un Employé")
        btn_lister = QPushButton("📋 Lister les Employés")
        btn_rechercher = QPushButton("🔍 Rechercher un Employé")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions (les fonctions seront implémentées après)
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_employes_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_employes_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_employes)
        btn_rechercher.clicked.connect(self.rechercher_employe)
        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_agences))

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ------------------- Fonctions (à implémenter) -------------------

    def ouvrir_formulaire_ajouter(self):
            """
            Ouvre le formulaire pour ajouter un nouvel employé.
            """
            self.formulaire_employe = FormulaireEmployeUI(self.main_window, mode="ajouter")
            self.main_window.central_widget.addWidget(self.formulaire_employe)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_employe)

    def afficher_liste_employes_modifier(self):
        """
        Affiche la liste des employés avec option de modification.
        """
        colonnes, employes = afficher_liste_employes_modifier()

        if employes:
            self.tableau_employes_modifier = TableauEmployesUI("Modifier un Employé", colonnes, employes, self.main_window)
            
            # Connecter le clic sur une ligne à l'ouverture du formulaire de modification
            self.tableau_employes_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)
            
            self.main_window.central_widget.addWidget(self.tableau_employes_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_employes_modifier)

    def ouvrir_formulaire_modifier(self, row, column):
        """
        Ouvre le formulaire de modification lorsqu'un employé est sélectionné.
        """
        id_emp = self.tableau_employes_modifier.table_widget.item(row, 0).text()  # ID de l'employé sélectionné

        # Récupérer les données de l'employé sélectionné
        employe_data = None
        for employe in self.tableau_employes_modifier.donnees:
            if employe[0] == id_emp:
                employe_data = employe
                break

        if employe_data:
            self.formulaire_modification = FormulaireEmployeUI(self.main_window, mode="modifier", employe=employe_data)
            self.main_window.central_widget.addWidget(self.formulaire_modification)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_modification)


    def afficher_liste_employes_supprimer(self):
        """
        Affiche la liste des employés avec option de suppression.
        """
        colonnes, employes = afficher_liste_employes_supprimer()

        if employes:
            self.tableau_employes_supprimer = TableauEmployesUI("Supprimer un Employé", colonnes, employes, self.main_window)
            
            # Connecter le clic à l'ouverture de la confirmation de suppression
            self.tableau_employes_supprimer.table_widget.cellClicked.connect(self.confirmer_suppression)

            self.main_window.central_widget.addWidget(self.tableau_employes_supprimer)
            self.main_window.central_widget.setCurrentWidget(self.tableau_employes_supprimer)


    def confirmer_suppression(self, row, column):
        """
        Demande confirmation avant suppression d'un employé.
        """
        id_emp = self.tableau_employes_supprimer.table_widget.item(row, 0).text()
        nom_emp = self.tableau_employes_supprimer.table_widget.item(row, 2).text()  # Nom de l'employé
        prenom_emp = self.tableau_employes_supprimer.table_widget.item(row, 3).text()  # Prénom de l'employé

        # Boîte de confirmation
        reponse = QMessageBox.question(
            None, 
            "Confirmation",
            f"Sohate exclut réellement l'employé '{nom_emp} {prenom_emp}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            # Supprimer l'employé
            supprimer_employe(id_emp)
            print("Employé supprimé avec succès!")

            # Retourner à la liste des employés
            self.tableau_employes_supprimer.table_widget.removeRow(row)

    def afficher_liste_employes(self):
        """
        Récupère tous les employés et les affiche dans le tableau `TableauEmployesUI` avec un filtre de recherche.
        """
        colonnes = ["ID", "NAS", "Nom", "Prénom", "Salaire", "Poste", "Agence"]  # 🔹 Correction ici
        employes = lister_employes()  # 🔹 Récupération correcte

        if employes:
            self.tableau_employes = TableauEmployesUI("Liste des Employés", colonnes, employes, self.main_window)
            self.main_window.central_widget.addWidget(self.tableau_employes)
            self.main_window.central_widget.setCurrentWidget(self.tableau_employes)




    def rechercher_employe(self):
        """
        Affiche un champ de recherche et affiche les résultats dans le tableau.
        """
        from PyQt5.QtWidgets import QInputDialog, QMessageBox
        from fonctions_gestion.employes import rechercher_employe
        from interface_utilisateur.tableaux.ui_tableau_employes import TableauEmployesUI

        # Demande à l'utilisateur de saisir un terme de recherche
        terme, ok = QInputDialog.getText(self, "Recherche d'Employé", "Entrez un NAS ou un Nom:")

        if ok and terme.strip():
            # Récupérer les résultats
            colonnes, employes = rechercher_employe(terme.strip())

            if employes:
                self.tableau_resultats_recherche = TableauEmployesUI(
                    "Résultats de la Recherche", colonnes, employes, self.main_window
                )
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                QMessageBox.information(self, "Résultat", "Aucun employé trouvé.")

