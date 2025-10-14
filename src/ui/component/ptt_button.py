from typing import Optional

from PySide6.QtCore import QObject, Signal


class PTTButton(QObject):
    ptt_pressed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._target_key: Optional[str] = None
        self._ptt_active: bool = False

    def set_target_key(self, target_key: str):
        self._target_key = target_key

    def key_pressed(self, key: str):
        if self._target_key is None:
            return
        if not self._ptt_active and key == self._target_key:
            self._ptt_active = True
            self.ptt_pressed.emit(self._ptt_active)

    def key_released(self, key: str):
        if self._target_key is None:
            return
        if self._ptt_active and key == self._target_key:
            self._ptt_active = False
            self.ptt_pressed.emit(self._ptt_active)
