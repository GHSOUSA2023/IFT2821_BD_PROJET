from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from interface_utilisateur.agences.ui_styles_agences import (
    FRAME_STYLE, TITLE_STYLE,
    BUTTON_STYLE_FINANCE, BUTTON_STYLE_CLIENTS,
    BUTTON_STYLE_OPERATIONS, BUTTON_STYLE_RETOUR
)
from interface_utilisateur.tableaux.ui_tableau_rapports import TableauRapportsUI
from fonctions_gestion.rapports import (
    rapport_flotte_vehicules,
    rapport_clients_incidents_assurance,
    rapport_vehicules_incidents,
    rapport_vehicules_disponibles_par_agence,
    rapport_entretien_par_agence,
    rapport_vehicules_contrats_actifs,
    rapport_employes_avec_incidents,
    rapport_reservations_agence_janvier,
    rapport_contrats_agence_janvier,
    rapport_facturation_agence_par_mois
)


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
        layout.setAlignment(Qt.AlignTop)

        label_title = QLabel("GESTION DES RAPPORTS")
        label_title.setStyleSheet(TITLE_STYLE)
        label_title.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        frame_layout = QVBoxLayout()

        # ---------- Section FINANCIER ----------
        label_finance = QLabel("Rapports Financiers")
        label_finance.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        frame_layout.addWidget(label_finance)

        btn_fin1 = QPushButton("Réservations par agence (janvier)")
        btn_fin1.clicked.connect(self.afficher_rapport_reservations_janvier)

        btn_fin2 = QPushButton("Contrats en cours par agence (janvier)")
        btn_fin2.clicked.connect(self.afficher_rapport_contrats_janvier)

        btn_fin3 = QPushButton("Facturation prévue et réalisée")
        btn_fin3.clicked.connect(self.afficher_rapport_facturation)

        for btn in [btn_fin1, btn_fin2, btn_fin3]:
            btn.setStyleSheet(BUTTON_STYLE_FINANCE)
            frame_layout.addWidget(btn)

        # ---------- Section CLIENTS ----------
        label_clients = QLabel("Rapports Clients")
        label_clients.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        frame_layout.addWidget(label_clients)

        btn_cli1 = QPushButton("Clients avec incidents d'assurance")
        btn_cli1.clicked.connect(self.afficher_rapport_clients_incidents)

        btn_cli2 = QPushButton("Clients avec contrats actifs")
        btn_cli2.clicked.connect(self.afficher_rapport_vehicules_contrats_actifs)

        for btn in [btn_cli1, btn_cli2]:
            btn.setStyleSheet(BUTTON_STYLE_CLIENTS)
            frame_layout.addWidget(btn)

        # ---------- Section OPÉRATIONS ----------
        label_ops = QLabel("Rapports Opérations")
        label_ops.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        frame_layout.addWidget(label_ops)

        btn_op1 = QPushButton("Flotte complète et contrats actifs")
        btn_op1.clicked.connect(self.afficher_rapport_flotte)

        btn_op2 = QPushButton("Véhicules disponibles par agence")
        btn_op2.clicked.connect(self.afficher_rapport_vehicules_disponibles)

        btn_op3 = QPushButton("Responsables de contrats avec incidents")
        btn_op3.clicked.connect(self.afficher_rapport_employes_incidents)

        btn_op4 = QPushButton("Véhicules avec incidents")
        btn_op4.clicked.connect(self.afficher_rapport_vehicules_incidents)

        btn_op5 = QPushButton("État d'entretien des véhicules")
        btn_op5.clicked.connect(self.afficher_rapport_entretien)

        for btn in [btn_op1, btn_op2, btn_op3, btn_op4, btn_op5]:
            btn.setStyleSheet(BUTTON_STYLE_OPERATIONS)
            frame_layout.addWidget(btn)

        # ---------- Botão de Retour ----------
        btn_retour = QPushButton("⬅ Retour")
        btn_retour.setStyleSheet(BUTTON_STYLE_RETOUR)
        btn_retour.clicked.connect(self.retourner)
        frame_layout.addWidget(btn_retour)

        frame.setLayout(frame_layout)
        layout.addWidget(label_title)
        layout.addWidget(frame)
        self.setLayout(layout)

    # ---------- Fonctions d’affichage des rapports ----------
    def afficher_rapport_flotte(self):
        colonnes, donnees = rapport_flotte_vehicules()
        self.afficher_tableau("Flotte complète et contrats actifs", colonnes, donnees)

    def afficher_rapport_clients_incidents(self):
        colonnes, donnees = rapport_clients_incidents_assurance()
        self.afficher_tableau("Clients avec incidents impactant l'assurance", colonnes, donnees)

    def afficher_rapport_vehicules_incidents(self):
        colonnes, donnees = rapport_vehicules_incidents()
        self.afficher_tableau("Véhicules ayant eu des incidents", colonnes, donnees)

    def afficher_rapport_vehicules_disponibles(self):
        colonnes, donnees = rapport_vehicules_disponibles_par_agence()
        self.afficher_tableau("Véhicules disponibles par agence", colonnes, donnees)

    def afficher_rapport_entretien(self):
        colonnes, donnees = rapport_entretien_par_agence()
        self.afficher_tableau("État d'entretien des véhicules par agence", colonnes, donnees)

    def afficher_rapport_vehicules_contrats_actifs(self):
        colonnes, donnees = rapport_vehicules_contrats_actifs()
        self.afficher_tableau("Véhicules avec contrats actifs", colonnes, donnees)

    def afficher_rapport_employes_incidents(self):
        colonnes, donnees = rapport_employes_avec_incidents()
        self.afficher_tableau("Employés ayant eu des incidents", colonnes, donnees)

    def afficher_rapport_reservations_janvier(self):
        colonnes, donnees = rapport_reservations_agence_janvier()
        self.afficher_tableau("Réservations par agence (janvier)", colonnes, donnees)

    def afficher_rapport_contrats_janvier(self):
        colonnes, donnees = rapport_contrats_agence_janvier()
        self.afficher_tableau("Contrats en cours par agence (janvier)", colonnes, donnees)

    def afficher_rapport_facturation(self):
        colonnes, donnees = rapport_facturation_agence_par_mois()
        self.afficher_tableau("Facturation prévue et réalisée par agence et mois", colonnes, donnees)

    def afficher_tableau(self, titre, colonnes, donnees):
        tableau = TableauRapportsUI(titre, colonnes, donnees, self.main_window, self)
        self.main_window.central_widget.addWidget(tableau)
        self.main_window.central_widget.setCurrentWidget(tableau)

    def retourner(self):
        """Retourner à l'écran principal."""
        self.main_window.central_widget.setCurrentWidget(self.main_window.ui_gestion_operations)
