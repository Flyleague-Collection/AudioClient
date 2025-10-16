import time
from typing import Optional

from PySide6.QtCore import QObject, QTimer, Signal
from loguru import logger

from src.model.voice_models import ConnectionState, ControlMessage, MessageType, VoicePacket, VoicePacketBuilder
from src.signal import AudioSignal, Signals
from .audio_handler import AudioHandler
from .network_handler import NetworkHandler


class VoiceClient(QObject):
    connection_state_changed = Signal(ConnectionState)
    message_received = Signal(ControlMessage)
    voice_data_received = Signal(VoicePacket)
    voice_data_sent = Signal()
    error_occurred = Signal(str)
    update_current_frequency = Signal(int)

    def __init__(self, signals: Signals, audio_signal: AudioSignal):
        super().__init__()

        self._network = NetworkHandler(signals)
        self._audio = AudioHandler(audio_signal)
        self._signals = signals

        self._connection_state = ConnectionState.DISCONNECTED
        self._cid: Optional[int] = None
        self._callsign: Optional[str] = None
        self._jwt_token: Optional[str] = None
        self._current_frequency: int = 0
        self._current_transmitter: int = 0
        self._main_frequency: int = 0
        self._is_atc: bool = False
        self._transmitter_receive_flag: dict[int, bool] = {}

        self._connect_signals()

        self._heartbeat_timer = QTimer()
        self._heartbeat_timer.timeout.connect(self._send_heartbeat)
        self._heartbeat_timer.setInterval(15000)

    def _log_message(self, level: str, message: str):
        self._signals.log_message.emit("VoiceClient", level, message)

    def _connect_signals(self):
        self._network.control_message_received.connect(self._handle_control_message)
        self._network.voice_packet_received.connect(self._handle_voice_packet)
        self._network.connection_status_changed.connect(self._handle_connection_status)
        self._network.error_occurred.connect(self.error_occurred)

        self._audio.on_encoded_audio = self._send_voice_data

    def connect_to_server(self, host: str, tcp_port: int, udp_port: int):
        self._set_connection_state(ConnectionState.CONNECTING)
        self._network.connect_to_server(host, tcp_port, udp_port, self._jwt_token)

    def disconnect(self):
        self._network.send_control_message(ControlMessage(MessageType.DISCONNECT, self._cid, self._callsign))

    def clear_frequency(self):
        if not self._is_ready():
            return
        self._current_frequency = 0
        self._current_transmitter = 0
        self.update_current_frequency.emit(0)

    def switch_frequency(self, frequency: int, transmitter: int = 0):
        if not self._is_ready():
            return

        self._current_frequency = frequency
        self._current_transmitter = transmitter

        self.update_current_frequency.emit(frequency)

        message = ControlMessage(
            type=MessageType.SWITCH,
            cid=self._cid,
            callsign=self._callsign,
            transmitter=transmitter,
            data=str(frequency)
        )
        self._log_message("INFO", f"Switch to {frequency / 1000:.3f}mHz")
        self._network.send_control_message(message)

    def send_text_message(self, target: str, message: str):
        if not self._is_ready():
            return

        control_message = ControlMessage(
            type=MessageType.MESSAGE,
            cid=self._cid,
            callsign=self._callsign,
            data=f"{target}:{message}"
        )
        self._network.send_control_message(control_message)

    def set_ptt_state(self, active: bool):
        self._audio.set_ptt_state(active)

    def _set_connection_state(self, state: ConnectionState):
        if self._connection_state != state:
            self._connection_state = state
            self.connection_state_changed.emit(state)

    def _is_ready(self) -> bool:
        return (self._connection_state == ConnectionState.READY and
                self._cid is not None and
                self._callsign is not None)

    def _send_heartbeat(self):
        if not self._is_ready():
            return
        message = ControlMessage(
            type=MessageType.PING,
            cid=self._cid,
            callsign=self._callsign,
            data=str(int(time.time()))
        )
        self._network.send_control_message(message)

    def _send_voice_data(self, encoded_data: bytes):
        if not self._is_ready() or self._current_frequency == 0:
            return

        self.voice_data_sent.emit()
        packet = VoicePacketBuilder.build_packet(self._cid,
                                                 self._current_transmitter,
                                                 self._current_frequency,
                                                 self._callsign,
                                                 encoded_data)
        self._network.send_voice_packet(packet)

    def _handle_control_message(self, message: ControlMessage):
        self.message_received.emit(message)

        if message.type == MessageType.ERROR:
            logger.error(f"Server error: {message.data}")
            self.error_occurred.emit(message.data)
        elif message.type == MessageType.PONG:
            logger.debug("Received pong from server")
        elif message.type == MessageType.MESSAGE:
            if message.data.startswith("SERVER:"):
                if "Welcome" in message.data:
                    data = message.data.split(":")
                    self._callsign = data[1]
                    self._heartbeat_timer.start()
                    self._audio.start_recording()
                    self._audio.start_playback()
                    if len(data) == 4:
                        self._main_frequency = int(data[-1])
                        self._is_atc = True
                    self._set_connection_state(ConnectionState.READY)
                    self._log_message("INFO", "Identity verification passed")
                    self._send_voice_data(b"")
        elif message.type == MessageType.DISCONNECT:
            self._heartbeat_timer.stop()
            self._audio.stop_recording()
            self._audio.stop_playback()
            self._network.disconnect()
            self._set_connection_state(ConnectionState.DISCONNECTED)

    def _handle_voice_packet(self, packet: VoicePacket):
        if not self._transmitter_receive_flag.get(packet.frequency, False):
            return
        self.voice_data_received.emit(packet)
        self._audio.play_encoded_audio(packet.data)

    def _handle_connection_status(self, connected: bool):
        if connected:
            self._set_connection_state(ConnectionState.CONNECTED)
        else:
            self._heartbeat_timer.stop()
            self._set_connection_state(ConnectionState.DISCONNECTED)

    def set_transmitter_receive_flag(self, frequency: int, receive_flag: bool):
        if receive_flag:
            self._log_message("INFO", f"Start listening frequency {frequency / 1000:.3f}mHz")
        else:
            self._log_message("INFO", f"Stop listening frequency {frequency / 1000:.3f}mHz")
        self._transmitter_receive_flag[frequency] = receive_flag

    def cleanup(self):
        self.disconnect()
        self._audio.cleanup()

    @property
    def connection_state(self) -> ConnectionState:
        return self._connection_state

    @property
    def cid(self) -> Optional[int]:
        return self._cid

    @cid.setter
    def cid(self, cid: int):
        self._cid = cid

    @property
    def callsign(self) -> Optional[str]:
        return self._callsign

    @callsign.setter
    def callsign(self, callsign: str):
        self._callsign = callsign

    @property
    def jwt_token(self) -> Optional[str]:
        return self._jwt_token

    @jwt_token.setter
    def jwt_token(self, jwt_token: str):
        self._jwt_token = jwt_token

    @property
    def main_frequency(self) -> int:
        return self._main_frequency

    @property
    def is_atc(self) -> bool:
        return self._is_atc
