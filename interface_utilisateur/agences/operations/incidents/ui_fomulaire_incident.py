from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout,
    QDateEdit, QTextEdit, QMessageBox, QApplication, QComboBox, QLineEdit
)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QKeyEvent
from constantes import constantes
from fonctions_gestion.incidents import ajouter_incident


class CustomDateEdit(QDateEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.ouvrir_calendrier)

    def ouvrir_calendrier(self):
        event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Down, Qt.AltModifier)
        QApplication.postEvent(self, event)


class FormulaireIncidentUI(QWidget):
    """
    Formulaire pour enregistrer un incident lié à un contrat et un véhicule.
    """
    def __init__(self, main_window, retour_widget, id_contrat, nom_client, infos_vehicule, date_debut, date_fin):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.main_window = main_window
        self.retour_widget = retour_widget
        self.id_contrat = id_contrat

        self.setWindowTitle("Déclarer un incident")
        self.setGeometry(100, 100, 600, 600)
        self.nom_client = nom_client
        self.infos_vehicule = infos_vehicule
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Infos sur le contrat et le véhicule avec dates ajoutées
        self.label_infos_contrat = QLabel(
            f"Contrat #{self.id_contrat} - Client: {self.nom_client}\n"
            f"Date de début: {self.date_debut} | Date de fin: {self.date_fin}"
        )
        self.label_infos_vehicule = QLabel(f"""
Marque: {self.infos_vehicule.get('MARQUE', '')}
Modèle: {self.infos_vehicule.get('MODELE', '')}
Couleur: {self.infos_vehicule.get('COULEUR', '')}
Immatriculation: {self.infos_vehicule.get('IMMATRICULATION', '')}
""")

        # Type d’incident
        self.type_incident_input = QComboBox()
        self.type_incident_input.addItem("Sélectionner un type d'incident")
        for t in constantes.TYPES_INCIDENTS:
            self.type_incident_input.addItem(t)

        # Date de l’incident
        self.date_incident_input = CustomDateEdit()
        self.date_incident_input.setCalendarPopup(True)
        self.date_incident_input.setDate(QDate.currentDate())
        self.date_incident_input.setMaximumDate(QDate.currentDate())

        # Coûts
        self.couts_input = QLineEdit()
        self.couts_input.setPlaceholderText("Ex: 150.00")

        # Détails
        self.details_input = QTextEdit()
        self.details_input.setPlaceholderText("Décrivez les circonstances de l'incident...")
        self.details_input.setFixedHeight(100)

        # Boutons
        self.btn_enregistrer = QPushButton("💾 Enregistrer l'incident")
        self.btn_enregistrer.setFixedWidth(150)  # Réduire la largeur
        self.btn_enregistrer.setStyleSheet("margin: 5px auto;")  # Centrer le bouton
        self.btn_enregistrer.clicked.connect(self.enregistrer_incident)

        self.btn_retour = QPushButton("⬅️ Retour")
        self.btn_retour.setFixedWidth(150)  # Réduire la largeur
        self.btn_retour.setStyleSheet("margin: 5px auto;")  # Centrer le bouton
        self.btn_retour.clicked.connect(self.retourner)

        # Layout pour centrer les boutons
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter)  # Centrer horizontalement

        # Ajouter les boutons au layout centré
        btn_layout.addWidget(self.btn_enregistrer, alignment=Qt.AlignHCenter)
        btn_layout.addWidget(self.btn_retour, alignment=Qt.AlignHCenter)

        # Ajout au layout principal
        form_layout.addRow("Informations du contrat :", self.label_infos_contrat)
        form_layout.addRow("Informations du véhicule :", self.label_infos_vehicule)
        form_layout.addRow("Type d'incident :", self.type_incident_input)
        form_layout.addRow("Date de l'incident :", self.date_incident_input)
        form_layout.addRow("Coûts liés :", self.couts_input)
        form_layout.addRow("Détails :", self.details_input)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)  # Ajouter le layout des boutons centrés
        self.setLayout(layout)

    def enregistrer_incident(self):
        """
        Vérifie les champs et envoie les données à la BD.
        """
        type_incident = self.type_incident_input.currentText()
        date_incident = self.date_incident_input.date().toString("yyyy-MM-dd")
        couts_str = self.couts_input.text().strip().replace(",", ".")
        details = self.details_input.toPlainText().strip()

        if type_incident == "Sélectionner un type d'incident" or not couts_str or not details:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            couts = float(couts_str)
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le champ 'Coûts' doit être un nombre valide.")
            return

        success = ajouter_incident(
            type_incident,
            date_incident,
            couts,
            details,
            self.id_contrat
        )

        if success == True:
            QMessageBox.information(self, "Succès", "Incident enregistré avec succès.")
            self.retourner()
        elif success == "incident_existe":
            QMessageBox.warning(self, "Attention", "Un incident est déjà enregistré pour ce contrat.")
        else:
            QMessageBox.critical(self, "Erreur", "L'enregistrement de l'incident a échoué.")


    def retourner(self):
        """
        Retourne à l’interface précédente.
        """
        if self.retour_widget:
            if hasattr(self.retour_widget, 'tb_in_recharger_tableau'):
                self.retour_widget.tb_in_recharger_tableau()
            self.main_window.central_widget.setCurrentWidget(self.retour_widget)
        else:
            if hasattr(self.main_window, 'ui_gestion_contrats'):
                self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_contrats)
