from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from interface_utilisateur.agences.operations.reservations.ui_gestion_reservations import GestionReservationsUI
from interface_utilisateur.agences.operations.rapports.ui_gestion_rapports import GestionRapportsUI
from fonctions_gestion.contrats import lister_toutes_contrats
from interface_utilisateur.tableaux.ui_tableau_reservations import TableauReservationsUI


class GestionOperationsUI(QWidget):
    """
    Interface de gestion des opérations.
    Permet d'accéder aux modules : 
    - Réservations
    - Contrats
    - Assurances
    - Tarification
    - Rapports
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Gestion des Opérations")
        self.setStyleSheet("background-color: #EAEDED;")

        self.initUI()

    def initUI(self):
        """
        Initialise l'interface : titres, boutons et mise en page.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES OPÉRATIONS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur principal (carte)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons de navigation
        btn_reservations = QPushButton("📅 Réservations")
        btn_contrats = QPushButton("📜 Contrats")
        btn_assurances = QPushButton("🛡 Assurances")
        btn_tarification = QPushButton("💰 Tarification")
        btn_rapports = QPushButton("📊 Rapports")
        btn_retour = QPushButton("⬅ Retour")

        # Appliquer le style aux boutons
        for btn in [btn_reservations, btn_contrats, btn_assurances, btn_tarification, btn_rapports, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions des boutons (placeholders pour l'instant)
        btn_reservations.clicked.connect(self.ouvrir_reservations)
        btn_contrats.clicked.connect(self.ouvrir_contrats)
        btn_assurances.clicked.connect(self.ouvrir_assurances)
        btn_tarification.clicked.connect(self.ouvrir_tarification)
        btn_rapports.clicked.connect(self.ouvrir_rapports)
        btn_retour.clicked.connect(self.retourner)

        # Ajout des boutons au conteneur
        for btn in [btn_reservations, btn_contrats, btn_assurances, btn_tarification, btn_rapports, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        # Ajout au layout principal
        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ------------------- Méthodes de navigation -------------------

    def ouvrir_reservations(self):
        """Méthode temporaire pour afficher les réservations."""
        if not hasattr(self.main_window, "ui_gestion_reservations"):
            self.main_window.ui_gestion_reservations = GestionReservationsUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_gestion_reservations)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_reservations)

    def ouvrir_contrats(self):
        """Ouvre le tableau des réservations (contrats) depuis l'interface opérations."""
        colonnes, reservations = lister_toutes_contrats()
        self.ui_tableau_reservations = TableauReservationsUI(
            "Liste des Réservations",
            colonnes,
            reservations,
            self.main_window,
            mode="oper",
            retour_widget=self
        )
        self.main_window.central_widget.addWidget(self.ui_tableau_reservations)
        self.main_window.central_widget.setCurrentWidget(self.ui_tableau_reservations)



    def ouvrir_assurances(self):
        """Méthode temporaire pour afficher les assurances."""
        print("Ouverture de la gestion des assurances (non implémenté).")

    def ouvrir_tarification(self):
        """Méthode temporaire pour afficher la tarification."""
        print("Ouverture de la gestion de la tarification (non implémenté).")

    def ouvrir_rapports(self):
        """
        Affiche le module des rapports et statistiques.
        """
        if not hasattr(self.main_window, "ui_gestion_rapports"):
            self.main_window.ui_gestion_rapports = GestionRapportsUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_gestion_rapports)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_rapports)

    def retourner(self):
        """Retourner à l'écran principal."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_agences_mere)
