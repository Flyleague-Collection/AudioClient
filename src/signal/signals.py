from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    show_config_windows = Signal()
    login_success = Signal()
    logout_request = Signal()
    log_message = Signal(str, str, str)  # from level content3
    resize_window = Signal(int, int, bool)  # width height move to center
