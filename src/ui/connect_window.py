from time import time

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QWidget
from loguru import logger

from src.config import config
from src.core import VoiceClient
from src.model import ConnectionState, VoicePacket
from src.signal import Signals
from src.utils import get_line_edit_data
from .client_window import ClientWindow
from .controller_window import ControllerWindow
from .form import Ui_ConnectWindow
from ..constants import default_frame_time


class ConnectWindow(QWidget, Ui_ConnectWindow):
    def __init__(self, voice_client: VoiceClient, signals: Signals):
        super().__init__()
        self.setupUi(self)
        self.voice_client = voice_client
        self.button_connect.clicked.connect(self.connect_to_server)
        self.voice_client.error_occurred.connect(self.handle_connect_error)
        self.voice_client.connection_state_changed.connect(self.connect_state_changed)
        self.controller_window = ControllerWindow(voice_client)
        self.client_window = ClientWindow()
        self.windows.addWidget(QWidget())
        self.windows.addWidget(self.controller_window)
        self.windows.addWidget(self.client_window)
        self.windows.setCurrentIndex(0)
        self.button_exit.clicked.connect(lambda: signals.logout_request.emit())
        voice_client.voice_data_sent.connect(self.tx_send)
        voice_client.voice_data_received.connect(self.rx_receive)
        self.last_data_receive = 0
        self.receive_timeout_timer = QTimer()
        self.receive_timeout_timer.timeout.connect(self.check_rx_timeout)
        self.receive_timeout_timer.start(50)
        self.last_data_send = 0
        self.send_timeout_timer = QTimer()
        self.send_timeout_timer.timeout.connect(self.check_tx_timeout)
        self.send_timeout_timer.start(50)

    def check_rx_timeout(self):
        if self.button_rx.is_active:
            if time() - self.last_data_receive > (default_frame_time / 1000):
                self.button_rx.set_active(False)

    def check_tx_timeout(self):
        if self.button_tx.is_active:
            if time() - self.last_data_send > (default_frame_time / 1000):
                self.button_tx.set_active(False)

    def tx_send(self) -> None:
        if self.voice_client.connection_state != ConnectionState.READY:
            self.button_tx.set_active(False)
            return
        self.last_data_send = time()
        self.button_tx.set_active(True)

    def rx_receive(self, voice: VoicePacket) -> None:
        if self.voice_client.connection_state != ConnectionState.READY:
            self.button_rx.set_active(False)
            return
        self.last_data_receive = time()
        self.button_rx.set_active(True)
        self.label_rx_callsign_v.setText(voice.callsign)
        self.label_rx_freq_v.setText(f"{voice.frequency / 1000:.3f}")

    def login_success(self):
        if self.voice_client.cid is None:
            return
        self.label_cid_v.setText(f"{self.voice_client.cid:04}")
        self.line_edit_address.setText(config.server_host)
        self.line_edit_tcp_port.setText(str(config.server_tcp_port))
        self.line_edit_udp_port.setText(str(config.server_udp_port))

    def connect_to_server(self):
        address = get_line_edit_data(self.line_edit_address, str)
        tcp_port = get_line_edit_data(self.line_edit_tcp_port, int)
        udp_port = get_line_edit_data(self.line_edit_udp_port, int)

        if address is None:
            logger.error(f"Address can't be empty")
            return

        if tcp_port is None:
            logger.error(f"TCP port can't be empty")
            return

        if udp_port is None:
            logger.error(f"UDP port can't be empty")
            return

        self.voice_client.connect_to_server(address, tcp_port, udp_port)
        config.server_host = address
        config.server_tcp_port = tcp_port
        config.server_udp_port = udp_port
        config.save_config()

    def disconnect_from_server(self):
        self.voice_client.disconnect()

    def connect_state_changed(self, state: ConnectionState):
        if state == ConnectionState.READY:
            self.button_connect.setText("断开连接")
            self.label_callsign_v.setText(self.voice_client.callsign)
            self.button_connect.clicked.disconnect(self.connect_to_server)
            self.button_connect.clicked.connect(self.disconnect_from_server)
            if self.voice_client.is_atc:
                self.windows.setCurrentIndex(1)
            else:
                self.windows.setCurrentIndex(2)
        elif state == ConnectionState.DISCONNECTED:
            self.button_connect.setText("连接服务器")
            self.label_callsign_v.setText("----")
            self.button_connect.clicked.disconnect(self.disconnect_from_server)
            self.button_connect.clicked.connect(self.connect_to_server)
            self.windows.setCurrentIndex(0)

    def handle_connect_error(self, message: str) -> None:
        QMessageBox.critical(self, "连接服务器失败", message)
        self.button_connect.setText("连接服务器")
        self.label_callsign_v.setText("----")
        self.button_connect.clicked.disconnect(self.disconnect_from_server)
        self.button_connect.clicked.connect(self.connect_to_server)
        self.windows.setCurrentIndex(0)
