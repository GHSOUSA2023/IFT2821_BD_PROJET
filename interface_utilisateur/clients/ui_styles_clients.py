# ui_styles_clients.py

# StyleSheet pour les boutons (déjà existant)
BUTTON_STYLE = """
    QPushButton {
        background-color: #28A745; 
        color: white; 
        padding: 12px; 
        border-radius: 6px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #218838;
    }
"""

# StyleSheet pour le titre principal (déjà existant)
TITLE_STYLE = """
    QLabel {
        font-size: 20px;
        font-weight: bold;
        color: #333;
    }
"""

# StyleSheet pour le cadre (ajouter ceci)
FRAME_STYLE = """
    QFrame {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 20px;
    }
"""
