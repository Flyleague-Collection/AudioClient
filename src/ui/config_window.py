from PySide6.QtWidgets import QWidget
from loguru import logger

from .form import Ui_ConfigWindow
from src.config import config
from src.signal import AudioSignal
from src.utils import get_device_info, get_host_api_info


class ConfigWindow(QWidget, Ui_ConfigWindow):
    def __init__(self, audio_signal: AudioSignal):
        super().__init__()
        self.setupUi(self)
        config.add_config_save_callback(self.update_config_data)

        self.audio_signal = audio_signal

        self._audio_drivers = get_host_api_info()
        self._audio_inputs = {}
        self._audio_outputs = {}
        self.combo_box_audio_driver.addItem("自动")
        for driver in self._audio_drivers:
            self.combo_box_audio_driver.addItem(driver)

        self.combo_box_audio_driver.currentTextChanged.connect(self.audio_device_update)
        self.audio_device_update(self.combo_box_audio_driver.currentText())
        self.update_config_data()
        self.combo_box_audio_input.currentTextChanged.connect(self.audio_input_device_change)
        self.audio_input_device_change(self.combo_box_audio_input.currentText())
        self.combo_box_audio_output.currentTextChanged.connect(self.audio_output_device_change)
        self.audio_output_device_change(self.combo_box_audio_output.currentText())

        self.button_cancel.clicked.connect(self.cancel_config_data)
        self.button_apply.clicked.connect(self.apply_config_data)
        self.button_ok.clicked.connect(self.save_config_data)

        self.button_ptt.select_message = "按下ESC退出"

    def audio_input_device_change(self, value: str):
        if not value:
            return
        logger.trace(f"Audio input device change: {value}")
        self.audio_signal.audio_input_device_change.emit(self._audio_inputs.get(value, -1))

    def audio_output_device_change(self, value: str):
        if not value:
            return
        logger.trace(f"Audio output device change: {value}")
        self.audio_signal.audio_output_device_change.emit(self._audio_outputs.get(value, -1))

    def audio_device_update(self, driver_name: str):
        logger.trace(f"Audio device driver update to: {driver_name}")
        driver_id = self._audio_drivers.get(driver_name, -1)
        if driver_id == -1:
            for name in self._audio_drivers:
                if "WASAPI" in name:
                    driver_id = self._audio_drivers[name]
            if driver_id == -1:
                driver_id = 0
        self._audio_inputs, self._audio_outputs = get_device_info(driver_id)

        self.combo_box_audio_input.clear()
        self.combo_box_audio_input.addItem("默认")
        for input_device in self._audio_inputs:
            self.combo_box_audio_input.addItem(input_device)
        self.combo_box_audio_input.setCurrentIndex(0)

        self.combo_box_audio_output.clear()
        self.combo_box_audio_output.addItem("默认")
        for output_device in self._audio_outputs:
            self.combo_box_audio_output.addItem(output_device)
        self.combo_box_audio_output.setCurrentIndex(0)

    def update_config_data(self):
        self.label_config_version_2.setText(config.config_version)
        self.check_box_remember_me.setChecked(config.remember_me)
        self.check_box_debug_mode.setChecked(config.debug_mode)
        self.combo_box_log_level.setCurrentText(config.log_level.upper())
        self.line_edit_account.setText(config.account)
        self.line_edit_password.setText(config.password)
        self.line_edit_server_address.setText(config.server_host)
        self.line_edit_tcp_port.setText(str(config.server_tcp_port))
        self.line_edit_udp_port.setText(str(config.server_udp_port))
        self.combo_box_audio_driver.setCurrentText(config.audio_driver)
        self.combo_box_audio_input.setCurrentText(config.audio_input)
        self.combo_box_audio_output.setCurrentText(config.audio_output)
        self.button_ptt.selected_key = config.ptt_key

    def save_config_data(self):
        self.apply_config_data()
        self.hide()

    def apply_config_data(self):
        config.remember_me = self.check_box_remember_me.isChecked()
        config.debug_mode = self.check_box_debug_mode.isChecked()
        config.log_level = self.combo_box_log_level.currentText().upper()
        config.account = self.line_edit_account.text()
        config.password = self.line_edit_password.text()
        config.server_host = self.line_edit_server_address.text()
        config.server_tcp_port = int(self.line_edit_tcp_port.text())
        config.server_udp_port = int(self.line_edit_udp_port.text())
        config.audio_driver = self.combo_box_audio_driver.currentText()
        config.audio_input = self.combo_box_audio_input.currentText()
        config.audio_output = self.combo_box_audio_output.currentText()
        config.ptt_key = self.button_ptt.selected_key
        config.save_config()

    def cancel_config_data(self):
        self.hide()
