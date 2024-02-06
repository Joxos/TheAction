"""
actions.py: Main logic of actions to process after recieved packages.
"""
from common.utils import logger
from sys import exit
import json
import os
from server.config import *

# resolve SQL connection
if SQL_TYPE == SQLTYPE.MYSQL:
    from pymysql import connect, Error
elif SQL_TYPE == SQLTYPE.MARIADB:
    from mariadb import connect, Error
elif SQL_TYPE == SQLTYPE.NONE:

    def connect(**kwargs):
        logger.error("No SQL selected. Cannot publish any connection.")
        exit(-1)

    class Error(Exception):
        pass


def change_question_mark(sentence):
    return sentence[:-1] + "!"


def database_test(sql):
    try:
        conn = connect(
            user=SQL_USER, password=SQL_PASSWORD, host=SQL_ADDRESS, port=SQL_PORT
        )
    except Error as e:
        logger.error(f"Error connecting to {SQL_TYPE.name.lower().title()}: {e}")
        return ""
    logger.info(f"Successfully connected to {SQL_TYPE.name.lower().title()}.")
    cur = conn.cursor()
    cur.execute(sql)
    res = ""
    for d in cur:
        res += d[0] + "\n"
    return res[:-1]


# write your own actions here


def login(username, password):
    if not os.path.exists("users.json"):
        return False
    with open("users.json", "r") as f:
        users = json.load(f)
    if username in users and users[username] == password:
        return True
    else:
        return False


def register(username, password):
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({username: password}, f)
        return True
    with open("users.json", "r") as f:
        users = json.load(f)
    if username in users:
        return False
    else:
        users[username] = password
        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
