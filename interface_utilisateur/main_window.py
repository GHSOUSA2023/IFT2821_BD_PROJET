from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

# Interface principale "ui_agences" (accueil Agences)
from interface_utilisateur.agences.ui_agences import AgencesUI
# Interface "ui_clients" (accueil Clients)
from interface_utilisateur.clients.ui_clients import ClientsUI
# Interface avancée de gestion d'Agences
from interface_utilisateur.agences.agence.ui_gestion_agences import GestionAgencesUI
from interface_utilisateur.agences.employe.ui_gestion_employes import GestionEmployesUI

class MainWindow(QMainWindow):
    """
    Fenêtre principale utilisant un QStackedWidget pour naviguer
    entre le menu principal, l'accueil agences, la gestion avancée
    et l'accueil clients.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GN Location - Gestion")
        self.setGeometry(50, 50, 1000, 600)
        # Activer le mode plein écran
        #self.showFullScreen()
        self.setStyleSheet("background-color: #f4f4f4;")

        # QStackedWidget pour la navigation interne
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.initUI()
        self.show_animation()

    def initUI(self):
        """Crée et affiche le menu principal dans le QStackedWidget."""
        self.menu_principal = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GN LOCATION")
        label_title.setFont(QFont("Arial", 24, QFont.Bold))
        label_title.setAlignment(Qt.AlignCenter)

        # Boutons de navigation (Agences / Clients)
        btn_agences = QPushButton("🏢 Gérer les Agences")
        btn_clients = QPushButton("👤 Gérer les Clients")

        btn_agences.setFont(QFont("Arial", 14))
        btn_clients.setFont(QFont("Arial", 14))

        btn_agences.setStyleSheet(
            "padding: 10px; background-color: #007BFF; color: white; border-radius: 5px;"
        )
        btn_clients.setStyleSheet(
            "padding: 10px; background-color: #28A745; color: white; border-radius: 5px;"
        )

        # Connexion des boutons aux écrans respectifs
        btn_agences.clicked.connect(lambda: self.afficher_interface(self.ui_agences))
        btn_clients.clicked.connect(lambda: self.afficher_interface(self.ui_clients))

        layout.addWidget(label_title)
        layout.addSpacing(20)
        layout.addWidget(btn_agences)
        layout.addWidget(btn_clients)

        self.menu_principal.setLayout(layout)

        # Instanciation des écrans :
        # 1) Accueil "ui_agences"
        self.ui_agences = AgencesUI(self)
        # 2) Gestion avancée "ui_gestion_agences"
        self.ui_gestion_agences = GestionAgencesUI(self)
        # 3) Accueil "ui_clients"
        self.ui_clients = ClientsUI(self)

        # Ajout des écrans au QStackedWidget
        self.central_widget.addWidget(self.menu_principal)      # index 0
        self.central_widget.addWidget(self.ui_agences)          # index 1
        self.central_widget.addWidget(self.ui_gestion_agences)  # index 2
        self.central_widget.addWidget(self.ui_clients)          # index 3

        # Afficher le menu principal au démarrage
        self.central_widget.setCurrentWidget(self.menu_principal)

    def show_animation(self):
        """Effet d'apparition en fondu sur toute la fenêtre."""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def afficher_interface(self, interface):
        """
        Affiche une interface spécifique dans la fenêtre principale (QStackedWidget).
        """
        self.central_widget.setCurrentWidget(interface)

    def revenir_menu_principal(self):
        """Retour au menu principal."""
        self.central_widget.setCurrentWidget(self.menu_principal)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
