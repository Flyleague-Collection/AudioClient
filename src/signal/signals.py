from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    show_config_windows = Signal()
    login_success = Signal()
    logout_request = Signal()
