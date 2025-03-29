from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox, QFrame
from fonctions_gestion.vehicules import ajouter_vehicule, modifier_vehicule
from fonctions_gestion.flotte import lister_marques, lister_tout_modeles, lister_tout_tp_vehic
from constantes import constantes
from fonctions_gestion.agences import lister_tout_agences  # Pour récupérer les agences
from interface_utilisateur.agences.ui_styles_agences import FORMULAIRE_FIELDS_STYLE
from interface_utilisateur.agences.operations.maintenance.ui_formulaire_maintenance import FormulaireMaintenanceUI
from PyQt5.QtCore import Qt

class FormulaireVehiculeUI(QWidget):
    """
    Interface du formulaire pour ajouter ou modifier un véhicule.
    """
    def __init__(self, main_window, mode="ajouter", vehicule=None, retour_widget=None):
        super().__init__()
        # Empêche l'héritage du background depuis le parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Remplit le fond avec la palette courante et définit le background en blanc
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-image: none; background-color: white;")
        self.setPalette(self.style().standardPalette())

        self.main_window = main_window
        self.mode = mode
        self.vehicule = vehicule  # Stocker les données du véhicule si en mode modification (dictionnaire)
        self.retour_widget = retour_widget
        self.setWindowTitle("Ajouter / Modifier un Véhicule")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet(FORMULAIRE_FIELDS_STYLE)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Champs du formulaire
        self.immatriculation_input = QLineEdit()
        self.annee_input = QLineEdit()
        self.couleur_input = QLineEdit()
        self.km_input = QLineEdit()

        self.marque_input = QComboBox()
        self.modele_input = QComboBox()
        self.type_input = QComboBox()
        self.carburant_input = QComboBox()
        self.agence_input = QComboBox()
        self.status_label = QLabel("DISPONIBLE")  # Statut affiché seulement

        # Charger les marques
        self.marque_input.addItem("Sélectionner une marque")
        for marque in lister_marques():
            self.marque_input.addItem(marque[1], marque[0])  # (Nom, ID)

        # Charger les modèles
        self.modele_input.addItem("Sélectionner un modèle")
        for modele in lister_tout_modeles():
            self.modele_input.addItem(modele[1], modele[0])  # (Nom, ID)

        # Charger les types de véhicules
        self.type_input.addItem("Sélectionner un type")
        for type_veh in lister_tout_tp_vehic():
            self.type_input.addItem(type_veh[1], type_veh[0])  # (Nom, ID)

        # Charger les types de carburant
        self.carburant_input.addItem("Sélectionner un carburant")
        for carburant in constantes.TYPES_CARBURANT:
            self.carburant_input.addItem(carburant)

        # Charger les agences
        agences = lister_tout_agences()
        self.agence_input.addItem("Sélectionner une agence", None)
        for agence in agences:
            self.agence_input.addItem(f"{agence[0]} - {agence[1]}", agence[0])

        # Si mode modification, remplir les champs avec les valeurs existantes depuis le dictionnaire
        if self.mode == "modifier" and self.vehicule:
            self.immatriculation_input.setText(self.vehicule['IMMATRICULATION'])
            self.annee_input.setText(str(self.vehicule['ANNEE_FAB']))
            self.couleur_input.setText(self.vehicule['COULEUR'])
            self.km_input.setText(str(self.vehicule['KM']))

            self.marque_input.setCurrentIndex(self.marque_input.findText(self.vehicule['MARQUE']))
            self.modele_input.setCurrentIndex(self.modele_input.findText(self.vehicule['MODELE']))
            self.type_input.setCurrentIndex(self.type_input.findText(self.vehicule['TYPE_VEHIC']))
            self.carburant_input.setCurrentIndex(self.carburant_input.findText(self.vehicule['TYPE_CARBUR']))
            # Correction pour sélectionner l'agence dans le combo
            for i in range(self.agence_input.count()):
                if self.vehicule['NOM_AGENCE'] in self.agence_input.itemText(i):
                    self.agence_input.setCurrentIndex(i)
                    break


        # Ajouter les champs au formulaire
        form_layout.addRow("Immatriculation:", self.immatriculation_input)
        form_layout.addRow("Année de fabrication:", self.annee_input)
        form_layout.addRow("Couleur:", self.couleur_input)
        form_layout.addRow("Kilométrage:", self.km_input)
        form_layout.addRow("Marque:", self.marque_input)
        form_layout.addRow("Modèle:", self.modele_input)
        form_layout.addRow("Type de véhicule:", self.type_input)
        form_layout.addRow("Carburant:", self.carburant_input)
        #form_layout.addRow("Statut:", self.status_label)
        form_layout.addRow("Agence:", self.agence_input)

        # Cadre pour mise en maintenance
        maintenance_frame = QFrame()
        maintenance_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
                background-color: #f9f9f9;
            }
        """)
        maintenance_layout = QVBoxLayout()

        self.btn_maintenance = QPushButton("🛠 Mettre ce véhicule en maintenance")
        self.btn_maintenance.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        self.btn_maintenance.clicked.connect(self.mettre_en_maintenance)

        maintenance_layout.addWidget(self.btn_maintenance)
        maintenance_frame.setLayout(maintenance_layout)
        form_layout.addRow("", maintenance_frame)

        # Boutons Sauvegarder / Effacer / Annuler
        self.btn_sauvegarder = QPushButton("💾 Sauvegarder")
        self.btn_effacer = QPushButton("🧹 Effacer")
        self.btn_annuler = QPushButton("❌ Annuler")

        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        self.btn_effacer.clicked.connect(self.effacer_formulaire)
        self.btn_annuler.clicked.connect(self.annuler)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_sauvegarder)
        btn_layout.addWidget(self.btn_effacer)
        btn_layout.addWidget(self.btn_annuler)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def mettre_en_maintenance(self):
        
        if self.mode == "modifier" and self.vehicule:
            status = self.vehicule.get('STATUS')

            if not status or status.strip().upper() != 'DISPONIBLE':
                QMessageBox.warning(self, "Information", "Cet vehicule déjà est en maintenance.")
                return

            # Se passou na verificação, abre o formulário
            formulaire_maintenance = FormulaireMaintenanceUI(
                self.main_window,
                self.vehicule['ID_VEHIC'],
                self.retour_widget
            )
            self.main_window.central_widget.addWidget(formulaire_maintenance)
            self.main_window.central_widget.setCurrentWidget(formulaire_maintenance)
        else:
            QMessageBox.warning(self, "Information", "Vous devez etre en mode modification par acceder a maintenance.")





    def sauvegarder(self):
        """Enregistre les données en fonction du mode (ajouter/modifier)."""
        immatriculation = self.immatriculation_input.text().strip()
        couleur = self.couleur_input.text().strip()
        annee_text = self.annee_input.text().strip()
        km_text = self.km_input.text().strip()

        if not immatriculation or not couleur or not annee_text or not km_text:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            annee_fab = int(annee_text)
            km = int(km_text)
        except ValueError:
            QMessageBox.warning(self, "Erreur", "L'année de fabrication et le kilométrage doivent être des nombres valides.")
            return

        type_carbur = self.carburant_input.currentText()
        id_marq = self.marque_input.currentData()
        id_mod = self.modele_input.currentData()
        id_tp_vehic = self.type_input.currentData()
        id_age = self.agence_input.currentData()
        status = "DISPONIBLE"

        if self.mode == "ajouter":
            ajouter_vehicule(id_marq, id_mod, id_tp_vehic, annee_fab, couleur, immatriculation, status, km, type_carbur, id_age)
        elif self.mode == "modifier":
            id_vehicule = self.vehicule['ID_VEHIC']
            modifier_vehicule(id_vehicule, id_marq, id_mod, id_tp_vehic, annee_fab, couleur, immatriculation, status, km, type_carbur, id_age)

        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_vehicules)



    def effacer_formulaire(self):
        """Efface tous les champs du formulaire."""
        self.immatriculation_input.clear()
        self.annee_input.clear()
        self.couleur_input.clear()
        self.km_input.clear()
        self.marque_input.setCurrentIndex(0)
        self.modele_input.setCurrentIndex(0)
        self.type_input.setCurrentIndex(0)
        self.carburant_input.setCurrentIndex(0)
        self.agence_input.setCurrentIndex(0)

    def annuler(self):
        """Annule l'action et retourne à la gestion des véhicules."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_vehicules)
