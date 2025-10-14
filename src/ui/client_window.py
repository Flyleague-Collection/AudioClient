from PySide6.QtWidgets import QWidget

from .form import Ui_ClientWindow


class ClientWindow(QWidget, Ui_ClientWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
