from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import BUTTON_STYLE, FRAME_STYLE, TITLE_STYLE

class GestionRapportsUI(QWidget):
    """
    Interface de gestion des rapports et statistiques.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Gestion des Rapports")
        self.setStyleSheet("background-color: #EAEDED;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label_title = QLabel("GESTION DES RAPPORTS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        btn_retour = QPushButton("⬅ Retour")
        btn_retour.setStyleSheet(BUTTON_STYLE)
        btn_retour.clicked.connect(self.retourner)

        frame_layout.addWidget(btn_retour)
        frame.setLayout(frame_layout)

        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    def retourner(self):
        """Retourner à l'écran principal."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_agences_mere)
