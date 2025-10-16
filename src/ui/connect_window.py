from datetime import datetime
from os import getcwd
from os.path import join
from threading import Thread
from time import sleep, time

from PySide6.QtCore import QTimer, Signal
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
from ..core.fsuipc_client import FSUIPCClient


class ConnectWindow(QWidget, Ui_ConnectWindow):
    fsuipc_client_connected = Signal()
    fsuipc_client_connect_fail = Signal()

    def __init__(self, voice_client: VoiceClient, signals: Signals):
        super().__init__()
        self.setupUi(self)

        try:
            self.fsuipc_client = FSUIPCClient(join(getcwd(), "libfsuipc.dll"))
        except FileNotFoundError:
            logger.error("Cannot find libfsuipc.dll")
            QMessageBox.critical(self, "Cannot load libfsuipc.dll",
                                 f"Cannot found libfsuipc.dll, download it and put it under {getcwd()}")
            exit(1)
        except Exception as e:
            logger.error(f"Fail to load libfsuipc.dll, {e}")
            QMessageBox.critical(self, "Cannot load libfsuipc.dll",
                                 "Unknown error occurred while loading libfsuipc.dll")
            exit(1)

        self.voice_client = voice_client
        self.button_connect.clicked.connect(self.connect_to_server)
        self.voice_client.error_occurred.connect(self.handle_connect_error)
        self.voice_client.connection_state_changed.connect(self.connect_state_changed)
        self.controller_window = ControllerWindow(voice_client)
        self.client_window = ClientWindow(voice_client, self.fsuipc_client)
        self.windows.addWidget(QWidget())
        self.windows.addWidget(self.controller_window)
        self.windows.addWidget(self.client_window)
        self.windows.setCurrentIndex(0)
        self.button_exit.clicked.connect(lambda: signals.logout_request.emit())
        self.fsuipc_client_connected.connect(self.fsuipc_connect)
        self.fsuipc_client_connect_fail.connect(self.fsuipc_connection_fail)
        signals.log_message.connect(self.log_message)

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

        self._connected = False
        self.signals = signals

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
        if self._connected:
            self.voice_client.disconnect()
            self.client_window.stop()
            self._connected = False
            return

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

    def connect_state_changed(self, state: ConnectionState):
        if state == ConnectionState.READY:
            self.button_connect.setText("断开连接")
            self._connected = True
            self.label_callsign_v.setText(self.voice_client.callsign)
            if self.voice_client.is_atc:
                self.windows.setCurrentIndex(1)
            else:
                Thread(target=self.connect_to_simulator, daemon=True).start()
        elif state == ConnectionState.DISCONNECTED:
            self._connected = False
            self.button_connect.setText("连接服务器")
            self.label_callsign_v.setText("----")
            self.windows.setCurrentIndex(0)

    def fsuipc_connect(self):
        self.windows.setCurrentIndex(2)
        self.signals.resize_window.emit(450, 600, True)
        self.client_window.start()

    def fsuipc_connection_fail(self):
        self.connect_to_server()
        QMessageBox.critical(self, "无法连接到模拟器", "无法连接到模拟器, 请检查FSUIPC/XPUIPC是否正确安装")

    def connect_to_simulator(self):
        retry = 0
        max_retry = 12
        retry_delay = 5
        while retry < max_retry:
            res = self.fsuipc_client.open_fsuipc_client()
            if res.requestStatus:
                logger.success("FSUIPC connection established")
                self.log_message("FSUIPC", "INFO", "FSUIPC连接成功")
                break
            logger.error(f"FSUIPC connection failed, {retry + 1}/{max_retry} times")
            self.log_message("FSUIPC", "ERROR", f"FSUIPC连接失败, 第 {retry + 1}/{max_retry} 次尝试")
            retry += 1
            sleep(retry_delay)
        if retry == max_retry:
            logger.error(f"FSUIPC connection failed")
            self.log_message("FSUIPC", "ERROR", "FSUIPC连接失败")
            self.fsuipc_client_connect_fail.emit()
            return
        self.fsuipc_client_connected.emit()

    def handle_connect_error(self, message: str) -> None:
        QMessageBox.critical(self, "连接服务器失败", message)
        self.button_connect.setText("连接服务器")
        self.label_callsign_v.setText("----")
        self.windows.setCurrentIndex(0)

    def log_message(self, name: str, level: str, message: str) -> None:
        self.text_browser_log.append(
            f"{datetime.now().strftime('%H:%M:%S')} | {name} | {level.upper()} | {message}")
        cursor = self.text_browser_log.textCursor()
        self.text_browser_log.moveCursor(cursor.MoveOperation.End)
