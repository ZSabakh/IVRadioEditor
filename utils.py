import os
import sys
import subprocess
import urllib.request
import zipfile
import winreg
import ctypes
from PySide6.QtWidgets import QMessageBox, QProgressDialog
from PySide6.QtCore import Qt
from ui.styles import MESSAGE_BOX_STYLE, PROGRESS_DIALOG_STYLE


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def is_admin():
    """Check if the program has admin rights"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart_as_admin():
    """Restart the current program with admin rights"""
    try:
        if hasattr(sys, '_MEIPASS'):  
            script = sys.executable
        else: 
            script = sys.argv[0]
        
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable,
            script,
            None, 
            1
        )
        return True
    except Exception as e:
        print(f"Failed to restart as admin: {e}")
        return False


def check_ffmpeg():
    """Check if FFmpeg is available in the system PATH"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def set_system_path_env(new_path):
    """Add FFmpeg to system PATH (requires admin rights)"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 0, winreg.KEY_ALL_ACCESS) as key:
            current_path = winreg.QueryValueEx(key, 'Path')[0]
            if new_path not in current_path:
                new_path_value = current_path + ';' + new_path
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path_value)
                subprocess.run(['setx', 'PATH', new_path_value], capture_output=True)
        return True
    except Exception as e:
        print(f"Error setting PATH: {e}")
        return False


class DownloadProgressDialog(QProgressDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Installing FFmpeg")
        self.setLabelText("Downloading FFmpeg...")
        self.setCancelButton(None)  
        self.setWindowModality(Qt.WindowModal)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(300, 100)
        self.setStyleSheet(PROGRESS_DIALOG_STYLE)

    def urlretrieve_callback(self, count, block_size, total_size):
        if total_size > 0:
            percent = int(count * block_size * 100 / total_size)
            self.setValue(min(percent, 100))


def install_ffmpeg(parent_window=None):
    """Download and install FFmpeg"""
    if not check_ffmpeg():
        msg_box = QMessageBox(parent_window)
        msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
        msg_box.setWindowTitle('FFmpeg Required')
        msg_box.setText('FFmpeg is required but not found on your system. Would you like to install it now?')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg_box.exec()

        if reply == QMessageBox.Yes:
            if not is_admin():
                admin_msg_box = QMessageBox(parent_window)
                admin_msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
                admin_msg_box.setWindowTitle('Admin Rights Required')
                admin_msg_box.setText('Installing FFmpeg requires administrator privileges. Would you like to restart the application as administrator?')
                admin_msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                admin_reply = admin_msg_box.exec()
                
                if admin_reply == QMessageBox.Yes:
                    if restart_as_admin():
                        sys.exit(0)  
                    else:
                        error_msg_box = QMessageBox(parent_window)
                        error_msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
                        error_msg_box.setWindowTitle('Error')
                        error_msg_box.setText('Failed to restart as administrator. Please run the application as administrator manually.')
                        error_msg_box.setStandardButtons(QMessageBox.Ok)
                        error_msg_box.exec()
                return False

            try:
                temp_dir = os.path.join(os.getenv('TEMP'), 'ffmpeg_install')
                os.makedirs(temp_dir, exist_ok=True)
                
                ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
                zip_path = os.path.join(temp_dir, "ffmpeg.zip")
                
                progress = DownloadProgressDialog(parent_window)
                progress.show()
                
                try:
                    urllib.request.urlretrieve(
                        ffmpeg_url,
                        zip_path,
                        reporthook=progress.urlretrieve_callback
                    )
                finally:
                    progress.close()

                progress = DownloadProgressDialog(parent_window)
                progress.setLabelText("Extracting FFmpeg...")
                progress.setValue(0)
                progress.show()

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                progress.setValue(100)
                progress.close()

                ffmpeg_folder = next(f for f in os.listdir(temp_dir) if f.startswith('ffmpeg-master'))
                bin_path = os.path.join(temp_dir, ffmpeg_folder, 'bin')

                if set_system_path_env(bin_path):
                    success_msg_box = QMessageBox(parent_window)
                    success_msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
                    success_msg_box.setWindowTitle('Success')
                    success_msg_box.setText('FFmpeg has been installed successfully.')
                    success_msg_box.setStandardButtons(QMessageBox.Ok)
                    success_msg_box.exec()
                    return True
                else:
                    error_msg_box = QMessageBox(parent_window)
                    error_msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
                    error_msg_box.setWindowTitle('Error')
                    error_msg_box.setText('Failed to set system PATH. Please install FFmpeg manually.')
                    error_msg_box.setStandardButtons(QMessageBox.Ok)
                    error_msg_box.exec()
                    return False

            except Exception as e:
                error_msg_box = QMessageBox(parent_window)
                error_msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
                error_msg_box.setWindowTitle('Error')
                error_msg_box.setText(f'Failed to install FFmpeg: {str(e)}')
                error_msg_box.setStandardButtons(QMessageBox.Ok)
                error_msg_box.exec()
                return False
        else:
            warning_msg_box = QMessageBox(parent_window)
            warning_msg_box.setStyleSheet(MESSAGE_BOX_STYLE)
            warning_msg_box.setWindowTitle('FFmpeg Required')
            warning_msg_box.setText('FFmpeg is required for audio processing. The application may not work correctly without it.')
            warning_msg_box.setStandardButtons(QMessageBox.Ok)
            warning_msg_box.exec()
            return False
    return True
