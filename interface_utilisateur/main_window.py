from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

# Importation des interfaces
from interface_utilisateur.agences.ui_agences_mere import AgenceMereUI
from interface_utilisateur.clients.ui_clients import ClientsUI
from interface_utilisateur.agences.agence.ui_gestion_agences import GestionAgencesUI
from interface_utilisateur.agences.employe.ui_gestion_employes import GestionEmployesUI
from interface_utilisateur.agences.operations.ui_gestion_operations import GestionOperationsUI
from interface_utilisateur.agences.operations.rapports.ui_gestion_rapports import GestionRapportsUI
from interface_utilisateur.tableaux.ui_tableau_liste_contrats_client import TableauListeContratsClientUI
# from interface_utilisateur.tableaux.ui_tableau_reservations import TableauReservationsUI

# Importation des styles depuis ui_styles.py
from interface_utilisateur.ui_styles import (
    WINDOW_STYLE, WINDOW_GEOMETRY,
    BUTTON_STYLE_AGENCES, BUTTON_STYLE_CLIENTS, BUTTON_STYLE_QUITTER,
    LABEL_TITLE_FONT
)


class MainWindow(QMainWindow):
    """
    Fenêtre principale utilisant un QStackedWidget pour naviguer
    entre le menu principal, la gestion des agences, clients, et autres modules.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GN Location - Gestion")
        self.resize(WINDOW_GEOMETRY[2], WINDOW_GEOMETRY[3])
        self.setFixedSize(WINDOW_GEOMETRY[2], WINDOW_GEOMETRY[3])
        self.move(WINDOW_GEOMETRY[0], WINDOW_GEOMETRY[1])
        self.setStyleSheet(WINDOW_STYLE)

        # QStackedWidget pour la navigation
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.initUI()
        self.show_animation()

    def initUI(self):
        """Crée et affiche le menu principal."""
        self.menu_principal = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GN LOCATION")
        label_title.setFont(QFont(LABEL_TITLE_FONT['family'], LABEL_TITLE_FONT['size'], LABEL_TITLE_FONT['weight']))
        label_title.setAlignment(Qt.AlignCenter)

        # Boutons de navigation
        btn_agences = QPushButton("🏢 Agences")
        btn_clients = QPushButton("👤 Clients")
        btn_quitter = QPushButton("🚪 Quitter le système")

        # Application des couleurs et styles à partir de ui_styles.py
        btn_agences.setStyleSheet(BUTTON_STYLE_AGENCES)
        btn_clients.setStyleSheet(BUTTON_STYLE_CLIENTS)
        btn_quitter.setStyleSheet(BUTTON_STYLE_QUITTER)

        # Connexions
        btn_agences.clicked.connect(lambda: self.afficher_interface(self.ui_agences_mere))
        btn_clients.clicked.connect(lambda: self.afficher_interface(self.ui_clients))
        btn_quitter.clicked.connect(QApplication.quit)

        # Ajout au layout
        layout.addWidget(label_title)
        layout.addSpacing(20)
        layout.addWidget(btn_agences)
        layout.addWidget(btn_clients)
        layout.addSpacing(10)
        layout.addWidget(btn_quitter)

        self.menu_principal.setLayout(layout)

        # Initialisation des interfaces
        self.ui_agences_mere = AgenceMereUI(self)
        self.ui_gestion_agences = GestionAgencesUI(self)
        self.ui_gestion_employes = GestionEmployesUI(self)
        self.ui_clients = ClientsUI(self)
        self.ui_gestion_operations = GestionOperationsUI(self)
        self.ui_gestion_rapports = GestionRapportsUI(self)
        self.ui_tableau_liste_contrats_client = TableauListeContratsClientUI(self)
        # self.ui_tableau_reservations = TableauReservationsUI(self)

        # Ajout dans le QStackedWidget
        self.central_widget.addWidget(self.menu_principal)
        self.central_widget.addWidget(self.ui_agences_mere)
        self.central_widget.addWidget(self.ui_gestion_agences)
        self.central_widget.addWidget(self.ui_gestion_employes)
        self.central_widget.addWidget(self.ui_clients)
        self.central_widget.addWidget(self.ui_gestion_operations)
        self.central_widget.addWidget(self.ui_gestion_rapports)
        self.central_widget.addWidget(self.ui_tableau_liste_contrats_client)
        # self.central_widget.addWidget(self.ui_tableau_reservations)

        # Afficher le menu principal au démarrage
        self.central_widget.setCurrentWidget(self.menu_principal)

    def show_animation(self):
        """Effet fondu d’apparition."""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def afficher_interface(self, interface):
        """Affiche une interface spécifique dans le QStackedWidget."""
        self.central_widget.setCurrentWidget(interface)

    def revenir_menu_principal(self):
        """Retour au menu principal."""
        self.central_widget.setCurrentWidget(self.menu_principal)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
