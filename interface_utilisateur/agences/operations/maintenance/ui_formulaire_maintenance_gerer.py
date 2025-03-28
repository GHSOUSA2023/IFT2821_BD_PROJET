import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout,
    QDateEdit, QTextEdit, QMessageBox, QApplication, QComboBox
)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QKeyEvent
from fonctions_gestion.flotte import get_infos_maint_vehicule_par_id_maint, ajouter_maintenance, terminer_maintenance
from fonctions_gestion.employes import lister_employes
from constantes import constantes
from fonctions_gestion.vehicules import lister_tous_vehicules


class CustomDateEdit(QDateEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.ouvrir_calendrier)

    def ouvrir_calendrier(self):
        event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Down, Qt.AltModifier)
        QApplication.postEvent(self, event)


class FormulaireMaintenanceGererUI(QWidget):
    def __init__(self, main_window, id_vehicule, retour_widget):
        super().__init__()
        self.main_window = main_window
        self.id_vehicule = id_vehicule
        self.retour_widget = retour_widget
        self.setWindowTitle("Créer ou terminer une maintenance")
        self.setGeometry(100, 100, 600, 650)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        vehicule_info = get_infos_maint_vehicule_par_id_maint(self.id_vehicule)

        self.infos_vehicule_label = QLabel(f"""
Agence: {vehicule_info['NOM_AGENCE']}
Marque: {vehicule_info['MARQUE']}
Modèle: {vehicule_info['MODELE']}
Année: {vehicule_info['ANNEE_FABRICATION']}
Couleur: {vehicule_info['COULEUR']}
Kilométrage: {vehicule_info['KILOMETRAGE']} km
Immatriculation: {vehicule_info['IMMATRICULATION']}
Type carburant: {vehicule_info['TYPE_CARBUR']}
Type véhicule: {vehicule_info['TYPE_VEHIC']}
""")

        self.date_debut_input = CustomDateEdit()
        self.date_debut_input.setCalendarPopup(True)
        self.date_debut_input.setMinimumDate(QDate.currentDate())
        self.date_debut_input.dateChanged.connect(self.mettre_a_jour_date_fin_minimale)

        self.date_fin_input = CustomDateEdit()
        self.date_fin_input.setCalendarPopup(True)
        self.date_fin_input.setSpecialValueText("Sélectionner une date")
        self.date_fin_input.setMinimumDate(QDate.currentDate())

        # ⬇️ Charger les dates à partir de la base de données
        if vehicule_info['DATE_MAINTEN']:
            dt = vehicule_info['DATE_MAINTEN']
            self.date_debut_input.setDate(QDate(dt.year, dt.month, dt.day))
        else:
            self.date_debut_input.setDate(QDate.currentDate())

        if vehicule_info['DATE_MAINTEN_FIN']:
            dtf = vehicule_info['DATE_MAINTEN_FIN']
            self.date_fin_input.setDate(QDate(dtf.year, dtf.month, dtf.day))

        # ⬇️ Type de maintenance
        self.type_maintenance_input = QComboBox()
        self.type_maintenance_input.addItem("Sélectionner un type de maintenance")
        for t in constantes.TYPES_MAINTENANCE:
            self.type_maintenance_input.addItem(t)
        if vehicule_info['TYPE_MAINTEN']:
            index = self.type_maintenance_input.findText(vehicule_info['TYPE_MAINTEN'])
            if index != -1:
                self.type_maintenance_input.setCurrentIndex(index)

        # ⬇️ Mécanicien
        self.mecanicien_input = QComboBox()
        self.mecanicien_input.addItem("Sélectionner un mécanicien", None)
        for emp in lister_employes():
            id_emp, nom = emp[0], emp[2]
            self.mecanicien_input.addItem(f"{id_emp} - {nom}", id_emp)
            if vehicule_info['ID_EMP'] == id_emp:
                self.mecanicien_input.setCurrentIndex(self.mecanicien_input.count() - 1)

        # ⬇️ Description
        self.desc_maintenance = QTextEdit()
        self.desc_maintenance.setPlaceholderText("Entrez ici la description de la maintenance...")
        self.desc_maintenance.setFixedHeight(120)
        if vehicule_info['DESC_MAINTEN']:
            self.desc_maintenance.setPlainText(vehicule_info['DESC_MAINTEN'])

        # ⬇️ Boutons
        #self.btn_enregistrer = QPushButton("💾 Enregistrer maintenance (EN MAINTENANCE)")
        #self.btn_enregistrer.clicked.connect(self.enregistrer_maintenance)

        self.btn_terminer = QPushButton("✅ Terminer la maintenance")
        self.btn_terminer.clicked.connect(self.terminer_maintenance)

        self.btn_retour = QPushButton("🔙 Retour")
        self.btn_retour.clicked.connect(self.retourner)

        # ⬇️ Ajout au layout
        form_layout.addRow("Informations du véhicule :", self.infos_vehicule_label)
        form_layout.addRow("Date début :", self.date_debut_input)
        form_layout.addRow("Date fin prévue :", self.date_fin_input)
        form_layout.addRow("Type de maintenance :", self.type_maintenance_input)
        form_layout.addRow("Mécanicien :", self.mecanicien_input)
        form_layout.addRow("Description :", self.desc_maintenance)

        layout.addLayout(form_layout)
        #layout.addWidget(self.btn_enregistrer)
        layout.addWidget(self.btn_terminer)
        layout.addWidget(self.btn_retour)
        self.setLayout(layout)

    def enregistrer_maintenance(self):
        description = self.desc_maintenance.toPlainText().strip()
        type_maintenance = self.type_maintenance_input.currentText()
        id_emp = self.mecanicien_input.currentData()

        if not description or type_maintenance == "Sélectionner un type de maintenance" or id_emp is None:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        success = ajouter_maintenance(
            self.id_vehicule,
            id_emp,
            type_maintenance,
            self.date_debut_input.date().toString("yyyy-MM-dd"),
            description,
            "EN MAINTENANCE"
        )

        if success:
            QMessageBox.information(self, "Succès", "Maintenance enregistrée avec statut EN MAINTENANCE.")
            self.retourner()
        else:
            QMessageBox.critical(self, "Erreur", "L'enregistrement de la maintenance a échoué.")

    def terminer_maintenance(self):
        date_fin = self.date_fin_input.date()
        date_debut = self.date_debut_input.date()

        if not date_fin.isValid():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une date de fin.")
            return
        if date_fin < date_debut:
            QMessageBox.warning(self, "Erreur", "La date de fin ne peut pas être antérieure à la date de début.")
            return
        description = self.desc_maintenance.toPlainText().strip()
        if not description:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une description de la maintenance.")
            return

        terminer_maintenance(
            self.id_vehicule,
            date_fin.toString("yyyy-MM-dd"),
            description
        )

        QMessageBox.information(self, "Succès", "Maintenance terminée avec succès.")
        self.retourner()

    def mettre_a_jour_date_fin_minimale(self):
        date_debut = self.date_debut_input.date()
        if date_debut.isValid():
            self.date_fin_input.setMinimumDate(date_debut)

    def retourner(self):
        if self.retour_widget:
            if hasattr(self.retour_widget, 'tb_mt_recharger_tableau'):
                self.retour_widget.tb_mt_recharger_tableau()
            self.main_window.central_widget.setCurrentWidget(self.retour_widget)
        else:
            if hasattr(self.main_window, 'ui_gestion_vehicules'):
                self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_vehicules)
