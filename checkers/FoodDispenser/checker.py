#!/usr/bin/env python3

import sys
from urllib.error import URLError
from comands import put, get, OK, DOWN, CHECKER_ERROR
import traceback


def close(code, public="", private="", flag_id=""):
    print(code)
    if flag_id:
        print(flag_id)
        exit(code)
    if public:
        print(public)
    if private:
        print(private, file=sys.stderr)
    exit(code)


class CheckerException(Exception):
    """Custom checker error"""

    def __init__(self, msg):
        super(CheckerException, self).__init__(msg)


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
        "Unsupported command %s" % sys.argv[1]
    )


if __name__ == '__main__':
    try:
        COMMANDS.get(sys.argv[1], not_found)(*sys.argv[2:])
    except CheckerException as e:
        close(DOWN, "Service did not work as expected",
              "Checker exception: %s" % e)
    except URLError as e:
        close(DOWN, "Bad command address", "Checksystem fail {}".format(traceback.format_exc()))
    except OSError as e:
        close(DOWN, "Socket I/O error", "SOCKET ERROR: %s" % e)
    except Exception as e:
        close(CHECKER_ERROR, "Unknown error", "INTERNAL ERROR: %s"
              % traceback.format_exc())
