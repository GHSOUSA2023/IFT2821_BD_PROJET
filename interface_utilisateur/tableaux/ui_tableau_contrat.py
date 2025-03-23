from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt
from fonctions_gestion.contratclient import remplir_contrat  # Assure-toi que cette fonction est bien disponible

class TableauContratUI(QWidget):
    """
    Interface pour afficher un contrat de location avec des options pour enregistrer en PDF,
    imprimer et envoyer par email.
    """
    def __init__(self, contrat_info, main_window, retour_widget):
        super().__init__()
        self.main_window = main_window
        self.retour_widget = retour_widget
        self.setWindowTitle("Contrat de location")

        # Remplir le texte du contrat à partir des données reçues (pyodbc.Row)
        donnees_contrat = dict(contrat_info)
        self.contrat_texte = remplir_contrat(donnees_contrat)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Zone d'affichage du contrat dans un champ texte non modifiable
        self.text_area = QTextEdit()
        self.text_area.setPlainText(self.contrat_texte)
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        # Bouton pour enregistrer le contrat en PDF
        self.btn_enregistrer_pdf = QPushButton("📥 Enregistrer en PDF")
        self.btn_enregistrer_pdf.clicked.connect(self.enregistrer_pdf)

        # Bouton pour imprimer le contrat
        self.btn_imprimer = QPushButton("🖨️ Imprimer")
        self.btn_imprimer.clicked.connect(self.imprimer_contrat)


        # Bouton retour pour revenir à l'écran précédent
        self.btn_retour = QPushButton("🔙 Retour")
        self.btn_retour.clicked.connect(self.retourner)

        # Ajout des boutons au layout
        layout.addWidget(self.btn_enregistrer_pdf)
        layout.addWidget(self.btn_imprimer)
        layout.addWidget(self.btn_retour)

        self.setLayout(layout)

    # Fonction pour enregistrer le contrat affiché en PDF
    def enregistrer_pdf(self):
        fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer le contrat en PDF", "", "PDF Files (*.pdf)")
        if fichier:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fichier)
            self.text_area.document().print_(printer)
            QMessageBox.information(self, "Succès", "Le contrat a été enregistré en PDF.")

    # Fonction pour imprimer le contrat directement
    def imprimer_contrat(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.text_area.document().print_(printer)


    # Retourne à l'écran précédent
    def retourner(self):
        self.main_window.central_widget.setCurrentWidget(self.retour_widget)
