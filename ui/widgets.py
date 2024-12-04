from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class StyledProgressBar(QProgressBar):
    def __init__(self, style_sheet, width=400):
        super().__init__()
        self.setValue(0)
        self.setFixedWidth(width)
        self.setStyleSheet(style_sheet)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


def load_custom_font(font_path):
    from PySide6.QtGui import QFontDatabase
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return QFont(family)
    else:
        raise RuntimeError(f"Failed to load font from {font_path}")
