import os
import json

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, \
    QMessageBox
from PySide6.QtCore import Qt
from ui.styles import BUTTON_STYLE, SONG_LIST_STYLE
from pyrpfiv import RPFParser
import qtawesome as qta


class SongSelectPage(QWidget):
    def __init__(self, gtaiv_path, selected_radio, on_next, on_back):
        super().__init__()
        self.gtaiv_path = gtaiv_path
        self.selected_radio = selected_radio
        self.on_next = on_next
        self.on_back = on_back

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Select a Song to Replace", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFC107;")
        self.layout.addWidget(title)

        self.song_list = QListWidget(self)
        self.song_list.setStyleSheet(SONG_LIST_STYLE)
        self.layout.addWidget(self.song_list)

        buttons_layout = QHBoxLayout()

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.on_back)
        self.back_button.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.proceed)
        self.next_button.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(self.next_button)

        self.layout.addLayout(buttons_layout)

        self.load_songs()

    def load_songs(self):
        rpf_path = os.path.abspath(os.path.join(self.gtaiv_path, "pc/audio/sfx", self.selected_radio))
        parser = RPFParser(rpf_path, os.path.abspath(os.path.join(self.gtaiv_path, "GTAIV.exe")))
        parser.save_json("radio_temp.json")

        with open("radio_temp.json", "r") as f:
            data = json.load(f)

        songs = []
        for directory in data.get("directories", []):
            if directory["name"].upper() == self.selected_radio[:-4].upper():
                for file in directory["files"]:
                    if not file["name"].startswith("ID_") and not file["name"].startswith("SOLO_"):
                        songs.append(file["name"])

        os.remove("radio_temp.json")

        if not songs:
            QMessageBox.warning(self, "No Songs Found", "No songs found in the selected radio.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.NoButton)
            return

        for song in songs:
            item = QListWidgetItem(song)
            item.setIcon(qta.icon('mdi.music-note',
                                  color='#FFC107'))
            self.song_list.addItem(item)

    def proceed(self):
        selected_item = self.song_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Song Selected", "Please select a song to replace.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.NoButton)
            return

        self.on_next(selected_item.text())
