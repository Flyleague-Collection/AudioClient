from threading import Event, Thread
from time import sleep

from PySide6.QtWidgets import QWidget
from loguru import logger

from .form import Ui_ClientWindow
from ..core import VoiceClient
from ..core.fsuipc_client import FSUIPCClient
from ..model import ConnectionState


class ClientWindow(QWidget, Ui_ClientWindow):
    def __init__(self, voice_client: VoiceClient, fsuipc_client: FSUIPCClient):
        super().__init__()
        self.setupUi(self)

        self.button_com1_tx.clicked.connect(self.com1_freq_tx_clicked)
        self.button_com2_tx.clicked.connect(self.com2_freq_tx_clicked)

        self.voice_client = voice_client
        self.fsuipc_client = fsuipc_client
        self.thread_exit = Event()
        self.com1_freq = 0
        self.com2_freq = 0
        self.com1_rx = False
        self.com2_rx = False
        self.overwrite_com1_freq = 0
        self.overwrite_com2_freq = 0

    def com1_freq_tx_clicked(self):
        self.button_com2_tx.selected = False
        if self.button_com1_tx.selected:
            self.voice_client.switch_frequency(self.com1_freq, 0)
        else:
            self.voice_client.clear_frequency()

    def com2_freq_tx_clicked(self):
        self.button_com1_tx.selected = False
        if self.button_com2_tx.selected:
            self.voice_client.switch_frequency(self.com2_freq, 1)
        else:
            self.voice_client.clear_frequency()

    def start(self):
        self.thread_exit.clear()
        Thread(target=self._receive_frequency, daemon=True).start()

    def stop(self):
        self.thread_exit.set()

    def _receive_frequency(self):
        err_count = 0
        while not self.thread_exit.is_set():
            res = self.fsuipc_client.get_frequency()
            if res.requestStatus:
                self.update_com_info(res.frequency[0] // 1000,
                                     res.frequency[2] // 1000,
                                     (res.frequencyFlag & 0x80) != 0x80,
                                     (res.frequencyFlag & 0x40) != 0x40)
            else:
                logger.error(f"Error while receiving frequency from FSUIPC: {res.errMessage}")
                err_count += 1
            if err_count >= 3:
                logger.error(f"Too many error received from FSUIPC: {err_count}, disconnecting")
            sleep(1)

    def update_com_info(self, com1_freq: int, com2_freq: int, com1_rx: bool, com2_rx: bool):
        if self.com1_freq != com1_freq:
            if self.com1_freq != 0:
                self.voice_client.set_transmitter_receive_flag(self.com1_freq, False)
            self.voice_client.set_transmitter_receive_flag(com1_freq, self.com1_rx | com1_rx)
            self.label_com1_freq.setText(f"{com1_freq / 1000:.3f}")
            if self.button_com1_tx.selected:
                self.voice_client.switch_frequency(com1_freq, 0)
            self.com1_freq = com1_freq

        if self.com2_freq != com2_freq:
            if self.com2_freq != 0:
                self.voice_client.set_transmitter_receive_flag(self.com2_freq, False)
            self.voice_client.set_transmitter_receive_flag(com2_freq, self.com2_rx | com2_rx)
            self.label_com2_freq.setText(f"{com2_freq / 1000:.3f}")
            if self.button_com2_tx.selected:
                self.voice_client.switch_frequency(com2_freq, 1)
            self.com2_freq = com2_freq

        self.button_com1_rx.selected = self.com1_rx | com1_rx
        self.com1_rx = com1_rx

        self.button_com2_rx.selected = self.com2_rx | com2_rx
        self.com2_rx = com2_rx
