from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QPropertyAnimation, QRect
from interface_utilisateur.agences.ui_agences import AgenceWindow
from interface_utilisateur.clients.ui_clients import ClientWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logiciel de Gestion de Location")
        self.setGeometry(100, 100, 800, 500)  # Largura x Altura

        # Layout principal
        layout = QVBoxLayout()

        # Botão para abrir a interface de Agências
        self.btn_agences = QPushButton("Gérer les Agences")
        self.btn_agences.setStyleSheet("font-size: 16px; padding: 10px;")
        self.btn_agences.clicked.connect(self.ouvrir_agences)

        # Botão para abrir a interface de Clientes
        self.btn_clients = QPushButton("Gérer les Clients")
        self.btn_clients.setStyleSheet("font-size: 16px; padding: 10px;")
        self.btn_clients.clicked.connect(self.ouvrir_clients)

        # Adicionando os botões ao layout
        layout.addWidget(self.btn_agences)
        layout.addWidget(self.btn_clients)

        # Configuração do widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Iniciar animação na abertura
        self.animer_ouverture()

    def animer_ouverture(self):
        """Animação da janela ao abrir."""
        self.animacao = QPropertyAnimation(self, b"geometry")
        self.animacao.setDuration(1000)  # 1 segundo
        self.animacao.setStartValue(QRect(self.x(), self.y() - 100, self.width(), self.height()))
        self.animacao.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animacao.start()

    def ouvrir_agences(self):
        """Abre a interface de Agências."""
        self.fenetre_agences = AgenceWindow()
        self.fenetre_agences.show()

    def ouvrir_clients(self):
        """Abre a interface de Clientes."""
        self.fenetre_clients = ClientWindow()
        self.fenetre_clients.show()

if __name__ == "__main__":
    app = QApplication([])
    fenetre = MainWindow()
    fenetre.show()
    app.exec_()
