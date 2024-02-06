'''
server.py: High-performance async server codes.
'''
import asyncio
import ssl

from common.protocol import on_init, is_framed
from common.utils import show_status, compress, decompress, STATUS, handle_run_main, logger
from server.package import unpack_and_process
from server.config import *


# callback style server:
class ServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.recieved_data = ''
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        on_init(self)
        show_status(STATUS.CONNECTED, self.address)

    def data_received(self, more_data):
        try:
            self.recieved_data += decompress(more_data).decode('utf-8')
        except:
            show_status(STATUS.ERROR, self.address,
                        'Failed to decompress or decode more data.')
            self.transport.close()
            return
        if is_framed(self):
            show_status(STATUS.RECV, self.address, self.recieved_data)
            # transfer control to actions.py
            res = unpack_and_process(self.recieved_data)
            self.transport.write(compress(bytes(res, encoding=default_coding)))
            show_status(STATUS.SEND, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_status(STATUS.DISCONNECTED, self.address)


async def main():
    context = None
    if enable_tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.check_hostname = False
        try:
            context.load_cert_chain(CRT_PATH, KEY_PATH)
        except FileNotFoundError:
            logger.error(f'File missing when using TLS.')
            return
        else:
            logger.info('TLS enabled.')
    else:
        logger.warning('TLS not enabled.')

    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: ServerProtocol(),
                                      SERVER_ADDRESS[0],
                                      SERVER_ADDRESS[1],
                                      ssl=context)

    logger.info(f'Listening at {SERVER_ADDRESS}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    handle_run_main(main, SERVER_ADDRESS)
