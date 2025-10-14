from PySide6.QtCore import QObject, Signal


class AudioSignal(QObject):
    audio_input_device_change = Signal(int)
    audio_output_device_change = Signal(int)
    ptt_status_change = Signal(bool)
