import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QToolButton, QButtonGroup, \
    QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon

from ui.styles import TOOL_BUTTON_STYLE, SCROLL_AREA_STYLE, BUTTON_STYLE
from utils import resource_path


class RadioSelectPage(QWidget):
    def __init__(self, gtaiv_path, on_next, on_back):
        super().__init__()
        self.gtaiv_path = gtaiv_path
        self.on_next = on_next
        self.on_back = on_back

        self.selected_radio = ""

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Select a Radio", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFC107;")
        self.layout.addWidget(title)

        self.radio_grid_widget = QWidget(self)
        self.radio_grid_layout = QGridLayout(self.radio_grid_widget)
        self.radio_grid_layout.setSpacing(20)
        self.radio_grid_layout.setContentsMargins(20, 20, 20, 20)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.radio_grid_widget)
        self.scroll_area.setStyleSheet(SCROLL_AREA_STYLE)
        self.layout.addWidget(self.scroll_area)

        buttons_layout = QHBoxLayout()

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.on_back)
        self.back_button.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.proceed)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(self.next_button)

        self.layout.addLayout(buttons_layout)

        self.radio_files = []
        self.radio_buttons = {}
        self.radio_button_group = QButtonGroup(self)
        self.radio_button_group.setExclusive(True)
        self.radio_button_group.buttonClicked.connect(self.radio_selected)

        self.load_radio_files()

    def load_radio_files(self):
        sfx_path = os.path.abspath(os.path.join(self.gtaiv_path, "pc/audio/sfx"))
        self.radio_files = [
            f for f in os.listdir(sfx_path) if f.startswith("radio_") and f.endswith(".rpf")
        ]

        if not self.radio_files:
            QMessageBox.warning(self, "No Radios Found", "No radio files found in the specified directory.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.NoButton)
            return

        icon_size = QSize(120, 120)
        button_size = QSize(180, 180)

        for index, radio_file in enumerate(self.radio_files):
            radio_name = radio_file[:-4]
            icon_path = resource_path(os.path.join('assets', 'radio', f"{radio_name}.png"))

            button = QToolButton(self)
            button.setText(radio_name.replace('radio_', '').upper())

            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path).scaled(icon_size, Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation)
                icon_img = QIcon(pixmap)
                button.setIcon(icon_img)
                button.setIconSize(icon_size)
            else:
                button.setIcon(QIcon(":/icons/radio_default.png"))  # Fallback icon

            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            button.setFixedSize(button_size)
            button.setCheckable(True)
            button.setStyleSheet(TOOL_BUTTON_STYLE)

            self.radio_button_group.addButton(button)
            self.radio_buttons[radio_name] = button

            row, column = divmod(index, 3)
            self.radio_grid_layout.addWidget(button, row, column)

    def radio_selected(self, button):
        for radio_name, btn in self.radio_buttons.items():
            if btn == button:
                self.selected_radio = radio_name + ".rpf"
                break

        self.next_button.setEnabled(True)

    def proceed(self):
        if not self.selected_radio:
            QMessageBox.warning(self, "No Radio Selected", "Please select a radio to proceed.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.NoButton)
            return

        self.on_next(self.selected_radio)
