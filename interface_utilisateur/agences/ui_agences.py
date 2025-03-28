from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from interface_utilisateur.agences.agence.ui_gestion_agences import GestionAgencesUI
from interface_utilisateur.agences.employe.ui_gestion_employes import GestionEmployesUI
from interface_utilisateur.agences.vehicules.ui_gestion_vehicules import GestionVehiculesUI

class AgencesUI(QWidget):
    """
    Interface d'accueil pour le module 'Agences'.
    Permet de naviguer vers la gestion avancée des agences,
    la gestion des employés, la gestion des véhicules et la gestion des clients,
    tout en restant dans le QStackedWidget du MainWindow.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Accueil - Agences")
        self.setStyleSheet("background-color: #EAEDED;")

        self.initUI()

    def initUI(self):
        """
        Initialise l'interface : titres, boutons, layouts.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES AGENCES")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur des options (Carte visuelle)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons de gestion
        btn_gestion_agences = QPushButton("📍 Gestion des Agences")
        btn_gestion_employes = QPushButton("👨‍💼 Gérer les Employés")
        btn_gestion_vehicules = QPushButton("🚗 Gérer les Véhicules")
        btn_gestion_clients = QPushButton("👥 Gérer les Clients")
        btn_retour = QPushButton("⬅ Retour")

        # Appliquer les styles définis dans ui_styles_agences.py
        for btn in [btn_gestion_agences, btn_gestion_employes, btn_gestion_vehicules, btn_gestion_clients, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions des boutons
        btn_gestion_agences.clicked.connect(self.ouvrir_gestion_agences)
        # Les 3 autres boutons sont ici à titre indicatif. 
        # Vous pouvez les relier à leurs écrans respectifs une fois créés:
        btn_gestion_employes.clicked.connect(self.ouvrir_gestion_employes)
        btn_gestion_vehicules.clicked.connect(self.ouvrir_gestion_vehicules)
        btn_gestion_clients.clicked.connect(self.ouvrir_gestion_clients)

        btn_retour.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_agences_mere))

        # Ajout des boutons au layout du 'frame'
        for btn in [btn_gestion_agences, btn_gestion_employes, btn_gestion_vehicules, btn_gestion_clients, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        # Ajout au layout principal
        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # --------------------------------------------------------------------
    # Méthodes de navigation
    # --------------------------------------------------------------------
    def ouvrir_gestion_agences(self):
        """
        Affiche l'écran de gestion avancée (ui_gestion_agences).
        """
        # Vérifier si l'attribut existe dans MainWindow
        if not hasattr(self.main_window, "ui_gestion_agences"):
            self.main_window.ui_gestion_agences = GestionAgencesUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_gestion_agences)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_agences)

    def ouvrir_gestion_employes(self):
        """
        Méthode placeholder: A relier avec l'interface de gestion des employés.
        """
                # Vérifier si l'attribut existe dans MainWindow
        if not hasattr(self.main_window, "ui_gestion_employes"):
            self.main_window.ui_gestion_employes = GestionEmployesUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_gestion_employes)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_employes)

        print("Ouverture de la gestion des employés (non implémenté).")

    def ouvrir_gestion_vehicules(self):
        """
        Méthode placeholder: A relier avec l'interface de gestion des véhicules.
        """
        if not hasattr(self.main_window, "ui_gestion_vehicules"):
            self.main_window.ui_gestion_vehicules = GestionVehiculesUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_gestion_vehicules)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_vehicules)

    def ouvrir_gestion_clients(self):
        """
        Méthode placeholder: A relier avec l'interface de gestion des clients.
        """
        print("Ouverture de la gestion des clients (non implémenté).")
