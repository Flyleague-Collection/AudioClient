import json
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
from struct import unpack
from threading import Thread
from typing import Optional

from PySide6.QtCore import QObject, Signal
from loguru import logger

from src.model.voice_models import ControlMessage, MessageType, VoicePacket
from src.signal import Signals


class NetworkHandler(QObject):
    control_message_received = Signal(ControlMessage)
    voice_packet_received = Signal(VoicePacket)
    connection_status_changed = Signal(bool)
    error_occurred = Signal(str)

    def __init__(self, signals: Signals):
        super().__init__()

        self._tcp_socket: Optional[socket] = None
        self._udp_socket: Optional[socket] = None
        self._server_address: Optional[tuple] = None

        self._signals = signals

        self._tcp_running = False
        self._udp_running = False

        self._is_connected = False
        self._cid: Optional[int] = None
        self._callsign: Optional[str] = None

    def _log_message(self, level: str, message: str):
        self._signals.log_message.emit("Network", level, message)

    def connect_to_server(self, host: str, tcp_port: int, udp_port: int, jwt_token: str):
        try:
            self._server_address = (host, udp_port)

            self._log_message("INFO", f"Connect to tcp://{host}:{tcp_port}")
            self._tcp_socket = socket(AF_INET, SOCK_STREAM)
            self._tcp_socket.connect((host, tcp_port))

            self._tcp_running = True
            tcp_thread = Thread(target=self._tcp_receive_loop, daemon=True)
            tcp_thread.start()

            self._log_message("INFO", f"Connect to udp://{host}:{udp_port}")
            self._udp_socket = socket(AF_INET, SOCK_DGRAM)
            self._udp_socket.connect((host, udp_port))
            self._udp_running = True
            udp_thread = Thread(target=self._udp_receive_loop, daemon=True)
            udp_thread.start()

            self._tcp_socket.send(f"{jwt_token}\n".encode())

            self._is_connected = True
            self.connection_status_changed.emit(True)
            logger.info("Connected to voice server")
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")
            self._log_message("ERROR", f"Failed to connect to server")
            self.error_occurred.emit(f"连接失败: {e}")
            self.cleanup()

    def disconnect(self):
        self.cleanup()
        self.connection_status_changed.emit(False)
        self._log_message("INFO", f"Disconnected from voice server")
        logger.info("Disconnected from voice server")

    def send_control_message(self, message: ControlMessage):
        if not self._tcp_socket:
            return
        try:
            data = json.dumps(message.to_dict()).encode()
            self._tcp_socket.send(data + b'\n')
        except Exception as e:
            logger.error(f"Failed to send control message: {e}")
            self.error_occurred.emit(f"发送消息失败: {e}")

    def send_voice_packet(self, packet: bytes):
        if not self._udp_socket or not self._server_address:
            return

        try:
            self._udp_socket.sendto(packet, self._server_address)
        except Exception as e:
            logger.error(f"Failed to send voice packet: {e}")

    def _tcp_receive_loop(self):
        while self._tcp_running and self._tcp_socket:
            try:
                data = self._tcp_socket.recv(4096)
                if not data:
                    break
                logger.trace(f"TCP receive from server: {data}")
                self._process_control_message(data.decode())
            except Exception as e:
                if self._tcp_running:
                    logger.error(f"TCP receive error: {e}")
                break
        self.disconnect()

    def _udp_receive_loop(self):
        while self._udp_running and self._udp_socket:
            try:
                data, addr = self._udp_socket.recvfrom(65507)
                self._process_voice_packet(data)
            except Exception as e:
                if self._udp_running:
                    logger.error(f"UDP receive error: {e}")
                break

    def _process_control_message(self, data: str):
        try:
            message_dict = json.loads(data)
            message = ControlMessage(
                type=MessageType(message_dict.get('type')),
                cid=message_dict.get('cid', 0),
                callsign=message_dict.get('callsign', ''),
                transmitter=message_dict.get('transmitter', 0),
                data=message_dict.get('data', '')
            )
            self.control_message_received.emit(message)
        except Exception as e:
            logger.error(f"Failed to process control message: {e}")

    def _process_voice_packet(self, data: bytes):
        try:
            if len(data) < 10 or data[-1] != 0x0A:
                return
            cid = unpack('<i', data[0:4])[0]
            transmitter = unpack('<b', data[4:5])[0]
            frequency = unpack('<i', data[5:9])[0] + 100000
            callsign_len = data[9]
            if 9 + callsign_len > len(data) - 1:
                return
            callsign = data[10:10 + callsign_len].decode("utf-8")
            audio_data = data[10 + callsign_len:-1]
            logger.trace(
                f"Received from {callsign} (CID={cid}, Frequency={frequency}), audio length: {len(audio_data)}")
            packet = VoicePacket(cid, transmitter, frequency, callsign, audio_data)
            self.voice_packet_received.emit(packet)
        except Exception as e:
            logger.error(f"Failed to process voice packet: {e}")

    def cleanup(self):
        self._tcp_running = False
        self._udp_running = False
        self._is_connected = False

        if self._tcp_socket:
            try:
                self._tcp_socket.close()
            except:
                pass
            self._tcp_socket = None

        if self._udp_socket:
            try:
                self._udp_socket.close()
            except:
                pass
            self._udp_socket = None
