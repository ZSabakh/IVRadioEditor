from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, \
    QMessageBox
from PySide6.QtCore import Qt
from ui.styles import BUTTON_STYLE, LINE_EDIT_STYLE


class ReplacePage(QWidget):
    def __init__(self, selected_song, on_replace, on_back):
        super().__init__()
        self.selected_song = selected_song
        self.on_replace = on_replace
        self.on_back = on_back

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel(f"Replace {self.selected_song}", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFC107;")
        self.layout.addWidget(title)

        self.new_song_input = QLineEdit(self)
        self.new_song_input.setPlaceholderText("Select the new song file...")
        self.new_song_input.setFixedWidth(400)
        self.new_song_input.setStyleSheet(LINE_EDIT_STYLE)
        self.layout.addWidget(self.new_song_input, alignment=Qt.AlignmentFlag.AlignCenter)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setFixedWidth(100)
        browse_button.setStyleSheet(BUTTON_STYLE)
        self.layout.addWidget(browse_button, alignment=Qt.AlignmentFlag.AlignCenter)

        buttons_layout = QHBoxLayout()

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.on_back)
        back_button.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(back_button)

        replace_button = QPushButton("Replace", self)
        replace_button.clicked.connect(self.replace)
        replace_button.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(replace_button)

        self.layout.addLayout(buttons_layout)

    def browse_file(self):
        new_song_path, _ = QFileDialog.getOpenFileName(self, "Select New Song", filter="Audio Files (*.mp3 *.wav)")
        if new_song_path:
            self.new_song_input.setText(new_song_path)

    def replace(self):
        new_song_path = self.new_song_input.text().strip()
        if not new_song_path:
            QMessageBox.warning(self, "Invalid File", "Please select a valid audio file.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.NoButton)
            return

        self.on_replace(new_song_path)
