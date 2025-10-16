from typing import Optional

from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication, QMainWindow
from loguru import logger

from .form import Ui_MainWindow
from .component import PTTButton
from .config_window import ConfigWindow
from .connect_window import ConnectWindow
from .loading_window import LoadingWindow
from .login_window import LoginWindow
from src.constants import app_title
from src.utils import http
from src.model import ConnectionState
from src.config import config
from src.thread import KeyboardListenerThread, MouseListenerThread
from src.core import VoiceClient
from src.signal import Signals, MouseSignals, KeyBoardSignals, AudioSignal


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, signals: Signals, mouse_signals: MouseSignals, keyboard_signals: KeyBoardSignals,
                 audio_signal: AudioSignal) -> None:
        super().__init__()
        logger.trace("Creating main window")

        self.setupUi(self)
        self.resize(300, 300)
        self.setMinimumSize(300, 300)
        self.setWindowTitle(app_title)
        self.menubar.setVisible(False)

        self.voice_client: Optional[VoiceClient] = None
        self.keyboard_listener: Optional[KeyboardListenerThread] = None
        self.mouse_listener: Optional[MouseListenerThread] = None
        self.connect: Optional[ConnectWindow] = None
        self.login: Optional[LoginWindow] = None
        self.config: Optional[ConfigWindow] = None
        self.ptt_button: Optional[PTTButton] = None

        self.loading = LoadingWindow()
        self.loading.setObjectName(u"loading")
        self.windows.addWidget(self.loading)
        self.windows.setCurrentIndex(0)

        self.signals = signals
        self.mouse_signals = mouse_signals
        self.keyboard_signals = keyboard_signals
        self.audio_signal = audio_signal

        config.add_config_save_callback(self.config_update)

        http.initialize()
        http.client_initialized.connect(self.initialize_complete)
        self.action_settings.triggered.connect(self.show_config_window)
        signals.show_config_windows.connect(self.show_config_window)
        signals.logout_request.connect(self.logout_request)
        signals.resize_window.connect(self.resize_window)

    def logout_request(self) -> None:
        self.windows.setCurrentIndex(1)

    def login_success(self) -> None:
        self.windows.setCurrentIndex(2)

    def config_update(self) -> None:
        self.ptt_button.set_target_key(config.ptt_key)

    def initialize_complete(self) -> None:
        self.setMinimumSize(0, 0)

        self.voice_client = VoiceClient(self.signals, self.audio_signal)

        self.login = LoginWindow(self.voice_client, self.signals)
        self.login.setObjectName(u"login")
        self.windows.addWidget(self.login)

        self.connect = ConnectWindow(self.voice_client, self.signals)
        self.connect.setObjectName(u"connect")
        self.windows.addWidget(self.connect)

        self.config = ConfigWindow(self.audio_signal)
        self.config.setObjectName(u"config")

        self.signals.login_success.connect(self.login_success)
        self.signals.login_success.connect(self.connect.login_success)

        self.mouse_listener = MouseListenerThread(self.mouse_signals)
        self.keyboard_listener = KeyboardListenerThread(self.keyboard_signals)

        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.config.button_ptt.mouse_signal = self.mouse_signals
        self.config.button_ptt.keyboard_signal = self.keyboard_signals

        self.ptt_button = PTTButton()
        self.config_update()
        self.mouse_signals.mouse_clicked.connect(self.ptt_button.key_pressed)
        self.keyboard_signals.key_pressed.connect(self.ptt_button.key_pressed)
        self.mouse_signals.mouse_released.connect(self.ptt_button.key_released)
        self.keyboard_signals.key_released.connect(self.ptt_button.key_released)
        self.ptt_button.ptt_pressed.connect(lambda x: self.audio_signal.ptt_status_change.emit(x))
        self.voice_client.connection_state_changed.connect(self.handle_connect_status_change)

        self.menubar.setVisible(True)
        self.resize(450, 450)
        self.center()
        self.windows.setCurrentIndex(1)
        self.loading.stop_animation()

    def center(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(screen)
        self.move(geo.topLeft())

    def handle_connect_status_change(self, status: ConnectionState) -> None:
        match status:
            case ConnectionState.DISCONNECTED:
                self.setWindowTitle(f"{app_title} - 已断开")
            case ConnectionState.CONNECTING:
                self.setWindowTitle(f"{app_title} - 连接中")
            case ConnectionState.CONNECTED:
                self.setWindowTitle(f"{app_title} - 已连接")
            case ConnectionState.AUTHENTICATING:
                self.setWindowTitle(f"{app_title} - 认证中")
            case ConnectionState.READY:
                self.setWindowTitle(f"{app_title} - 已就绪")

    def show_config_window(self) -> None:
        self.config.update_config_data()
        self.config.show()

    def resize_window(self, width: int, height: int, to_center: bool) -> None:
        self.resize(width, height)
        if to_center:
            self.center()
