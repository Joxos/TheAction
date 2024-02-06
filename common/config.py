"""
config.py: Configuration defines here.
"""
from enum import Enum, auto


class COMPRESSER(Enum):
    NONE = auto()
    ZLIB = auto()
    GZIP = auto()
    BZ2 = auto()
    LZMA = auto()


# configuration starts here
DEFAULT_COMPRESSER = COMPRESSER.NONE
DEFAULT_CODING = "utf-8"
ENABLE_TLS = True
