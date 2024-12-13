from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from pydub import AudioSegment

from ui.pages.intro import IntroPage
from ui.pages.radio_select import RadioSelectPage
from ui.pages.song_select import SongSelectPage
from ui.pages.replace import ReplacePage
from ui.pages.progress import ProgressPage
from replace_audio.replace_audio import replace_special_audio
from update_length.update_song_length import update_song_length
from utils import install_ffmpeg, check_ffmpeg
from pyrpfiv import RPFParser
import os
import shutil
from PySide6.QtCore import QThread, Signal


class ReplaceSongWorker(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, gtaiv_path, selected_radio, selected_song, new_song_path):
        super().__init__()
        self.gtaiv_path = gtaiv_path
        self.selected_radio = selected_radio
        self.selected_song = selected_song
        self.new_song_path = new_song_path

    def run(self):
        try:
            print("Worker started")
            rpf_path = os.path.join(self.gtaiv_path, "pc/audio/sfx", self.selected_radio)
            radio_name = self.selected_radio[:-4].upper()
            full_song_path = f"{radio_name}/{self.selected_song}"
            print(f"RPF Path: {rpf_path}")
            print(f"Full Song Path: {full_song_path}")

            parser = RPFParser(rpf_path, os.path.join(self.gtaiv_path, "GTAIV.exe"))
            output_folder = "temp_extracted"
            os.makedirs(output_folder, exist_ok=True)
            parser.extract_file(full_song_path, output_folder)

            extracted_file = os.path.join(output_folder, self.selected_song)

            self.progress.emit(25)
            print("Progress 25%")

            replace_special_audio(extracted_file, self.new_song_path)
            self.progress.emit(50)
            print("Progress 50%")

            audio = AudioSegment.from_file(self.new_song_path)
            new_song_length = int(audio.duration_seconds * 1000)
            update_song_length(self.gtaiv_path, radio_name, self.selected_song, new_song_length)
            self.progress.emit(75)
            print("Progress 75%")

            parser.add_file(extracted_file, full_song_path)

            shutil.rmtree(output_folder)
            self.progress.emit(100)
            print("Progress 100%")
            self.finished.emit()
        except Exception as e:
            print(f"Worker encountered an error: {e}")
            self.error.emit(str(e))


class GTAIVEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gtaiv_path = ""
        self.selected_radio = ""
        self.selected_song = ""
        self.new_song_path = ""
        self.worker = None

        self.song_select_page = None
        self.radio_select_page = None
        self.intro_page = IntroPage(on_next=self.goto_radio_select)
        self.replace_page = None
        self.progress_page = ProgressPage(on_cancel=self.cancel_replace)

        self.setWindowTitle("GTA IV Radio Editor")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_ui()

    def init_ui(self):
        self.stack.addWidget(self.intro_page)
        self.stack.addWidget(self.progress_page)
        self.stack.setCurrentWidget(self.intro_page)

    def start_replace(self, new_song_path):
        self.new_song_path = new_song_path

        if not check_ffmpeg():
            if not install_ffmpeg(self):
                QMessageBox.critical(
                    self,
                    "Error",
                    "FFmpeg is required for audio processing. The operation cannot continue without it.",
                    QMessageBox.Ok
                )
                return

        self.worker = ReplaceSongWorker(
            self.gtaiv_path, self.selected_radio, self.selected_song, self.new_song_path
        )

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_replace_finished)
        self.worker.error.connect(self.on_replace_error)

        self.worker.start()
        self.stack.setCurrentWidget(self.progress_page)

    def goto_radio_select(self, gtaiv_path):
        self.gtaiv_path = gtaiv_path
        self.radio_select_page = RadioSelectPage(
            gtaiv_path=self.gtaiv_path,
            on_next=self.goto_song_select,
            on_back=self.goto_intro
        )
        self.stack.addWidget(self.radio_select_page)
        self.stack.setCurrentWidget(self.radio_select_page)

    def goto_intro(self):
        self.stack.setCurrentWidget(self.intro_page)

    def goto_song_select(self, selected_radio):
        self.selected_radio = selected_radio
        self.song_select_page = SongSelectPage(
            gtaiv_path=self.gtaiv_path,
            selected_radio=self.selected_radio,
            on_next=self.goto_replace,
            on_back=self.goto_radio_select_back
        )
        self.stack.addWidget(self.song_select_page)
        self.stack.setCurrentWidget(self.song_select_page)

    def goto_radio_select_back(self):
        self.stack.setCurrentWidget(self.radio_select_page)

    def goto_replace(self, selected_song):
        self.selected_song = selected_song
        self.replace_page = ReplacePage(
            selected_song=self.selected_song,
            on_replace=self.start_replace,
            on_back=self.goto_song_select_back
        )
        self.stack.addWidget(self.replace_page)
        self.stack.setCurrentWidget(self.replace_page)

    def goto_song_select_back(self):
        self.stack.setCurrentWidget(self.song_select_page)

    def update_progress(self, value):
        self.progress_page.update_progress(value)

    def on_replace_finished(self):
        self.progress_page.update_progress(100)
        QMessageBox.information(self, "Success", "The song was successfully replaced!")
        self.stack.setCurrentWidget(self.intro_page)

    def on_replace_error(self, message):
        QMessageBox.critical(self, "Error", f"An error occurred: {message}", QMessageBox.StandardButton.Ok,
                             QMessageBox.StandardButton.NoButton)
        self.stack.setCurrentWidget(self.replace_page)

    def cancel_replace(self):
        QMessageBox.information(self, "Cancelled", "The replacement operation has been cancelled.")
        if self.worker is not None:
            self.worker.terminate()
            self.worker = None
        self.stack.setCurrentWidget(self.intro_page)
