import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt

from ui.styles import BUTTON_STYLE, LINE_EDIT_STYLE


class IntroPage(QWidget):
    def __init__(self, on_next):
        super().__init__()
        self.on_next = on_next

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Enter the GTA IV installation directory...")
        self.path_input.setFixedWidth(400)
        self.path_input.setStyleSheet(LINE_EDIT_STYLE)
        self.layout.addWidget(self.path_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_directory)
        self.browse_button.setFixedWidth(100)
        self.browse_button.setStyleSheet(BUTTON_STYLE)
        self.layout.addWidget(self.browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.validate_and_proceed)
        self.next_button.setFixedWidth(100)
        self.next_button.setStyleSheet(BUTTON_STYLE)
        self.layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def browse_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select GTA IV Directory")
        if path:
            self.path_input.setText(path)

    def validate_and_proceed(self):
        gtaiv_path = self.path_input.text().strip()
        if not os.path.isdir(gtaiv_path) or not os.path.exists(os.path.join(gtaiv_path, "pc/audio/sfx")):
            QMessageBox.warning(self, "Invalid Path", "Invalid GTA IV directory. Please try again.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.NoButton)
            return
        self.on_next(gtaiv_path)
