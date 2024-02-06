'''
utils.py: Common utils defines here.
'''
from asyncio import run
from enum import Enum, auto
from sys import stderr
from loguru import logger
from config import *

# logger settings
logger.remove()
logger.add(
    stderr,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)

logger.info(f'{compresser.name.lower().title()} compress selected.')
if compresser == COMPRESSER.ZLIB:
    from zlib import compress, decompress
elif compresser == COMPRESSER.GZIP:
    from gzip import compress, decompress
elif compresser == COMPRESSER.BZ2:
    from bz2 import compress, decompress
elif compresser == COMPRESSER.LZMA:
    from lzma import compress, decompress
elif compresser == COMPRESSER.NONE:

    def compress(m):
        return m

    def decompress(m):
        return m


# console banners
class STATUS(Enum):
    SEND = auto()
    RECV = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()
    ERROR = auto()


def show_status(direction, address, message=''):
    if direction == STATUS.RECV:
        logger.info(f'<-- {address} {message}')
    elif direction == STATUS.SEND:
        logger.info(f'--> {address} {message}')
    elif direction == STATUS.CONNECTED:
        logger.info(f'--- {address} {message}')
    elif direction == STATUS.DISCONNECTED:
        logger.info(f'-x- {address} {message}')
    elif direction == STATUS.ERROR:
        logger.error(f'xxx {address} {message}')


# console exception handler
def handle_run_main(main, server_address):
    try:
        run(main())
    except KeyboardInterrupt:
        logger.info('User exit.')
    except ConnectionRefusedError:
        logger.error(f'{server_address} refused to accept a connection.')
    except ConnectionResetError:
        logger.error(f'Connection to {server_address} was reset.')
        logger.info(
            'This might caused by that TLS support is enabled on the server but not on client.'
        )
