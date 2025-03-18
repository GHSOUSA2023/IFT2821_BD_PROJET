from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from interface_utilisateur.agences.ui_agences import AgencesUI
from interface_utilisateur.agences.operations.ui_gestion_operations import GestionOperationsUI


class AgenceMereUI(QWidget):
    """
    Interface principale pour l'administration des agences, employées, opérations et rapports.
    Permet de naviguer vers les modules principaux.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Administration des Agences")
        self.setStyleSheet("background-color: #EAEDED;")

        self.initUI()

    def initUI(self):
        """
        Initialise l'interface : titres, boutons, layouts.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("ADMINISTRATION GÉNÉRALE")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Conteneur principal (Carte visuelle)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # Boutons principaux
        btn_cadastres = QPushButton("📂 Cadastres")
        btn_operations = QPushButton("⚙️ Opérations")
        btn_retour = QPushButton("⬅ Retour")

        # Appliquer les styles
        for btn in [btn_cadastres, btn_operations, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions des boutons
        btn_cadastres.clicked.connect(self.ouvrir_cadastres)
        btn_operations.clicked.connect(self.ouvrir_operations)
        btn_retour.clicked.connect(self.main_window.revenir_menu_principal)

        # Ajout des boutons au layout du frame
        for btn in [btn_cadastres, btn_operations, btn_retour]:
            frame_layout.addWidget(btn)

        frame.setLayout(frame_layout)

        # Ajout au layout principal
        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # --------------------------------------------------------------------
    # Méthodes de navigation
    # --------------------------------------------------------------------

    def ouvrir_cadastres(self):
        """
        Affiche le module de cadastres (Agences, Employés, Véhicules, Clients).
        """
        if not hasattr(self.main_window, "ui_agences"):
            self.main_window.ui_agences = AgencesUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_agences)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_agences)

    def ouvrir_operations(self):
        """
        Affiche le module des opérations (réservations, contrats, gestion de flotte...).
        """
        if not hasattr(self.main_window, "ui_gestion_operations"):
            self.main_window.ui_gestion_operations = GestionOperationsUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_gestion_operations)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_operations)
