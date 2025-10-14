from os.path import expandvars, join

from .utils.version import Version

config_version: Version = Version([1, 0, 0])
config_path: str = "config"
app_version: Version = Version([0, 1, 0])
app_name: str = "AudioClient"
app_title: str = f"{app_name} v{app_version.version}"
appdata_path: str = join(expandvars("%APPDATA%"), app_name)

organization_name: str = "APOC Dev team"
organization_website: str = "https://www.apocfly.com"

opus_default_sample_rate: int = 48000
opus_default_bitrate: int = int(opus_default_sample_rate / 2)
default_sample_rate: int = 44100
default_channels: int = 1
default_frame_time: int = 10  # ms
default_frame_size: int = int(opus_default_sample_rate / (1000 / default_frame_time))
