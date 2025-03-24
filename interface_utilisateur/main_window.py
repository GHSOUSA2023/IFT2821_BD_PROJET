import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QStackedWidget, QFrame
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GN Location - Gestion")
        self.setGeometry(50, 50, 1000, 600)

        # 1) Construire le chemin absolu vers l'image
        image_path = os.path.join(os.path.dirname(__file__), "Background_picture.jpg")
        image_path = image_path.replace("\\", "/")  # Pour compatibilité Windows

        # 2) Feuille de style QSS pour étirer l'image de fond
        self.setStyleSheet(f"""
            QMainWindow {{
                border-image: url("{image_path}") 0 0 0 0 stretch stretch;
            }}
        """)

        # 3) QStackedWidget pour la navigation
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # 4) Initialisation de l'UI
        self.initUI()
        self.show_animation()

    def initUI(self):
        """Crée et affiche le menu principal."""
        # Widget racine du menu principal
        self.menu_principal = QWidget()
        main_layout = QVBoxLayout(self.menu_principal)
        main_layout.setAlignment(Qt.AlignCenter)

        # --- Création d'un QFrame (rectangle blanc) ---
        frame = QFrame()
        # Style du rectangle (fond blanc, arrondi, padding, etc.)
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.85);  /* Légère transparence */
                border-radius: 12px;
                padding: 20px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        # 5) Titre principal
        label_title = QLabel("GN LOCATION")
        label_title.setFont(QFont("Arial", 28, QFont.Bold))
        label_title.setAlignment(Qt.AlignCenter)

        # 6) Style unifié des boutons
        button_style = (
            "padding: 12px; "
            "font-size: 16px; "
            "border-radius: 8px; "
            "color: white; "
        )

        # 7) Boutons de navigation
        btn_agences = QPushButton("🏢 Agences")
        btn_clients = QPushButton("👤 Clients")
        btn_quitter = QPushButton("🚪 Quitter le système")

        # Couleurs spécifiques
        btn_agences.setStyleSheet(button_style + "background-color: #007BFF;")
        btn_clients.setStyleSheet(button_style + "background-color: #28A745;")
        btn_quitter.setStyleSheet(button_style + "background-color: #DC3545;")

        # 8) Connexions
        btn_agences.clicked.connect(lambda: self.afficher_interface(self.ui_agences_mere))
        btn_clients.clicked.connect(lambda: self.afficher_interface(self.ui_clients))
        btn_quitter.clicked.connect(QApplication.quit)

        # 9) Ajout des widgets dans le layout du frame (rectangle blanc)
        frame_layout.addWidget(label_title)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(btn_agences)
        frame_layout.addWidget(btn_clients)
        frame_layout.addSpacing(10)
        frame_layout.addWidget(btn_quitter)

        # 10) Ajouter le frame au layout principal (centré)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

        # 11) Initialiser les interfaces supplémentaires
        self.ui_agences_mere = AgenceMereUI(self)
        self.ui_gestion_agences = GestionAgencesUI(self)
        self.ui_gestion_employes = GestionEmployesUI(self)
        self.ui_clients = ClientsUI(self)
        self.ui_gestion_operations = GestionOperationsUI(self)
        self.ui_gestion_rapports = GestionRapportsUI(self)
        self.ui_tableau_liste_contrats_client = TableauListeContratsClientUI(self)

        # 12) Ajout dans le QStackedWidget
        self.central_widget.addWidget(self.menu_principal)
        self.central_widget.addWidget(self.ui_agences_mere)
        self.central_widget.addWidget(self.ui_gestion_agences)
        self.central_widget.addWidget(self.ui_gestion_employes)
        self.central_widget.addWidget(self.ui_clients)
        self.central_widget.addWidget(self.ui_gestion_operations)
        self.central_widget.addWidget(self.ui_gestion_rapports)
        self.central_widget.addWidget(self.ui_tableau_liste_contrats_client)

        # 13) Afficher le menu principal au démarrage
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
