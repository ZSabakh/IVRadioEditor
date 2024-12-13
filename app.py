import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.main_window import GTAIVEditor
from qt_material import apply_stylesheet
from utils import check_ffmpeg, install_ffmpeg


class SplashWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GTA IV Radio Editor")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #121212;")


def main():
    app = QApplication(sys.argv)

    extra = {
        'density_scale': '-2',
        'font_family': 'Montserrat',
        'primaryTextColor': '#FFFFFF',
        'secondaryTextColor': '#B0BEC5',
        'primaryColor': '#000000',
        'secondaryColor': '#424242',
        'accentColor': '#FFC107',
        'backgroundColor': '#121212',
        'windowColor': '#121212',
        'dialogColor': '#212121',
        'borderColor': '#424242',
        'hoverColor': '#FFC107',
        'focusColor': '#FFC107',
        'buttonBackgroundColor': '#FFC107',
        'buttonForegroundColor': '#000000',
        'buttonBorderColor': '#FFC107',
    }

    apply_stylesheet(app, theme='dark_cyan.xml', extra=extra)

    splash = SplashWindow()
    splash.show()

    if not check_ffmpeg():
        if not install_ffmpeg(splash):
            sys.exit(1)

    editor = GTAIVEditor()
    editor.show()
    splash.close()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
