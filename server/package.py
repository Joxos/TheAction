"""
package.py: Define the format of different packages and ways to parse them.
"""
import json
from server.actions import *
from common.package import *


def pack_answer_change_question_mark(sentence):
    return pack_json(
        {"type": PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name, "sentence": sentence}
    )


def pack_answer_mariadb_test(result):
    return pack_json({"type": PACKAGE.ANSWER_MARIADB_TEST.name, "result": result})


def pack_answer_login(result):
    return pack_json({"type": PACKAGE.ANSWER_LOGIN.name, "result": result})


def pack_answer_register(result):
    return pack_json({"type": PACKAGE.ANSWER_REGISTER.name, "result": result})


def unpack_and_process(package):
    """Main logic to process every package."""
    package = json.loads(package)
    package_type = package.get("type")
    if package_type == PACKAGE.REQUEST_CHANGE_QUESTION_MARK.name:
        return pack_answer_change_question_mark(
            change_question_mark(package.get("sentence"))
        )
    elif package_type == PACKAGE.REQUEST_MARIADB_TEST.name:
        return pack_answer_mariadb_test(database_test(package.get("sql")))
    elif package_type == PACKAGE.REQUEST_LOGIN.name:
        return pack_answer_login(
            login(package.get("username"), package.get("password"))
        )
    elif package_type == PACKAGE.REQUEST_REGISTER.name:
        return pack_answer_register(
            register(package.get("username"), package.get("password"))
        )
    else:
        return pack_unknown_package_type()
