# ui_styles_agences.py

# StyleSheet pour les boutons
BUTTON_STYLE = """
    QPushButton {
        background-color: #007BFF; 
        color: white; 
        padding: 12px; 
        border-radius: 6px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #0056b3;
    }
"""

# StyleSheet pour le cadre principal (Card Visuel)
FRAME_STYLE = """
    QFrame {
        background-color: white; 
        border-radius: 10px; 
        padding: 20px;
        border: 1px solid #D1D1D1;
    }
"""

# StyleSheet pour le titre principal
TITLE_STYLE = """
    QLabel {
        font-size: 22px;
        font-weight: bold;
        color: #333;
    }
"""

# StyleSheet pour les boutons financiers
BUTTON_STYLE_FINANCE = """
    QPushButton {
        background-color: #4169E1; 
        color: white; 
        padding: 12px; 
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #40E0D0;
    }
"""

# StyleSheet pour les boutons clients
BUTTON_STYLE_CLIENTS = """
    QPushButton {
        background-color: #0F52BA; 
        color: white; 
        padding: 12px; 
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #40E0D0;
    }
"""

# StyleSheet pour les boutons opérations
BUTTON_STYLE_OPERATIONS = """
    QPushButton {
        background-color: #000080 ; 
        color: white; 
        padding: 12px; 
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #40E0D0;
    }
"""

# StyleSheet pour le bouton retour
BUTTON_STYLE_RETOUR = """
    QPushButton {
        background-color: #6c757d; 
        color: white; 
        padding: 12px; 
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        width: 250px;
    }
    QPushButton:hover {
        background-color: #5a6268;
    }
"""

FORMULAIRE_FIELDS_STYLE = """
    QLineEdit, QComboBox {
        min-height: 20px;
        font-size: 12px;
    }
"""
