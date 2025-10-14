from PySide6.QtCore import QObject, Signal


class MouseSignals(QObject):
    mouse_clicked = Signal(str)
    mouse_released = Signal(str)

