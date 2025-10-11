from enum import Enum


class VersionType(Enum):
    ALL_MATCH = 0
    PATCH_UNMATCH = 1
    MINOR_UNMATCH = 2
    MAJOR_UNMATCH = 3
