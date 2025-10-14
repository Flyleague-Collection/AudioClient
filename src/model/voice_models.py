from dataclasses import dataclass
from enum import Enum
from struct import pack
from typing import List


class MessageType(str, Enum):
    SWITCH = "channel"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    TEXT_RECEIVE = "text_receive"
    MESSAGE = "message"
    DISCONNECT = "disconnect"


class ConnectionState(Enum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    AUTHENTICATING = 3
    READY = 4


@dataclass
class ControlMessage:
    type: MessageType
    cid: int = 0
    callsign: str = ""
    transmitter: int = 0
    data: str = ""

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "cid": self.cid,
            "callsign": self.callsign,
            "transmitter": self.transmitter,
            "data": self.data
        }


@dataclass
class ChannelInfo:
    frequency: int
    user_count: int = 0
    is_active: bool = False
    users: List[str] = None

    def __post_init__(self):
        if self.users is None:
            self.users = []


@dataclass
class VoicePacket:
    cid: int
    transmitter: int
    frequency: int
    callsign: str
    data: bytes


class VoicePacketBuilder:
    @staticmethod
    def build_packet(cid: int, transmitter: int, frequency: int, callsign: str, audio_data: bytes) -> bytes:
        callsign_bytes = callsign.encode('utf-8')
        callsign_len = len(callsign_bytes)

        if callsign_len > 255:
            raise ValueError("Callsign too long")

        if frequency >= 200000:
            raise ValueError("Frequency too large")

        if frequency > 100000:
            frequency -= 100000

        packet = bytearray()
        packet.extend(pack('<i', cid))
        packet.extend(pack('<b', transmitter))
        packet.extend(pack('<i', frequency))
        packet.append(callsign_len)
        packet.extend(callsign_bytes)
        packet.extend(audio_data)
        packet.extend(b'\n')

        return bytes(packet)
