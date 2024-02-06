"""
package.py: Define the format of different packages and ways to parse them.
"""
import json
from common.package import *


def pack_request_change_question_mark(sentence):
    return pack_json(
        {"type": PACKAGE.REQUEST_CHANGE_QUESTION_MARK.name, "sentence": sentence}
    )


def pack_request_mariadb_test(sql):
    return pack_json({"type": PACKAGE.REQUEST_MARIADB_TEST.name, "sql": sql})

def pack_request_login(username, password):
    return pack_json({"type": PACKAGE.REQUEST_LOGIN.name, "username": username, "password": password})

def pack_request_register(username, password):
    return pack_json({"type": PACKAGE.REQUEST_REGISTER.name, "username": username, "password": password})

def unpack_and_process(package):
    """Main logic to process every package."""
    package = json.loads(package)
    package_type = package.get("type")
    if package_type == PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name:
        return package.get("sentence")
    elif package_type == PACKAGE.ANSWER_MARIADB_TEST.name:
        return "\n" + package.get("result")
    elif package_type == PACKAGE.ANSWER_LOGIN.name:
        return package.get("result")
    elif package_type == PACKAGE.ANSWER_REGISTER.name:
        return package.get("result")
    else:
        return pack_unknown_package_type()
