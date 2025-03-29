from PyQt5.QtWidgets import QApplication
from interface_utilisateur.main_window import MainWindow
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
