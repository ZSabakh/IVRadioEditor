from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from ui.widgets import StyledProgressBar
from ui.styles import BUTTON_STYLE, PROGRESS_BAR_STYLE


class ProgressPage(QWidget):
    def __init__(self, on_cancel: object) -> None:
        super().__init__()
        self.on_cancel = on_cancel

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Replacing song, please wait...", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; color: #FFC107;")
        self.layout.addWidget(title)

        self.progress_bar = StyledProgressBar(PROGRESS_BAR_STYLE)
        self.layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.on_cancel)
        cancel_button.setFixedWidth(100)
        cancel_button.setStyleSheet(BUTTON_STYLE)
        self.layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
