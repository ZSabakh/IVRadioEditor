from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):
    progress = Signal(int)  # Signal to report progress percentage (0-100).
    finished = Signal()     # Signal emitted when work is completed.
    error = Signal(str)     # Signal emitted when an error occurs.
