from PySide6.QtCore import QObject, Signal


class KeyBoardSignals(QObject):
    key_pressed = Signal(str)
    key_released = Signal(str)

