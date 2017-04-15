#!/usr/bin/env python3

import sys
from urllib.error import URLError
from comands import put, get, OK, DOWN, CHECKER_ERROR
import traceback


def close(code, public="", private="", flag_id=""):
    """
    :param code: answer code
    :param public: anyone will see it
    :param private: only for admins
    :param flag_id: cache for put->get
    :return:
    """
    if flag_id:
        print(flag_id)
        exit(code)
    if public:
        print(public)
    if private:
        print(private, file=sys.stderr)
    exit(code)


def on_check(command_ip):
    check_result = put.check(command_ip)
    close(**check_result)


def on_put(command_ip, flag_id, flag, vuln=None):
    put_result = put.put(command_ip, flag_id, flag, vuln)
    close(**put_result)


def on_get(command_ip, flag_id, flag, vuln=None):
    get_result = get.get(command_ip, flag_id, flag, vuln)
    close(**get_result)


def on_info(*args):
    close(OK, "vulns: 1:1")


COMMANDS = {
    'check': on_check,
    'put': on_put,
    'get': on_get,
    'info': on_info
}


def not_found(*args):
    close(
        CHECKER_ERROR,
        "Checker error",
        "Unsupported command {}".format(sys.argv[1])
    )


if __name__ == '__main__':
    try:
        COMMANDS.get(sys.argv[1], not_found)(*sys.argv[2:])
    except URLError as e:
        close(DOWN, "Bad command address", "Checksystem fail {}"
              .format(traceback.format_exc(e)))
    except OSError as e:
        close(DOWN, "Socket I/O error", "SOCKET ERROR: {}".format(
            traceback.format_exc(e)))
    except Exception as e:
        close(CHECKER_ERROR, "Unknown error", "INTERNAL ERROR: {}"
              .format(traceback.format_exc(e)))
