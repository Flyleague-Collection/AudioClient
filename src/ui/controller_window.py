from re import compile

from PySide6.QtWidgets import QWidget

from src.core import VoiceClient
from src.model import ConnectionState
from src.utils import clear_error
from .form import Ui_ControllerWindow

frequency_pattern = compile(r"\d{1,3}\.\d{3}")


class ControllerWindow(QWidget, Ui_ControllerWindow):
    def __init__(self, voice_client: VoiceClient):
        super().__init__()
        self.setupUi(self)
        self.voice_client = voice_client
        self.button_main_freq_tx.clicked.connect(self.main_freq_tx_click)
        self.button_main_freq_rx.clicked.connect(self.main_freq_rx_click)
        self.button_unicom_freq_tx.clicked.connect(self.unicom_freq_tx_click)
        self.button_unicom_freq_rx.clicked.connect(self.unicom_freq_rx_click)
        self.button_emer_freq_tx.clicked.connect(self.emer_freq_tx_click)
        self.button_emer_freq_rx.clicked.connect(self.emer_freq_rx_click)
        self.button_freq_tx.clicked.connect(self.freq_tx_click)
        self.button_freq_rx.clicked.connect(self.freq_rx_click)
        voice_client.connection_state_changed.connect(self.connect_state_changed)
        voice_client.update_current_frequency.connect(
            lambda x: self.label_current_freq_v.setText(f"{x / 1000:.3f}" if x != 0 else "---.---")
        )
        self._frequency = -1
        self.line_edit_freq.textChanged.connect(self.decode_frequency)

    def decode_frequency(self, text: str):
        if frequency_pattern.match(text) is not None:
            self._frequency = int(float(text) * 1000)
            self.button_freq_rx.setEnabled(True)
            self.button_freq_tx.setEnabled(True)
        else:
            self._frequency = -1
            self.button_freq_rx.selected = False
            self.button_freq_tx.selected = False
            self.button_freq_rx.setEnabled(False)
            self.button_freq_tx.setEnabled(False)
            self.voice_client.set_transmitter_receive_flag(self._frequency, False)

    def freq_tx_click(self):
        clear_error(self.line_edit_freq)
        self.button_emer_freq_tx.selected = False
        self.button_main_freq_tx.selected = False
        self.button_unicom_freq_tx.selected = False
        if self.button_freq_tx.selected:
            self.voice_client.switch_frequency(self._frequency, 3)
        else:
            self.voice_client.clear_frequency()

    def freq_rx_click(self):
        self.voice_client.set_transmitter_receive_flag(self._frequency,
                                                       self.button_freq_rx.selected)

    def main_freq_tx_click(self):
        self.button_freq_tx.selected = False
        self.button_emer_freq_tx.selected = False
        self.button_unicom_freq_tx.selected = False
        if self.button_main_freq_tx.selected:
            self.voice_client.switch_frequency(self.voice_client.main_frequency, 0)
        else:
            self.voice_client.clear_frequency()

    def main_freq_rx_click(self):
        self.voice_client.set_transmitter_receive_flag(self.voice_client.main_frequency,
                                                       self.button_main_freq_rx.selected)

    def unicom_freq_tx_click(self):
        self.button_freq_tx.selected = False
        self.button_emer_freq_tx.selected = False
        self.button_main_freq_tx.selected = False
        if self.button_unicom_freq_tx.selected:
            self.voice_client.switch_frequency(122800, 1)
        else:
            self.voice_client.clear_frequency()

    def unicom_freq_rx_click(self):
        self.voice_client.set_transmitter_receive_flag(122800, self.button_unicom_freq_rx.selected)

    def emer_freq_tx_click(self):
        self.button_freq_tx.selected = False
        self.button_main_freq_tx.selected = False
        self.button_unicom_freq_tx.selected = False
        if self.button_emer_freq_tx.selected:
            self.voice_client.switch_frequency(121500, 2)
        else:
            self.voice_client.clear_frequency()

    def emer_freq_rx_click(self):
        self.voice_client.set_transmitter_receive_flag(121500, self.button_emer_freq_rx.selected)

    def connect_state_changed(self, state: ConnectionState):
        if not self.voice_client.is_atc:
            return
        if state == ConnectionState.READY:
            self.label_main_freq_v.setText(f"{self.voice_client.main_frequency / 1000:.3f}")
            self.button_main_freq_rx.selected = True
            self.button_unicom_freq_rx.selected = True
            self.button_emer_freq_rx.selected = True
            self.button_freq_rx.selected = False
            self.button_freq_rx.setEnabled(False)
            self.button_freq_tx.setEnabled(False)
            self.voice_client.set_transmitter_receive_flag(self.voice_client.main_frequency,
                                                           self.button_main_freq_rx.selected)
            self.voice_client.set_transmitter_receive_flag(122800, self.button_unicom_freq_rx.selected)
            self.voice_client.set_transmitter_receive_flag(121500, self.button_emer_freq_rx.selected)
