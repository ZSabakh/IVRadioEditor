import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import GTAIVEditor
from qt_material import apply_stylesheet


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

    editor = GTAIVEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
