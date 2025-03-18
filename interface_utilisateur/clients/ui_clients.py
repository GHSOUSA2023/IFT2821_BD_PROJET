from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from interface_utilisateur.clients.ui_styles_clients import BUTTON_STYLE, TITLE_STYLE

class ClientsUI(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titre principal
        label = QLabel("GESTION DES CLIENTS")
        label.setStyleSheet(TITLE_STYLE)

        # Bouton de retour
        btn_retour = QPushButton("⬅ Retour")
        btn_retour.setStyleSheet(BUTTON_STYLE)
        btn_retour.clicked.connect(self.main_window.revenir_menu_principal)

        layout.addWidget(label)
        layout.addWidget(btn_retour)
        self.setLayout(layout)
