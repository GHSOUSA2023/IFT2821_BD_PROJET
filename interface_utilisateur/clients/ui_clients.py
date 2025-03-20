from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.clients.ui_styles_clients import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE
from interface_utilisateur.clients.reservations.ui_formulaire_reservation import FormulaireReservationUI
from interface_utilisateur.clients.reservations.ui_formulaire_client import FormulaireClientUI


class ClientsUI(QWidget):
    """
    Interface d'accueil pour la gestion des clients.
    Suivant le même layout que la section 'Agences' avec un cadre centré.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #EAEDED;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Titre principal
        label_title = QLabel("GESTION DES CLIENTS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        # Cadre central (QFrame)
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)

        # Boutons avec style vert différencié
        btn_reservation = QPushButton("📝 Faire une réservation")
        btn_gerer_reserv = QPushButton("📋 Gérer mes réservations")
        btn_retour = QPushButton("⬅ Retour")

        # Appliquer les styles verts définis dans BUTTON_STYLE
        for btn in [btn_reservation, btn_gerer_reserv, btn_retour]:
            btn.setStyleSheet(BUTTON_STYLE)

        # Connexions futures
        # btn_reservation.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_faire_reservation))
        # btn_gerer_reserv.clicked.connect(lambda: self.main_window.afficher_interface(self.main_window.ui_gerer_reservations))
        btn_reservation.clicked.connect(self.ouvrir_faire_reservation)
        btn_retour.clicked.connect(self.main_window.revenir_menu_principal)

        # Ajout des boutons dans le cadre
        frame_layout.addWidget(btn_reservation)
        frame_layout.addWidget(btn_gerer_reserv)
        frame_layout.addWidget(btn_retour)

        frame.setLayout(frame_layout)

        # Ajout au layout principal
        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    def ouvrir_faire_reservation(self):
        if not hasattr(self.main_window, "ui_faire_reservation"):
            self.main_window.ui_faire_reservation = FormulaireReservationUI(self.main_window)
            self.main_window.central_widget.addWidget(self.main_window.ui_faire_reservation)
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_faire_reservation)
