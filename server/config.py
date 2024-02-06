from common.config import *


class SQLTYPE(Enum):
    NONE = auto()
    MYSQL = auto()
    MARIADB = auto()


CRT_PATH = "server.crt"
KEY_PATH = "server.key"
SERVER_ADDRESS = ("127.0.0.1", 1145)
SQL_TYPE = SQLTYPE.MARIADB
SQL_ADDRESS = "192.168.2.115"
SQL_USER = "root"
SQL_PASSWORD = "123456"
SQL_PORT = 3306
OPEN_REGISTRATION = True
