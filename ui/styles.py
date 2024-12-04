BUTTON_STYLE = """
    QPushButton {
        background-color: #FFC107;
        color: #000000;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #FFD54F;
    }
    QPushButton:pressed {
        background-color: #FFA000;
    }
"""

LINE_EDIT_STYLE = """
    QLineEdit {
        background-color: #2A2A2A;
        border: 2px solid #424242;
        border-radius: 4px;
        padding: 8px;
        color: white;
    }
    QLineEdit:focus {
        border: 2px solid #FFC107;
    }
"""

SCROLL_AREA_STYLE = """
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    QScrollBar:vertical {
        background-color: #2A2A2A;
        width: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background-color: #424242;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #FFC107;
    }
"""

SONG_LIST_STYLE = """
    QListWidget {
        background-color: #2A2A2A;
        border: 2px solid #424242;
        border-radius: 4px;
        color: white;
    }
    QListWidget::item {
        padding: 8px;
    }
    QListWidget::item:selected {
        background-color: #424242;
        color: white;
    }
    QListWidget::item:hover {
        background-color: #383838;
    }
"""

TOOL_BUTTON_STYLE = """
    QToolButton {
        background-color: #2A2A2A;
        color: white;
        border: 2px solid #424242;
        border-radius: 8px;
        padding: 8px;
        font-weight: bold;
    }
    QToolButton:checked {
        background-color: #424242;
        border: 2px solid #FFC107;
    }
    QToolButton:hover {
        background-color: #383838;
    }
"""

PROGRESS_BAR_STYLE = """
    QProgressBar {
        background-color: #2A2A2A;
        border: 2px solid #424242;
        border-radius: 4px;
        color: black;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #FFC107;
        border-radius: 2px;
    }
"""
