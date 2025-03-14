from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from fonctions_gestion.tarifications import (
    ajouter_tarification, modifier_tarification, supprimer_tarification,
    lister_toutes_tarifications, rechercher_tarification,
    afficher_liste_tarifications_modifier, afficher_liste_tarifications_supprimer
)
from interface_utilisateur.tableaux.ui_tableau_tarifications import TableauTarificationsUI
from interface_utilisateur.agences.operations.tarifications.ui_formulaire_tarification import FormulaireTarificationUI
from PyQt5.QtWidgets import QMessageBox, QInputDialog

class GestionTarificationsUI(QWidget):
    """
    Interface avancée pour la gestion des tarifications.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Référence à la MainWindow
        self.setWindowTitle("Gestion des Tarifications")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES TARIFICATIONS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur (Card)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons
        btn_ajouter = QPushButton("➕ Ajouter une Tarification")
        btn_modifier = QPushButton("✏ Modifier une Tarification")
        btn_supprimer = QPushButton("🗑 Supprimer une Tarification")
        btn_lister = QPushButton("📋 Lister les Tarifications")
        btn_rechercher = QPushButton("🔍 Rechercher une Tarification")
        btn_retour = QPushButton("⬅ Retour")

        for btn in [btn_ajouter, btn_modifier, btn_supprimer, btn_lister, btn_rechercher, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions
        btn_ajouter.clicked.connect(self.ouvrir_formulaire_ajouter)
        btn_modifier.clicked.connect(self.afficher_liste_tarifications_modifier)
        btn_supprimer.clicked.connect(self.afficher_liste_tarifications_supprimer)
        btn_lister.clicked.connect(self.afficher_liste_tarifications)
        btn_rechercher.clicked.connect(self.rechercher_tarification)
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
        Ouvre le formulaire pour ajouter une nouvelle tarification.
        """
        self.formulaire_tarification = FormulaireTarificationUI(self.main_window, mode="ajouter")
        self.main_window.central_widget.addWidget(self.formulaire_tarification)
        self.main_window.central_widget.setCurrentWidget(self.formulaire_tarification)

    def afficher_liste_tarifications_modifier(self):
        """
        Affiche la liste des tarifications avec option de modification.
        """
        colonnes, tarifications = afficher_liste_tarifications_modifier()

        if tarifications:
            self.tableau_tarifications_modifier = TableauTarificationsUI("Modifier une Tarification", colonnes, tarifications, self.main_window)
            
            # Connecter le clic sur une ligne à l'ouverture du formulaire de modification
            self.tableau_tarifications_modifier.table_widget.cellClicked.connect(self.ouvrir_formulaire_modifier)
            
            self.main_window.central_widget.addWidget(self.tableau_tarifications_modifier)
            self.main_window.central_widget.setCurrentWidget(self.tableau_tarifications_modifier)

    def ouvrir_formulaire_modifier(self, row, column):
        """
        Ouvre le formulaire de modification d'une tarification lorsqu'une ligne est cliquée.
        """
        id_tarif = self.tableau_tarifications_modifier.table_widget.item(row, 0).text()  # ID de la tarification sélectionnée

        # Charger les informations de la tarification sélectionnée
        tarif_data = None
        for tarif in self.tableau_tarifications_modifier.donnees:
            if tarif[0] == id_tarif:
                tarif_data = tarif
                break

        if tarif_data:
            self.formulaire_modification = FormulaireTarificationUI(self.main_window, mode="modifier", tarification=tarif_data)
            self.main_window.central_widget.addWidget(self.formulaire_modification)
            self.main_window.central_widget.setCurrentWidget(self.formulaire_modification)

    def afficher_liste_tarifications_supprimer(self):
        """
        Affiche la liste des tarifications dans le tableau avec possibilité de suppression.
        """
        colonnes, tarifications = afficher_liste_tarifications_supprimer()

        if tarifications:
            self.tableau_tarifications_supprimer = TableauTarificationsUI("Supprimer une Tarification", colonnes, tarifications, self.main_window)
            self.tableau_tarifications_supprimer.table_widget.cellClicked.connect(self.confirmer_suppression)
            self.main_window.central_widget.addWidget(self.tableau_tarifications_supprimer)
            self.main_window.central_widget.setCurrentWidget(self.tableau_tarifications_supprimer)

    def confirmer_suppression(self, row, column):
        """
        Demande confirmation avant suppression d'une tarification.
        """
        id_tarif = self.tableau_tarifications_supprimer.table_widget.item(row, 0).text()
        QMessageBox.warning(self, "Confirmation", f"Voulez-vous vraiment supprimer cette tarification (ID: {id_tarif}) ?", QMessageBox.Yes | QMessageBox.No)

        if QMessageBox.Yes:
            supprimer_tarification(id_tarif)
            print("Tarification supprimée avec succès!")
            self.tableau_tarifications_supprimer.table_widget.removeRow(row)

    def afficher_liste_tarifications(self):
        """
        Récupère toutes les tarifications et les affiche dans le tableau.
        """
        colonnes, tarifications = lister_toutes_tarifications()

        if tarifications:
            self.tableau_tarifications = TableauTarificationsUI("Liste des Tarifications", colonnes, tarifications, self.main_window)
            self.main_window.central_widget.addWidget(self.tableau_tarifications)
            self.main_window.central_widget.setCurrentWidget(self.tableau_tarifications)

    def rechercher_tarification(self):
        """
        Affiche un champ de recherche et affiche les résultats dans le tableau.
        """
        terme, ok = QInputDialog.getText(self, "Recherche Tarification", "Entrez un prix ou un type de véhicule:")

        if ok and terme.strip():
            colonnes, tarifications = rechercher_tarification(terme.strip())

            if tarifications:
                self.tableau_resultats_recherche = TableauTarificationsUI("Résultats de la Recherche", colonnes, tarifications, self.main_window)
                self.main_window.central_widget.addWidget(self.tableau_resultats_recherche)
                self.main_window.central_widget.setCurrentWidget(self.tableau_resultats_recherche)
            else:
                QMessageBox.information(self, "Résultat", "Aucune tarification trouvée.")
